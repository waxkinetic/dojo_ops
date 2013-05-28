from __future__ import absolute_import

# standard
pass

# dojo
from awsspotmonitor import AwsSpotMonitor

# package
from .builder import update_and_notify


class DojoSpotMon(AwsSpotMonitor):
    def process_fulfilled(self, req):
        super(DojoSpotMon,self).process_fulfilled(req)

        # build new instance.
        if update_and_notify(req.instance_id) == 0:
            # add instance to our ELB.
            pass

        # need to make spotmon smarter so it keeps things in the same availability zone?
        # should do all this work in another process
