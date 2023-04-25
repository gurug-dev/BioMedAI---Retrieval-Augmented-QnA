"""Python file to serve as the frontend"""
import streamlit as st
from streamlit_chat import message
import os
from utils import load_docs, split_docs, get_answer
from init_setup import *
import pinecone 
from langchain.vectorstores import Pinecone

global index
index = Pinecone.from_existing_index(index_name=index_name, embedding=embeddings)

# From here down is all the StreamLit UI.
st.set_page_config(page_title="PubMed QA Bot", page_icon=":robot:")
st.header("Ask me a Question, I will try to provide answers based on PubMed articles")

if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []


def get_query():
    input_text = st.text_input("You: ", "What diseases can I ask you about?", key="input")
    return input_text


user_input = get_query()

if user_input:
    answer = get_answer(index, user_input)
    output = f"Answer: {answer}"

    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state["generated"]:

    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")