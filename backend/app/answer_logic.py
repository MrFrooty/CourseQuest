# from IPython.display import display, Markdown
# from transformers import (
#     pipeline,
#     AutoModelForCausalLM,
#     AutoTokenizer,
# )
# from langchain.llms import HuggingFaceTextGenInference

# model_name = "google-bert/bert-large-cased"
# auth_token = "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"
# tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=auth_token)
# model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=auth_token)
# qa_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)

import random

def get_random_answer():
    answers = ["Yes", "No", "Maybe"]
    return random.choice(answers)