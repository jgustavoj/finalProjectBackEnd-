from twilio.rest import Client
import os

def send(body='Some body', to=''):
    # Your Account Sid and Auth Token from twilio.com/console
    # DANGER! This is insecure. See http://twil.io/secure
    account_sid = 'ACebcf1c431d0537bdb929713268a2e58f'
    auth_token = 'b8c38652760d2384938d6c1041831ad0'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=body,
        from_='+12013899753',
        to='+19546465110'
    )

    print(message.sid)