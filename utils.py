from init_setup import *
from langchain.document_loaders import DirectoryLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_docs(directory):
  documents = []

  pdf_loader = DirectoryLoader(directory, glob="*.pdf")
  documents.extend(pdf_loader.load())

  loader = DirectoryLoader(directory, glob="*.csv", loader_cls=CSVLoader)
  documents.extend(loader.load())

  return documents

def split_docs(documents,chunk_size=1000,chunk_overlap=20):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
  docs = text_splitter.split_documents(documents)
  return docs

def get_similiar_docs(index, query,k=2,score=False):
  if score:
    similar_docs = index.similarity_search_with_score(query,k=k)
  else:
    similar_docs = index.similarity_search(query,k=k)
  return similar_docs

def get_answer(index, query):
  similar_docs = get_similiar_docs(index, query)
  # print(similar_docs)
  answer =  chain.run(input_documents=similar_docs, question=query)
  return  answer