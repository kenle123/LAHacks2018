import pyrebase
from nlp_utils import NlpUtils
from datetime import datetime,date

class FirebaseUtils:

    def __init__(self,email,password):

        #Initializes the firebase set up for the app
        config = {
            "apiKey": "AIzaSyCbDjZY8k6rGXRLzE3C4_qOl7A9lzekWCA",
            "authDomain": "baymax-5a01c.firebaseapp.com",
            "databaseURL": "https://baymax-5a01c.firebaseio.com",
            "storageBucket": "baymax-5a01c.appspot.com",
            "serviceAccount":"Baymax-c7785fbef68e.json"
        }

        self.firebase = pyrebase.initialize_app(config)
        self.firebase_db = self.firebase.database()
        self.auth=self.firebase.auth()
        self.email=email
        self.password=password
        self.idToken=None
        self.local_id=None
        self.name=None


    ''' Initial database interfacing methods'''
    def create_user(self,email,password):
        self.auth.create_user_with_email_and_password(email,password)

    def sign_in_user(self,email,password):
        self.user=self.auth.sign_in_with_email_and_password(email,password)
        self.idToken=self.user["idToken"]
        self.local_id=self.user["localId"]
        self.email=self.user["email"]


    def write_user_db(self):
        #Initializes the data structures
        user={}
        user_info={} #All available info about users

        #user_info["name"]=self.name
        user_info["email"]=self.email
        user[self.local_id]=user_info
        self.firebase_db.child("users").child().set(user,self.idToken)


    def create_sentiment_history_db(self,sentiment):

        sentiment_obj=self._sentiment_obj_create(sentiment)
        self.firebase_db.child("users").child(self.local_id).child("sentiment_history").push(sentiment_obj, self.idToken)

    def update_sentiment_history_db(self,sentiment):

        #Creates sentiment object from the sentiment passed in
        sentiment_obj = self._sentiment_obj_create(sentiment)

        #Updates sentiment
        self.firebase_db.child("users").child(self.local_id).child("sentiment_history").push(sentiment_obj,self.idToken)

    def create_response_history_db(self,response,sentiment):

        #Creates history of response object from the response and sentiment
        response_obj=self._response_obj_create(response,sentiment)

        #Creates sentiment
        self.firebase_db.child("users").child(self.local_id).child("response_history").push(response_obj,self.idToken)

    def update_response_history_db(self,response,sentiment):

        #Creates history of response object from the response and sentiment
        response_obj=self._response_obj_create(response,sentiment)

        #Creates sentiment
        self.firebase_db.child("users").child(self.local_id).child("response_history").push(response_obj,self.idToken)

    def create_vocabulary_db(self,new_vocab):
        for key in new_vocab:
            self.firebase_db.child("users").child(self.local_id).child("vocabulary").child(key).set(new_vocab[key],self.idToken)
            self.firebase_db.child("users").child(self.local_id).child("vocabulary").child(key).child("frequency").set(1,
                                                                                                    self.idToken)
    def update_vocabulary_db(self,new_vocab,vocab_list):
        for new_word in new_vocab:
            print(new_word)
            if new_word in vocab_list:
                frequency = self.firebase_db.child("users").child(self.local_id).child("vocabulary").child(
                    new_word).child("frequency").get(self.idToken)
                self.firebase_db.child("users").child(self.local_id).child("vocabulary").child(new_word).child(
                    "frequency").set(frequency.val() + 1, self.idToken)

            else:
                self.firebase_db.child("users").child(self.local_id).child("vocabulary").child(new_word).set(
                    new_vocab[new_word], self.idToken)
                self.firebase_db.child("users").child(self.local_id).child("vocabulary").child(new_word).child(
                    "frequency").set(1, self.idToken)

    ''' Helper functions for creating fields '''
    def _sentiment_obj_create(self,sentiment):
        sentiment_obj = {}

        time_stamp = str(datetime.now())  # Replace with actual time stamp
        sentiment_obj["sentiment"] = sentiment
        sentiment_obj["timestamp"] = time_stamp

        return sentiment_obj

    #Creates the response stored in db
    def _response_obj_create(self,response,sentiment):
        response_obj={}

        day_stamp=str(date.today())

        #Writes response to dictionary
        response_obj["sentiment"] = sentiment
        response_obj["response"]=response
        response_obj["timestamp"] = day_stamp

        return response_obj

    #Will check the stressor frequency and give suggested actions if the stressor is strongly neg
    def _check_stressor_vocabulary(self,new_vocab):

        vocab_list=self._create_vocab_list()
        if vocabulary==None:
            self.create_vocabulary_db(new_vocab)

        else:
            self.update_vocabulary_db(new_vocab,vocab_list)

    #Pre-processes the vocab for the checking mechanism
    def _create_vocab_list(self):
        vocab_list = []
        vocabulary = self.firebase_db.child("users").child(self.local_id).child("vocabulary").get(self.idToken).each()
        for word in vocabulary:
            vocab_list.append(word.key())

        return vocab_list

''' Used for testing firebase_utils '''
if __name__=="__main__":
    nlpUtils=NlpUtils()
    fbUtils=FirebaseUtils("antroomies@gmail.com","zotzotzot")
    #utils.create_user(utils.email,utils.password) Remove comment if account does not exist
    fbUtils.sign_in_user(fbUtils.email, fbUtils.password)
    #fbUtils.write_user_db()


    for i in range(1):
        #text1=nlpUtils.predict_sentiment("HATE HATE HATE Person. Trees. Person")
        text2=nlpUtils.predict_sentiment("Love. I love this. Amazing. Great. Love!")
        #fbUtils.create_sentiment_history_db(text1)
        #fbUtils.update_sentiment_history_db(text2)
        #fbUtils.create_response_history_db("I love you",text1)
        fbUtils.update_response_history_db("Everything here on this earth I love",text2)
        vocabulary=nlpUtils.analyze_text_entities("My mom has been making me so mad. So mad. Mom")
        fbUtils._check_stressor_vocabulary(vocabulary)
