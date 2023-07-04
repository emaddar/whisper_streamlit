# pip install --upgrade --force-reinstall azure-ai-textanalytics
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import (
        TextAnalyticsClient,
        RecognizeEntitiesAction,
        RecognizePiiEntitiesAction,
    )
from dotenv import load_dotenv
import os
import typing
load_dotenv()
key1 = os.getenv('key1')
key2 = os.getenv('key2')
endpoint = os.getenv('endpoint')



# Authenticate the client using your key and endpoint 
def authenticate_client():
    ta_credential = AzureKeyCredential(key1)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client


def sample_extractive_summarization(document):
    client = authenticate_client()
    poller = client.begin_extract_summary(document)
    extract_summary_results = poller.result()
    for result in extract_summary_results:
        if result.kind == "ExtractiveSummarization":
            return "\n".join([sentence.text for sentence in result.sentences])
        elif result.is_error is True:
            print("...Is an error with code '{}' and message '{}'".format(
                result.error.code, result.error.message
            ))

def sample_abstractive_summarization(document):
    client = authenticate_client()
    summary = ""
    poller = client.begin_abstract_summary(document)
    abstract_summary_results = poller.result()
    # summary.contexts
    for result in abstract_summary_results:
        print(result,end='\n\n\n')
        if result.is_error is True:
            print("...Is an error with code '{}' and message '{}'".format(result.error.code, result.error.message))
        summary += "\n".join([summary.text for summary in result.summaries]) + '\n\n'
    return summary


def sample_recognize_entities(document):
    client = authenticate_client()
    result = client.recognize_entities(document)
    result = [review for review in result if not review.is_error]
    dico = {}
    # entity.confidence_score
    for review in result:
        for entity in review.entities:
            if entity.category not in dico :
                dico[entity.category] = set([entity.text])
            else :
                dico[entity.category].add(entity.text)
    return dico


def sample_recognize_actions(document):
    client = authenticate_client()
    dico = {}
    poller = client.begin_analyze_actions(
            document,
            display_name="Sample Text Recognize",
            actions=[
                RecognizeEntitiesAction(),
                RecognizePiiEntitiesAction(),
            ],
        )
    document_results = poller.result()
    for action_results in document_results:
        for result in action_results:
            if result.is_error is True:
                print(f"...Is an error with code '{result.error.code}' and message '{result.error.message}'")
            for entity in result.entities:
                if entity.category not in dico :
                    dico[entity.category] = set([entity.text])
                else :
                    dico[entity.category].add(entity.text)
    return dico


def sample_extract_key_phrases(document):
    client = authenticate_client()
    key_phrases = []
    result = client.extract_key_phrases(document)
    for doc in result:
        if not doc.is_error:
            key_phrases.append(", ".join(doc.key_phrases))
    return "\n".join(key_phrases)



def sample_analyze_sentiment(document):
    client = authenticate_client()
    result = client.analyze_sentiment(document, show_opinion_mining=False)
    doc_result = [doc.confidence_scores for doc in result if not doc.is_error]
    return(doc_result)




if __name__ == '__main__':
    document = [
        'We went to Contoso Steakhouse located at midtown NYC last week for a dinner party, and we adore the spot! '
        'They provide marvelous food and they have a great menu. The chief cook happens to be the owner (I think his name is John Doe) '
        'and he is super nice, coming out of the kitchen and greeted us all.'
        ,

        'We enjoyed very much dining in the place! '
        'The Sirloin steak I ordered was tender and juicy, and the place was impeccably clean. You can even pre-order from their '
        'online menu at www.contososteakhouse.com, call 312-555-0176 or send email to order@contososteakhouse.com! '
        'The only complaint I have is the food didn\'t come fast enough. Overall I highly recommend it!'
    ]
    print(sample_analyze_sentiment(document))