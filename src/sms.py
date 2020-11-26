from twilio.rest import Client
import os

def send(body='', to='+13057984105'):
    # Your Account Sid and Auth Token from twilio.com/console
    # DANGER! This is insecure. See http://twil.io/secure
    # account_sid = 'account from twilio'
    # auth_token = 'token from twilio account'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=body,
        from_='+12546025189',
        to='+13057984105'
    )

    print(message.sid)

# make sure to add account sid and auth token from twilio personal account on line 7 and 8