from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

class llmPipeline():
    def __init__(self, model="gemini-2.5-flash", prompt_template="ask user for prompt in one sentence"):
        self.llm = ChatGoogleGenerativeAI(model=model)
        self.prompt = ChatPromptTemplate.from_template(prompt_template)
        self.chain = self.prompt | self.llm | StrOutputParser()

    def invoke(self, input_dict={}):
        try:
            response = self.chain.invoke(input_dict)
            return response
        except Exception as e:
            return f"API Test Failed. Ensure the GOOGLE_API_KEY is correctly set in your .env file. Error: {e}"
        

if __name__ == "__main__":
    pipeline = llmPipeline()
    result = pipeline.invoke({"input": "how are you?"})
    print(result)