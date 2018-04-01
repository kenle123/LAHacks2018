from flask import Flask, request, render_template, redirect, url_for
from twilio.rest import Client
from twilio.twiml.messaging_response import Message, MessagingResponse, Redirect
from firebase_utils import FirebaseUtils
from nlp_utils import NlpUtils

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
texter = Trivilio_bae("+17148048394") #"+17148371567"
global convo_level
global NLP#Natural Language Processing
global FB #FireBase
FB = FirebaseUtils("antroomies@gmail.com","zotzotzot")
NLP = NlpUtils()
FB.sign_in_user(FB.email, FB.password)

@app.route("/")
def main():
    global convo_level
    global NLP
    global FB
    print("Program Start")
    texter.sendText("How was your day today?")
    convo_level = "base"
    return "Complete"

@app.route("/sms", methods=['GET', 'POST'])
def handleResponse():
    global convo_level
    global NLP
    global FB
    print(convo_level) #testing what it is
    body = request.values.get('Body', None)
    response = MessagingResponse()
    #body sent into nlp
    sentimental = NLP.predict_sentiment(body)
    FB.update_response_history_db(body, sentimental)
    vocab = NLP.analyze_text_entities(body) #not sure what the data members do and why
    FB._check_stressor_vocabulary(vocab)
    #get this ^ looked over at.
    if(convo_level == "base"):
        #check for postive or negative reponse
        if("Positive" in sentimental):#positive
            response.message("That's great to hear! What made it so great?")
            convo_level = "positive1"
        else: #negative
            response.message("It's okay. Even Steve Jobs gets runtime errors.")
            convo_level = "negative2"
        return str(response)
    elif(convo_level == "positive1"):
        response.message("")
        #update db and respond based on analysis
        #respond based on most frequent type of word (0-7)
        convo_level = "positive2"
    elif(convo_level == "positive2"): #not sure how deep we should do in convo
        response.message("")
        #update db and respond based on analysis
        #respond based on most frequent type of word (0-7)
    elif(convo_level == "negative1"): #not sure how deep we should do in convo
        response.message("")
        #update db and respond based on analysis
        #respond based on most frequent type of word (0-7)
        convo_level = "negative2"
    elif(convo_level == "negative2"): #not sure how deep we should do in convo
        response.message("")
        #update db and respond based on analysis
        #respond based on most frequent type of word (0-7)
    else: #neutral
        response.message("")
        #update db and respond based on analysis
    return str(response)

#def 

if __name__ == "__main__":
    app.run()
