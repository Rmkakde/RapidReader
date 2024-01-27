from dotenv import load_dotenv
import streamlit as st
import os
import fitz 
import google.generativeai as genai

# It will Load environment variables
load_dotenv()

# Configureing API Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get Gemini response for summarizing and highlighting key points
def get_gemini_summary(pdf_text, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([pdf_text, prompt])
    return response['text']

# This Function will extract text from PDF
def extract_text_from_pdf(uploaded_file):
    if uploaded_file is not None:
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        pdf_text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            pdf_text += page.get_text()

        return pdf_text
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit Interface
st.set_page_config(page_title="RapidReader")
st.header("RapidReader")

uploaded_file = st.file_uploader("Upload your PDF...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit = st.button("Summarize and Highlight Key Points")

input_prompt = """
You are a summarization expert tasked with providing a concise summary and highlighting key points of the given PDF. 
Please analyze the document and extract the most important information for quick understanding.
"""

if submit:
    if uploaded_file is not None:
        pdf_text = extract_text_from_pdf(uploaded_file)
        response = get_gemini_summary(pdf_text, input_prompt)
        
        st.subheader("Summary and Key Points")
        st.write(response)
    else:
        st.write("Please upload the PDF")