# pip install --upgrade --force-reinstall azure-ai-textanalytics
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import (
        TextAnalyticsClient,
        RecognizeEntitiesAction,
        RecognizePiiEntitiesAction,
    )
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


def sample_recognize_entities(document):
    client = authenticate_client()
    result = client.recognize_entities(document)
    result = [review for review in result if not review.is_error]
    dico = {}
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



def sample_recognize(document):
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

    ner = [sorted(list(set([(entity.offset,entity.offset+entity.length,entity.category,entity.text,entity.confidence_score) for result in action_results if result.is_error is False for entity in result.entities if (entity.confidence_score > score_min)])), key=sort_by_start_order) for action_results in document_results]
    
    filtered_ner = [[tup[:-1] for tup in texte_ner if tup[4] == max([t[4] for t in texte_ner if t[0] == tup[0] or t[1] == tup[1] or ((t[1] > tup[1]) and (t[0] < tup[0])) or ((t[1] < tup[1]) and (t[0] > tup[0]))])] for texte_ner in ner]
    return filtered_ner

def list_to_dict(document):
    var_dict = {}
    var = sample_recognize(document)
    for sublist in var:
        for tuple_item in sublist:
            entity_type = tuple_item[2]
            entity_value = tuple_item[3]
            
            if entity_type in var_dict:
                var_dict[entity_type].append(entity_value)
            else:
                var_dict[entity_type] = [entity_value]
    return var_dict
    
def sample_recognize_to_annotated_text(document):
    filtered_ner = sample_recognize(document)
    res =[]
    for idx_texte,texte in enumerate(document):
        position=0
        for (start,stop,category,entity) in filtered_ner[idx_texte]:
            if texte[position:start] !='':
                res.append(texte[position:start])
            replace = f'("{texte[start:stop]}", "{category}")'
            res.append(replace)
            position = stop
        res.append(texte[stop:])
        res.append('\n')
    return res[:-1]

    


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


    # print(sample_recognize_to_annotated_text(document))
    print(list_to_dict(document))
    # print(sample_recognize_actions(document))