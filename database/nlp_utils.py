''' Class that parses text and determines sentiment and context'''
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import os

class NlpUtils():

    #Initializes environmental variables and the language API
    def __init__(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="gcp_credentials.json"

        #Instantiates a client for language services
        self.client=language.LanguageServiceClient()
        self.entriesDict = {}

        #Instance variable for types
        self.type_dict={

            0:"unknown",
            1:"person",
            2:"location",
            3:"organization",
            4:"event",
            5:"work_of_art",
            6:"consumer_good",
            7:"other"

        }

    #Analyzes sentiment
    def predict_sentiment(self,text):

        document=types.Document(
            content=text,
            type=enums.Document.Type.PLAIN_TEXT)

        sentiment=self.client.analyze_sentiment(document=document).document_sentiment

        sentiment_descriptor=self._classify_sentiment(sentiment.score)

        return sentiment_descriptor

    #Analyzes content
    def analyze_text_entities(self,text):

        document = types.Document(
            content=text,
            type=enums.Document.Type.PLAIN_TEXT)

        classifications=self.client.analyze_entities(document)

        cleaned_classification=self._clean_text_analysis(classifications)

        return cleaned_classification

    ''' Helper methods for contextualizing and preprocessing data'''
    def _clean_text_analysis(self,classification):

        cleaned_text_analysis={}

        # Loops through each analyzed entity
        for entity in classification.entities:
            dict_entry=[self.type_dict[entity.type],entity.salience]
            cleaned_text_analysis[entity.name]=dict_entry

        return cleaned_text_analysis

    #Helps qualify quantified sentiment
    def _classify_sentiment(self,score):

        polarity=""
        degree=""

        if score<0:
            polarity="Negative"
        else:
            polarity="Positive"

        if abs(score)>0.8:
            degree="Strongly "
        elif abs(score)<0.3:
            degree="Mildly "

        return degree+polarity

if __name__=="__main__":
    nlp_gc=NlpUtils()
    text=" kalsjdfkl;asjd;fla At this point in the story, two of the children are already gone: Augustus Gloop has been sucked up the chocolate pipe and Violet Beauregarde has been rolled off to the juicing room after turning into a gigantic blueberry. Now Mr. Wonka is rushing his slightly smaller tour group through the maze of factory corridors, whizzing them past thousands of rooms with the strangest titles on their doors"
    print(nlp_gc.predict_sentiment(text))
    print(nlp_gc.analyze_text_entities(text))