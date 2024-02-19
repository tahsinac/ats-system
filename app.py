import streamlit as st
from langchain.llms import OpenAI
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv() ## load all our environment variables

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def get_gpt_repsonse(input):
    model=OpenAI(openai_api_key=OPENAI_API_KEY,temperature=0.5)
    return model.invoke(input)

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template

input_prompt="""
Imagine you are an advanced Application Tracking System (ATS) specializing in the tech industry, particularly in software engineering, data science, data analysis, and machine learning engineering. Your task is to meticulously assess a given resume in relation to a provided job description.
Given the highly competitive job market, it's crucial to deliver a nuanced evaluation.
More the skills and relevant experience a resume has when compared to the job description, the higher the score.
**Resume:**
{text}

**Job Description:**
{jd}

Provide the response in a single string with the following structure:
{{"Job Description Match": "%", "Reasoning": "", "Missing Keywords": [], "Advice": ""}}

Pay special attention to accuracy. A high accuracy score should only be assigned if the resume is genuinely a good fit for the job description. If the roles are distinct, make sure the model understands that and accurately identifies missing keywords.
"""


## streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd=st.text_area("Paste the Job Description")
text=st.text_area("Paste resume here")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please upload the pdf")

submit = st.button("Submit")

if submit:
    response=get_gpt_repsonse(input_prompt)
    st.subheader(response)
    # if uploaded_file is not None:
    #     text=input_pdf_text(uploaded_file)
    #     response=get_gpt_repsonse(input_prompt)
    #     st.subheader(response)