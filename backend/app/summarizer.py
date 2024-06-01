import openai


def summarize_profile(selected_info: dict):
    openai.api_key = "your_openai_api_key"
    prompt = "Summarize the following information: " + str(selected_info)
    response = openai.Completion.create(engine="davinci", prompt=prompt, max_tokens=150)
    summary = response.choices[0].text.strip()
    return summary
