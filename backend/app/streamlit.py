import streamlit as st
import pandas as pd
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import fitz

# Initialize LLaMA2 model and tokenizer
# model_name = "meta-llama/LLaMA2"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForCausalLM.from_pretrained(model_name)
# qa_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)

st.title("CourseQuest 🐐")

st.sidebar.header("Upload Course Catalog PDF")
uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    # Read the uploaded PDF file
    pdf_reader = fitz.open(uploaded_file)
    num_pages = pdf_reader.numPages
    catalog_text = ""

    # Extract text from each page of the PDF
    for page_num in range(num_pages):
        page = pdf_reader.getPage(page_num)
        catalog_text += page.extractText()

    # Split the extracted text into rows based on newline character
    catalog_rows = catalog_text.split("\n")
    catalog = pd.DataFrame(catalog_rows, columns=["Course Description"])

    st.write("Course Catalog")
    st.dataframe(catalog)

    # User prompt for questions
    user_question = st.text_input("Ask a question about the course catalog:")

    if st.button("Get Answer"):
        if user_question:
            # Generate the context from the course catalog
            context = catalog_text

            # Combine user question with the context
            prompt = f"Context: {context}\n\nQuestion: {user_question}\nAnswer:"

            # Get response from LLaMA2 model
            # response = qa_pipeline(prompt, max_length=500)[0]['generated_text']
            # st.write("Answer:")
            # st.write(response)
        else:
            st.write("Please enter a question.")
