import streamlit as st
import pandas as pd
import io
import runpod
from IPython.display import display, Markdown
from transformers import (
    pipeline,
    AutoModelForCausalLM,
    AutoTokenizer,
)
from langchain.llms import HuggingFaceTextGenInference

from pdf_processing import load_pdf_text
from answer_logic import get_random_answer

# RUNPOD_API_KEY = "0M5TTL1BIJ"

# runpod.get_gpus()

# pod = runpod.create_pod(
#     name="Meta-Llama-3-8B",
#     image_name="ghcr.io/huggingface/text-generation-inference:0.8",
#     gpu_type_id="NVIDIA A100 80GB PCIe",
#     cloud_type="SECURE",
#     # data_center_id="US-KS-1",
#     docker_args=f"--model-id tiiuae/falcon-40b --num-shard 1",
#     gpu_count=1,
#     volume_in_gb=195,
#     container_disk_in_gb=5,
#     ports="80/http,29500/http",
#     volume_mount_path="/data",
# )

# Set page configuration
st.set_page_config(page_title="CourseQuest 🗺️", page_icon=":books:", layout="wide")

# Main title
st.title("CourseQuest 🗺️")
st.markdown("## Your Interactive Course Catalog Assistant")

# Sidebar for file upload
st.sidebar.header("Upload Course Catalog PDF")
uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf")

# Initialize session state for catalog text
if 'catalog_text' not in st.session_state:
    st.session_state['catalog_text'] = ""

# Load PDF and extract text
if uploaded_file and st.session_state['catalog_text'] == "":
    with st.spinner('Loading PDF...'):
        pdf_stream = io.BytesIO(uploaded_file.read())
        catalog_text = load_pdf_text(pdf_stream)
        st.session_state['catalog_text'] = catalog_text
        st.success('PDF loaded successfully!')

# User question input
st.markdown("### Ask a Question About the Course Catalog")
user_question = st.text_input("Enter your question here:")

# Button to get answer
if st.button("Get Answer"):
    if user_question:
        answer = get_random_answer()
        st.markdown(f"**Question:** {user_question}")
        st.markdown(f"**Answer:** {answer}")
    else:
        st.error("Please enter a question.")