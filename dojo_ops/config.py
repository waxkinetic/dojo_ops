from __future__ import absolute_import

# standard
from collections import namedtuple


MailConfig = namedtuple('MailConfig', 'conn, sender, recipients')(
    conn = dict(
        host = 'email-smtp.us-east-1.amazonaws.com',
        port = 465,
        use_ssl = True,
        use_tls = False,
        username = 'AKIAJBSLXQSCGLOXTMFA',
        password = 'AobVwVCx43kFQ48rpiClYVG4JaFwg8AnV/JFulu56D8K'
    ),
    sender = ('Dojo OPS', 'no-reply@dojo.dj'),
    recipients = [
        'borick@gmail.com'
    ]
)
