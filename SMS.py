import os
from twilio.rest import Client

# Set environment variables for your credentials
# Read more at http://twil.io/secure
account_sid = "AC5f36cf50b6f51600683bbf3390e6961a"
auth_token = "cc086000b578ae88a2b3b031e403213d"
client = Client(account_sid, auth_token)


def Warning_msg(msg: str):
    message = client.messages.create(
        body=msg,
        from_="+13854583625",
        to="+212624160665"
    )