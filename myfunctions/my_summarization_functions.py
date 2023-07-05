# pip install --upgrade --force-reinstall azure-ai-textanalytics
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import (
        TextAnalyticsClient,
        RecognizeEntitiesAction,
        RecognizePiiEntitiesAction,
    )
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


def sample_recognize_to_annotated_text(document):
    client = authenticate_client()
    poller = client.begin_analyze_actions(
            document,
            display_name="Sample Text Recognize",
            actions=[
                RecognizeEntitiesAction(),
                RecognizePiiEntitiesAction(),
            ],
        )
    document_results = poller.result()
    score_min = 0.5
    sort_by_start_order = lambda tuple: tuple[0]

    ner = [sorted(list(set([(entity.offset,entity.offset+entity.length,entity.category,entity.confidence_score) for result in action_results if result.is_error is False for entity in result.entities if (entity.confidence_score > score_min)])), key=sort_by_start_order) for action_results in document_results]

    filtered_ner = [[tup[:-1] for tup in texte_ner if tup[3] == max([t[3] for t in texte_ner if t[0] == tup[0] or t[1] == tup[1] or ((t[1] > tup[1]) and (t[0] < tup[0])) or ((t[1] < tup[1]) and (t[0] > tup[0]))])] for texte_ner in ner]

    res =[]
    for idx_texte,texte in enumerate(document):
        position=0
        for (start,stop,category) in filtered_ner[idx_texte]:
            if texte[position:start] !='':
                res.append((texte[position:start], ''))
            res.append((texte[start:stop], category))
            position = stop
        res.append((texte[stop:], ''))
        res.append(('\n',''))
    return res[:-1]