from twilio.rest import Client
import os

def send(body='', to='+13057984105'):
    # Your Account Sid and Auth Token from twilio.com/console
    # DANGER! This is insecure. See http://twil.io/secure
    account_sid = 'AC94e8b0d3e7dd7969485fbc45b982abda'
    auth_token = 'aaffc0412f30ea9cc374a3d3e6bbc075'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=body,
        from_='+12546025189',
        to='+13057984105'
    )

    print(message.sid)

