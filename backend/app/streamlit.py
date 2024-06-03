import streamlit as st
import pandas as pd
import fitz
import requests
import os
import runpod
from IPython.display import display, Markdown
from transformers import (
    pipeline,
    AutoModelForCausalLM,
    AutoTokenizer,
)
from langchain.llms import HuggingFaceTextGenInference

RUNPOD_API_KEY = "0M5TTL1BIJWE7CEEXVJQW9WD5IWEGGTNI5IT1TJQ"
RUNPOD_INSTANCE_URL = "YOUR_RUNPOD_INSTANCE_URL"

if RUNPOD_API_KEY == "0M5TTL1BIJWE7CEEXVJQW9WD5IWEGGTNI5IT1TJQ":
    display(
        Markdown(
            "It appears that you don't have a RunPod API key. You can obtain one at [runpod.io](https://runpod.io?ref=s7508tca)"
        )
    )
    raise AssertionError("Missing RunPod API key")

runpod.get_gpus()

pod = runpod.create_pod(
    name="Meta-Llama-3-8B",
    image_name="ghcr.io/huggingface/text-generation-inference:0.8",
    gpu_type_id="NVIDIA A100 80GB PCIe",
    cloud_type="SECURE",
    # data_center_id="US-KS-1",
    docker_args=f"--model-id tiiuae/falcon-40b --num-shard 1",
    gpu_count=1,
    volume_in_gb=195,
    container_disk_in_gb=5,
    ports="80/http,29500/http",
    volume_mount_path="/data",
)

inference_server_url = f'https://{pod["id"]}-80.proxy.runpod.net'
llm = HuggingFaceTextGenInference(
    inference_server_url=inference_server_url,
    max_new_tokens=100,
    top_k=10,
    top_p=0.95,
    typical_p=0.95,
    temperature=0.001,
    repetition_penalty=1.03,
)

# Initialize Hugging Face model and tokenizer with authentication token
model_name = "meta-llama/Meta-Llama-3-8B"
auth_token = "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"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=auth_token)
model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=auth_token)
qa_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)

st.title("CourseQuest 🐐")

st.sidebar.header("Upload Course Catalog PDF")
uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    # Read the uploaded PDF file
    with open(uploaded_file.name, "rb") as f:
        files = {"file": f}
        response = requests.post(
            f"{RUNPOD_INSTANCE_URL}/upload",
            files=files,
            headers={"Authorization": f"Bearer {RUNPOD_API_KEY}"},
        )
        if response.status_code == 200:
            st.write("PDF file uploaded successfully.")
        else:
            st.write("Failed to upload PDF file. Please try again.")

    pdf_reader = fitz.open(uploaded_file)
    num_pages = len(pdf_reader)
    catalog_text = ""

    # Extract text from each page of the PDF
    for page_num in range(num_pages):
        page = pdf_reader[page_num]
        catalog_text += page.get_text()

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

            # Get response from Hugging Face model
            response = qa_pipeline(prompt, max_length=500)[0]["generated_text"]
            st.write("Answer:")
            st.write(response)
        else:
            st.write("Please enter a question.")
