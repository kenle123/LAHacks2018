from twilio.rest import Client
from twilio.twiml.messaging_response import Message, MessagingResponse, Redirect

class Trivilio_bae:
    # Find these values at https://twilio.com/user/account
    
    def __init__(self, toNum):
        self.account_sid = "AC7af9b1a6b83c353bed3e1fd20bd77879"
        self.auth_token = "9ddee86ec6f70a5b6a82866fb47dd0a3"
        self.client = Client(self.account_sid, self.auth_token)
        self.toNUMBER = toNum

    def sendText(self, message):
        self.client.api.account.messages.create(
        to = self.toNUMBER,
        from_ = "+14124670847",
        body = message)

    def responseText(self, text):
        response = MessagingResponse()
        response.message(text)    
