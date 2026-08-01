import streamlit as st
from langchain_openai import ChatOpenAI

class OpenAILLM:
    def __init__(self, user_controls_input):
        self.user_controls_input= user_controls_input
    
    def get_llm_model(self):
        try:
            openai_api_key=self.user_controls_input["OPENAI_API_KEY"]
            selected_openai_model=self.user_controls_input["selected_model"]
            if not openai_api_key:
                st.error("Please enter your OpenAI API key")
                st.stop()
            llm=ChatOpenAI(api_key=openai_api_key,model=selected_openai_model)
            return llm
        except Exception as e:
            raise ValueError(f"Error Initializing OpenAI LLM:{e}")