from __future__ import absolute_import

# standard
from collections import namedtuple
import os

MailConfig = namedtuple('MailConfig', 'conn, sender, recipients')(
    conn = dict(
        host = 'email-smtp.us-east-1.amazonaws.com',
        port = 465,
        use_ssl = True,
        use_tls = False,
        username = os.environ['SES_USERNAME'],
        password = os.environ['SES_PASSWORD']
    ),
    sender = ('Dojo OPS', 'no-reply@dojo.dj'),
    recipients = [
        'borick@gmail.com'
    ]
)
