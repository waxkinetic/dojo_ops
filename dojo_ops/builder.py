from __future__ import absolute_import

# standard
from functools import partial
import json
import os
from pkg_resources import resource_filename
import subprocess
import sys
from tempfile import NamedTemporaryFile
import time
import traceback

# pypi
import boto.ec2
from fabric.exceptions import NetworkError
from fabric.network import disconnect_all

# dojo
from awsspotmonitor import create_plaintext_msg, send_plaintext_msg
from fabcloudkit import Config, Context

# package
from .config import MailConfig


__all__ = ['Builder', 'update_and_notify', 'run_script']


def update_and_notify(instance_id, provision=False):
    code, text = run_script(instance_id, 'single', ['webapi', 'qman'], provision)
    sender, recipients, msg = create_plaintext_msg(
        'Dojo OPS instance update results',
        MailConfig.sender, MailConfig.recipients, text)
    send_plaintext_msg(MailConfig.conn, sender, recipients, msg)
    return code


def run_script(instance_id, role_name, also_activate=None, provision=True):
    """Runs the update, captures and returns the output.

    This implementation is roundabout because Fabric doesn't current allow capturing
    of information logged to screen. So, we jump through some hoops to run a script
    in a separate process, and remap stdin and stdout to capture output. That script
    in turn simply calls the update() method on Builder.

    :param instance_id: the EC2 instance to update.
    :param role_name: the fabcloudkit role for the instance.
    :param also_activate: optional; additional fabcloudkit roles to activate on the
                          instance. these roles are not used to provision or
                          build, only to activate.
    :param provision: if True, the instance is provisioned before build and activation.
    :return: (code, text) tuple: the process return code, and the captured output.
    """
    with NamedTemporaryFile(mode='w+b', prefix='dojo_ops_', delete=True) as file:
        print('capturing update output: {0}'.format(file.name))

        # build script arguments.
        args = [
            sys.executable,
            resource_filename(__name__, 'scripts/build.py'),
            instance_id,
            role_name,
            also_activate if isinstance(also_activate, basestring) else json.dumps(also_activate),
            str(int(provision))
        ]

        # execute script and capture output.
        code = 1
        try:
            code = subprocess.call(args, stdout=file, stderr=file)
        except:
            file.write('\nexception raised by subprocess.call()\n')
            traceback.print_exc(file=file)

        # read captured output, return code and output.
        file.seek(0)
        text = file.read()
        return code, text


class Builder(object):
    def __init__(self, region_name='us-east-1'):
        Config.load()
        self._ctx = Context(resource_filename(__name__, 'fck/context.yaml'))
        self._conn = boto.ec2.connect_to_region(region_name,
            aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])

    def update(self, instance_id, role_name, also_activate=None, provision=True):
        if also_activate is None:
            also_activate = []
        if also_activate and isinstance(also_activate, basestring):
            also_activate = [also_activate]

        inst = self._get_single_instance(instance_id)
        role = self._ctx.get_role(role_name)
        lst = [] if not provision else [partial(role.provision_instance, inst)]
        lst.append(partial(role.build_instance, inst))
        lst.append(partial(role.activate_instance, inst))

        for name in also_activate:
            lst.append(partial(self._ctx.get_role(name).activate_instance, inst))

        for f in lst:
            self._exec_with_reconnect(f)

    def _exec_with_reconnect(self, f, tries=5, wait_sec=8):
        while tries > 0:
            try:
                return f()
            except NetworkError:
                traceback.print_exc()
                disconnect_all()
                time.sleep(wait_sec)
                tries -= 1
                wait_sec *= 2
        raise RuntimeError('Unable to execute after multiple attempts.')

    def _get_single_instance(self, id):
        """Returns a single EC2 instance.

        Convenience method.

        :param id: specifies the instance ID.
        :return: the instance object, or None.
        """
        r = self._conn.get_all_instances(id)
        return r[0].instances[0] if r and r[0].instances else None
