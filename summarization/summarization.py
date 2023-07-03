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


def sample_extractive_summarization(client,document):
    poller = client.begin_extract_summary(document)
    extract_summary_results = poller.result()
    for result in extract_summary_results:
        if result.kind == "ExtractiveSummarization":
            return "\n".join([sentence.text for sentence in result.sentences])
        elif result.is_error is True:
            print("...Is an error with code '{}' and message '{}'".format(
                result.error.code, result.error.message
            ))

def sample_abstractive_summarization(client,document):
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


if __name__ == "__main__":
    
    client = authenticate_client()

    document = [
            "At Microsoft, we have been on a quest to advance AI beyond existing techniques, by taking a more holistic, "
            "human-centric approach to learning and understanding. As Chief Technology Officer of Azure AI Cognitive "
            "Services, I have been working with a team of amazing scientists and engineers to turn this quest into a "
            "reality. In my role, I enjoy a unique perspective in viewing the relationship among three attributes of "
            "human cognition: monolingual text (X), audio or visual sensory signals, (Y) and multilingual (Z). At the "
            "intersection of all three, there's magic-what we call XYZ-code as illustrated in Figure 1-a joint "
            "representation to create more powerful AI that can speak, hear, see, and understand humans better. "
            "We believe XYZ-code will enable us to fulfill our long-term vision: cross-domain transfer learning, "
            "spanning modalities and languages. The goal is to have pretrained models that can jointly learn "
            "representations to support a broad range of downstream AI tasks, much in the way humans do today. "
            "Over the past five years, we have achieved human performance on benchmarks in conversational speech "
            "recognition, machine translation, conversational question answering, machine reading comprehension, "
            "and image captioning. These five breakthroughs provided us with strong signals toward our more ambitious "
            "aspiration to produce a leap in AI capabilities, achieving multisensory and multilingual learning that "
            "is closer in line with how humans learn and understand. I believe the joint XYZ-code is a foundational "
            "component of this aspiration, if grounded with external knowledge sources in the downstream AI tasks."
        ]


    print(sample_abstractive_summarization(client,document))
    print()
    print(sample_extractive_summarization(client,document))