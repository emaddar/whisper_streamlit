# pip install --upgrade --force-reinstall azure-ai-textanalytics
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from dotenv import load_dotenv
import os

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
    poller = client.begin_abstract_summary(document)
    abstract_summary_results = poller.result()
    for result in abstract_summary_results:
        if result.kind == "AbstractiveSummarization":
            # return [summary.contexts[0].length for summary in result.summaries] # liste des longueurs des résumés
            # return [f"{summary.text}" for summary in result.summaries] # liste des résumés
            return "\n".join([summary.text for summary in result.summaries]) # string des résumé
        elif result.is_error is True:
            print("...Is an error with code '{}' and message '{}'".format(
                result.error.code, result.error.message
            ))