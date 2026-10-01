# SPDX-License-Identifier: GPL-3.0-or-later
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('manage', Path(__file__).resolve().parents[1]/'scripts/manage.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def settings(root):
    return dict(project='test-ai', owner_name='Test Owner', agent_name='Test AI',
                linux_user='tester', ssh_host='192.0.2.10', ssh_port=22, timezone='UTC',
                data_dir=str(root), hermes_image='nousresearch/hermes-agent:latest',
                portainer_image='portainer/portainer-ce:lts', kuma_image='louislam/uptime-kuma:2',
                tailscale_image='tailscale/tailscale:stable', tailscale_hostname='test-ai-node',
                portainer_port=9443, kuma_port=3001, telegram_users='123456789')


class FakeEngine:
    def __init__(self): self.calls=[]; self.prefix=['docker']
    def call(self,*args,**kwargs):
        self.calls.append(args)
        if args[:1] == ('ps',): return subprocess.CompletedProcess(args,0,stdout='hermes\nkuma\n')
        return subprocess.CompletedProcess(args,0,stdout='{}')
    def cli(self,*args):
        self.call('stop','hermes')
        return self.call('run','--rm','--no-deps','hermes',*args)


class InstallerTests(unittest.TestCase):
    def test_gateway_not_interactive_daemon(self):
        c=m.compose_spec(settings('/tmp/test-runtime'))
        self.assertEqual(c['services']['hermes']['command'],['gateway','run'])
        self.assertEqual(len([x for x in c['services'] if x=='hermes']),1)
        self.assertNotIn('ports',c['services']['hermes'])

    def test_no_socket_or_host_network_to_agent(self):
        c=m.compose_spec(settings('/tmp/test-runtime'))
        for service in ['hermes','kuma']:
            self.assertNotIn('/var/run/docker.sock',json.dumps(c['services'][service]))
            self.assertNotIn('privileged',c['services'][service])
            self.assertNotEqual(c['services'][service].get('network_mode'),'host')
        self.assertEqual(c['services']['hermes']['networks'],['agent'])
        self.assertEqual(c['services']['portainer']['networks'],['management'])

    def test_localhost_admin_ports(self):
        c=m.compose_spec(settings('/tmp/test-runtime'))
        for service in ['portainer','kuma']:
            self.assertTrue(all(port.startswith('127.0.0.1:') for port in c['services'][service]['ports']))

    def test_persistent_state_and_tailscale_no_authkey(self):
        c=m.compose_spec(settings('/tmp/test-runtime'))
        self.assertIn('/opt/data',[v['target'] for v in c['services']['hermes']['volumes']])
        self.assertIn('/var/lib/tailscale',[v['target'] for v in c['services']['tailscale']['volumes']])
        self.assertNotIn('TS_AUTHKEY',json.dumps(c))
        self.assertEqual(c['services']['tailscale']['entrypoint'],['tailscaled'])

    def test_atomic_private_write(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'config'
            m.atomic(p,'private')
            self.assertEqual(p.stat().st_mode & 0o777,0o600)
            self.assertEqual(p.read_text(),'private')

    def test_reject_dangerous_data_paths(self):
        for p in ['/', '/etc', '/tmp', '/var/lib/docker', './relative', '/tmp/$(id)/data']:
            self.assertFalse(m.valid_data(p),p)
        with tempfile.TemporaryDirectory() as t:
            self.assertTrue(m.valid_data(t+'/new-services/data'))

    def test_configure_secret_not_in_settings_or_compose(self):
        with tempfile.TemporaryDirectory() as t:
            rt=Path(t)/'runtime'; state=Path(t)/'state'
            values=iter(['test-ai','John Doe','John AI','john','192.0.2.10','22','UTC',str(state),
                         'nousresearch/hermes-agent:latest','portainer/portainer-ce:lts',
                         'louislam/uptime-kuma:2','tailscale/tailscale:stable','john-ai-node',
                         '9443','3001','123456789','y'])
            secret='123456:'+('x'*30)
            with patch.object(m,'CONFIG',rt/'settings.json'), patch.object(m,'COMPOSE',rt/'compose.json'),\
                 patch('builtins.input',side_effect=lambda _: next(values)), patch.object(m.getpass,'getpass',return_value=secret):
                c=m.configure()
                self.assertNotIn(secret,(rt/'settings.json').read_text())
                self.assertNotIn(secret,(rt/'compose.json').read_text())
                env=(state/'hermes/.env').read_text()
                self.assertIn(secret,env)
                self.assertIn("GATEWAY_ALLOW_ALL_USERS='false'",env)
                original=(state/'hermes/SOUL.md').read_text()
                m.configure() # no prompts and no regeneration
                self.assertEqual((state/'hermes/SOUL.md').read_text(),original)
                self.assertFalse(m.initial_hermes(c)['auxiliary']['title_generation']['enabled'])

    def test_failed_oauth_does_not_start_gateway(self):
        with tempfile.TemporaryDirectory() as t:
            e=FakeEngine(); c=settings(t)
            with patch.object(m,'lock_images'), patch.object(m,'prepare_workspace'), patch.object(m,'yes',return_value=False):
                with self.assertRaises(RuntimeError): m.install(c,e)
            self.assertFalse(any(x[:2]==('up','-d') for x in e.calls))
            self.assertIn(('stop','hermes'),e.calls)
            self.assertTrue(any('--oneshot' in x for x in e.calls))

    def test_backup_failure_restarts_only_previously_running_services(self):
        with tempfile.TemporaryDirectory() as t:
            e=FakeEngine()
            with patch.object(m.subprocess,'run',side_effect=subprocess.CalledProcessError(1,['tar'])):
                with self.assertRaises(subprocess.CalledProcessError): m.backup(settings(t),e)
            self.assertIn(('stop',),e.calls)
            self.assertEqual(e.calls[-1],('up','-d','hermes','kuma'))

    def test_image_pinning(self):
        with tempfile.TemporaryDirectory() as t:
            c=settings(t); e=FakeEngine()
            digest='registry.invalid/test@sha256:'+('a'*64)
            with patch.object(m,'CONFIG',Path(t)/'settings.json'), patch.object(m,'COMPOSE',Path(t)/'compose.json'),\
                 patch.object(m.subprocess,'check_output',return_value=json.dumps([digest])):
                m.lock_images(c,e)
            self.assertEqual(c['hermes_image'],digest)
            self.assertIn(('pull',),e.calls)
            self.assertNotIn(':latest',(Path(t)/'compose.json').read_text())

    def test_missing_digest_aborts(self):
        with patch.object(m.subprocess,'check_output',return_value='[]'):
            with self.assertRaises(RuntimeError): m.lock_images(settings('/tmp/test-state'),FakeEngine())

    def test_successful_install_records_human_acceptance(self):
        with tempfile.TemporaryDirectory() as t:
            e=FakeEngine(); c=settings(t)
            original_exists=Path.exists
            with patch.object(m,'lock_images'), patch.object(m,'prepare_workspace'), \
                 patch.object(m,'yes',return_value=True), patch.object(m,'RUNTIME',Path(t)), \
                 patch.object(Path,'exists',lambda p: True if str(p)=='/dev/net/tun' else original_exists(p)):
                m.install(c,e)
            accepted=json.loads((Path(t)/'acceptance.json').read_text())
            self.assertTrue(accepted['telegram_confirmed_by_user'])
            self.assertTrue(accepted['oauth_confirmed_by_user'])
            self.assertIn(('up','-d','hermes','portainer','kuma'),e.calls)
            self.assertIn(('up','-d','tailscale'),e.calls)

    def test_wrong_provider_blocks_gateway_start(self):
        class RejectedProvider(FakeEngine):
            def call(self,*args,**kwargs):
                if '--entrypoint' in args and 'python3' in args:
                    raise subprocess.CalledProcessError(1,args)
                return super().call(*args,**kwargs)
        e=RejectedProvider()
        with patch.object(m,'lock_images'), patch.object(m,'prepare_workspace'):
            with self.assertRaises(subprocess.CalledProcessError): m.install(settings('/tmp/test-state'),e)
        self.assertFalse(any(x[:2]==('up','-d') for x in e.calls))

    def test_no_shell_interpolation_in_ssh_command(self):
        c=settings('/tmp/data')
        self.assertEqual(c['ssh_host'],'192.0.2.10')
        self.assertIn('no-new-privileges:true',m.compose_spec(c)['services']['hermes']['security_opt'])


if __name__=='__main__': unittest.main()
