from langchain_chroma import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)
from datetime import date
from langchain_openai import ChatOpenAI
import os
import json
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_KEY')

class Item(BaseModel):
    query: str

app = FastAPI()

origins = ["*"]  # This allows all origins, you can restrict this to specific origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

embeddings = OpenAIEmbeddings(api_key=OPENAI_KEY)
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

example_selector = SemanticSimilarityExampleSelector(
    vectorstore=vectorstore,
    k=3,
)

# Define the few-shot prompt.
few_shot_prompt = FewShotChatMessagePromptTemplate(
    # The input variables select the values to pass to the example_selector
    input_variables=["input"],
    example_selector=example_selector,
    # Define how each example will be formatted.
    # In this case, each example will become 2 messages:
    # 1 human, and 1 AI
    example_prompt=ChatPromptTemplate.from_messages(
        [("human", "{input}"), ("ai", "{output}")]
    ),
)


# Final prompt template
today = date.today()
d1 = today.strftime("%d/%m/%Y")

final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system","You're a brilliant data sorcerer. Your task is to generate responses based on examples. Your responses should adhere to the patterns observed in the examples provided. Note that today's date is " + str(d1) + "."+"Should an inquiry pertain to showcasing or producing data for the preceding 7 days, last week, last quarter, or akin durations, ensure adept substitution of accurate dates within the parameters of start_date and end_date."),
        few_shot_prompt,
        ("human", "{input}"),
    ]
)

#chain = final_prompt | ChatOpenAI(openai_api_key=OPENAI_KEY, model = 'gpt-3.5-turbo-0125', temperature=0.0)
#chain.invoke({"input": "  I want to refresh all our records from the electronic health records, what steps are involved? "}).content

@app.post("/run/")
async def run(item: Item):
    chain = final_prompt | ChatOpenAI(openai_api_key=OPENAI_KEY, model = 'gpt-3.5-turbo-0125', temperature=0.0)
    llm_output = chain.invoke({"input": item.query}).content
    try:
        results = json.loads(llm_output)
    except:
        results = {"error" : llm_output}
    return results

