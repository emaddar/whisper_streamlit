# pip install --upgrade --force-reinstall azure-ai-textanalytics
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from dotenv import load_dotenv
import streamlit as st
# load_dotenv()
# key1 = os.getenv('key1')
# key2 = os.getenv('key2')
# endpoint = os.getenv('endpoint')
key1 = st.secrets["key1"]
key2 = st.secrets["key2"]
endpoint = st.secrets["endpoint"]



# Authenticate the client using your key and endpoint 
def authenticate_client():
    ta_credential = AzureKeyCredential(key1)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client


def sample_extractive_summarization(document):
    client = authenticate_client()
    summary = []
    poller = client.begin_extract_summary(document)
    extract_summary_results = poller.result()
    for result in extract_summary_results:
        if result.is_error is True:
            print("...Is an error with code '{}' and message '{}'".format(result.error.code, result.error.message))
        else :
            summary.append("\n".join([sentence.text for sentence in result.sentences]))
    return "\n".join(summary)



def sample_abstractive_summarization(document):
    client = authenticate_client()
    summary = []
    poller = client.begin_abstract_summary(document)
    abstract_summary_results = poller.result()
    # summary.contexts
    for result in abstract_summary_results:
        if result.is_error is True:
            print("...Is an error with code '{}' and message '{}'".format(result.error.code, result.error.message))
        else :
            summary.append("\n".join([summary.text for summary in result.summaries]))
    return "\n".join(summary)