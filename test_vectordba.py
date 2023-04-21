import os
os.environ["OPENAI_API_KEY"] = "OPEN AI API KEY"
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import openai
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone 
from langchain.vectorstores import Pinecone
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain

directory = "docs"

def load_docs(directory):
  loader = DirectoryLoader(directory)
  documents = loader.load()
  return documents

documents = load_docs(directory)
len(documents)


def split_docs(documents,chunk_size=1000,chunk_overlap=20):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
  docs = text_splitter.split_documents(documents)
  return docs

docs = split_docs(documents)
print(len(docs))

embeddings = OpenAIEmbeddings()

query_result = embeddings.embed_query("Hello world")
len(query_result)


# initialize pinecone
pinecone.init(
    api_key="PINECONE API KEY",  # find at app.pinecone.io
    environment="PINECONE ENV"  # next to api key in console
)

index_name = "langchain-demo"
pinecone.create_index(index_name, dimension=1536,
                          metric="cosine", pods=1, pod_type="p1.x1")

index = Pinecone.from_documents(docs, embeddings, index_name=index_name)

def get_similiar_docs(query,k=2,score=False):
  if score:
    similar_docs = index.similarity_search_with_score(query,k=k)
  else:
    similar_docs = index.similarity_search(query,k=k)
  return similar_docs

# query = "How to compute sample size?"  
# similar_docs = get_similiar_docs(query)
# similar_docs



# model_name = "text-davinci-003"
model_name = "gpt-3.5-turbo"
# model_name = "gpt-4"
llm = OpenAI(model_name=model_name)

chain = load_qa_chain(llm, chain_type="stuff")

def get_answer(query):
  similar_docs = get_similiar_docs(query)
  # print(similar_docs)
  answer =  chain.run(input_documents=similar_docs, question=query)
  return  answer

query = "How to compute sample size?"  
get_answer(query)
