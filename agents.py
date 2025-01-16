from langchain.chains.llm import LLMChain
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAI
from config import Config

#Your output must be only JSON, without additional markers such as triple quotes (''') or backticks (```).
class Screener:
    def __init__(self, openai_key, base_url):
        self.openai_key = openai_key
        self.base_url = base_url
        self.screener_prompt = """
        You are an arbiter responsible for screening a user's emails. You will decide if the content of an email is important or not.

        An email is considered important if:
        - The subject line or content relates to jobs
        - The subject line or content is something personal to the user
        - The subject line or content relates to the user's bank accounts
        - The subject line or content relates to an e-Commerce order

        You will receive a list of items. Each item of the list is an email as a structured JSON with the keys "From", "Subject" and "Content". 
        
        Evaluate each item in the list and add a new key "Important". If the email is considered important, set its value to "Y" or "N" if it is not important. Return only the modified list of items and nothing else.
        If you are unable to evaluate the input as per these instructions, respond with "Failed to screen".

        List:
        {emails}
        """

    def screen_emails(self, emails):
        prompt = PromptTemplate(template=self.screener_prompt, input_variables=["emails"])
        # Add logger statement

        llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=self.openai_key)

        llm_screener_chain = prompt | llm | StrOutputParser()

        screener_response = llm_screener_chain.invoke(emails)

        return screener_response

class Summarizer:
    def __init__(self, openai_key, base_url):
        self.openai_key = openai_key
        self.base_url = base_url
        self.summarizer_prompt = """
        You are a personal assistant that excels at summarizing important emails. You will receive a list of emails and your task is to summarize them.

        You will receive a list of items. Each item of the list is an email as a structured JSON with the keys "From", "Subject" and "Content". 
        
        Read the "Content" key's value of each item in the list and make a brief summary with a maximum limit of 20 words. The summary must be crisp and straight to the point. Do not furnish your response with irrelevant or unnecessary information.
        Return a list of the summarized content, with each summary as an item of this list. If you are unable to do this, return an empty list.

        List:
        {emails}
        """
    
    def summarize_emails(self, emails):
        prompt = PromptTemplate(template=self.summarizer_prompt, input_variables=["emails"])
        # Add logger statement

        llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=self.openai_key)
        llm_summarizer_chain = prompt | llm | StrOutputParser()

        summarizer_response = llm_summarizer_chain.invoke(emails)

        return summarizer_response