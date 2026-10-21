import streamlit as st
import anthropic

def get_client():
    return anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

MODEL = "claude-3-haiku-20240307"
