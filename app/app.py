from fastapi import FastAPI
import uvicorn
import os
from utils import load_docs, split_docs, get_answer
from init_setup import *
import pinecone 
from langchain.vectorstores import Pinecone
from pydantic import BaseModel

app = FastAPI(title="PubMed QA", 
              description="Question answering on PubMed articles", version="0.1.0")

@app.get("/")
def main():
    return {"message": "This is a chatbot for PubMed articles."}

class request_body(BaseModel):
    query: str

#load prebuilt pinecone index
@app.on_event("startup")
def get_index():
    global index
    index = Pinecone.from_existing_index(index_name=index_name, embedding=embeddings)

@app.post("/answer/{query}")
def answer(data: request_body):
    query = data.query
    answer = get_answer(index, query)
    return {"answer": answer}