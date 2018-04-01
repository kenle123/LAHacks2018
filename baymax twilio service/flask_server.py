from flask import Flask, request, render_template, redirect, url_for
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

app = Flask(__name__)
texter = Trivilio_bae("+17148371567") #"+17148371567"
global convo_level

@app.route("/")
def main():
    global convo_level
    print("Start up!")
    texter.sendText("How was your day today?")
    convo_level = "base"
    return "Complete"

@app.route("/sms", methods=['GET', 'POST'])
def handleResponse():
    global convo_level
    print(convo_level) #testing what it is
    body = request.values.get('Body', None)
    response = MessagingResponse()
    if(convo_level == "base"):
        if("great" in body or "Great" in body or body == "Great" or body == "great"):
            response.message("That's great to hear! What made it so great?")
            convo_level = "great"
        elif("hate" in body or "Hate" in body or "HATE" in body):
            response.message("It's okay. Even Steve Jobs gets runtime errors.")
            convo_level = "hate"
        else:
            response.message("Sorry I have no response for that yet")
        return str(response)
    elif(convo_level == "great"):
        response.message("Daddy Elon would be proud ;)")
    return str(response)

#def 

if __name__ == "__main__":
    app.run()
