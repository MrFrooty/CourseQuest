import json
from transformers import pipeline

# Load the fine-tuned model and tokenizer
qa_pipeline = pipeline(
    "question-answering", model="./fine_tuned_model", tokenizer="./fine_tuned_model"
)

# Example questions to evaluate
questions = [
    {
        "question": "What are the prerequisites for CPLT 042W?",
        "context": "CPLT 042W Responses to Political Repression in Modern Chinese Literature and Film 4 Lecture, 3 hours; discussion, 1 hour; written work, 3 hours. Prerequisite(s): ENGL 001B with a grade of C or better. An examination of the various responses to political repression in China during the second half of the twentieth century through selected literary and artistic representations. Fulfills the third-quarter writing requirement for students who earn a grade of “C” or better for courses that the Academic Senate designates, and that the student’s college permits, as alternatives to English 001C. Cross-listed with AST 046W, and CHN 046W. Credit is awarded for one of the following CHN 046W, AST 046W, CPLT 042W, AST 046, CHN 046, or CPLT 042.",
    },
    {
        "question": "What is CPLT 042W cross-listed with?",
        "context": "CPLT 042W Responses to Political Repression in Modern Chinese Literature and Film 4 Lecture, 3 hours; discussion, 1 hour; written work, 3 hours. Prerequisite(s): ENGL 001B with a grade of C or better. An examination of the various responses to political repression in China during the second half of the twentieth century through selected literary and artistic representations. Fulfills the third-quarter writing requirement for students who earn a grade of “C” or better for courses that the Academic Senate designates, and that the student’s college permits, as alternatives to English 001C. Cross-listed with AST 046W, and CHN 046W. Credit is awarded for one of the following CHN 046W, AST 046W, CPLT 042W, AST 046, CHN 046, or CPLT 042.",
    },
]

# Evaluate the model
for q in questions:
    result = qa_pipeline(question=q["question"], context=q["context"])
    print(f"Question: {q['question']}")
    print(f"Answer: {result['answer']}")
