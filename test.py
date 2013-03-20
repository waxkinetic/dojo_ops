from fabcloudkit import *

Config.load()
ctx = Context('dojo_ops/fck/context.yaml')
ctx.aws_sync()

inst, role = ctx.get_host_in_role('single')
