from __future__ import absolute_import

# standard
from collections import namedtuple
from datetime import datetime
import json
import sys
import traceback

# pypi
from fabric.state import output

# dojo
from dojo_ops import Builder


# command line argument values.
_Args = namedtuple('_Args', 'instance_id, role_name, also_activate, provision')


def _parse_args(*args):
    if not args:
        args = sys.argv[1:]

    instance_id = args[0]
    role_name = args[1]
    if len(args) <= 2:
        # default value.
        also_activate = None
    elif '[' in args[2]:
        also_activate = json.loads(args[2])
    else:
        also_activate = args[2]
    provision = True if len(args) <= 3 else bool(int(args[3]))

    print('instance-id: {0} / role: {1} / also_activate: {2} / provision: {3}'
          .format(instance_id, role_name, also_activate, provision))
    return _Args(instance_id, role_name, also_activate, provision)


def build_instance(*args):
    """Updates an EC2 instance using the dojo fabcloudkit configuration.

    Simple wrapper to call to Builder().update() that allows parameters to be specified from the
    command line, and output to be redirected/captured for logging or email delivery.
    (Fabric does not currently allow capturing log output in a reasonable way.)

    The args must be as follows (very little error checking is performed):
        args[0]: instance_id of an EC2 instance
        args[1]: name of the fabcloudkit role
        args[2]: optional: a string, or a json list of strings; each string
                 identifies a fabcloudkit role, in addition to args[1],
                 that should also be activated on the instance (note that
                 these roles are never provisioned or built, just activated).
                 Can be "null" to indicated empty when also specifying args[3].
        args[3]: optional: [0|1], default=1. If 1, indicates that the instance
                 should be provisioned for the role args[1]. If 0 then no
                 provisioning takes place.
    """
    print('BEGIN DOJO INSTANCE UPDATE:')
    print('{0} UTC'.format(datetime.utcnow().isoformat()))
    args = _parse_args(*args)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~')

    code = 0
    try:
        # quiet down the output volume.
        output['running'] = False
        Builder().update(args.instance_id, args.role_name, args.also_activate, args.provision)
    except:
        traceback.print_exc()
        code = 1

    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    if code:
        print('***** UPDATE FAILED *****')
    print('{0} UTC'.format(datetime.utcnow().isoformat()))
    print('END DOJO INSTANCE UPDATE.')
    exit(code)


if __name__ == '__main__':
    build_instance()
