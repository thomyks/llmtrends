import openai
from config.settings import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def call_gpt_api(prompt):
    """Calls GPT-40 API to validate topic labels."""
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"].strip()

def validate_or_generate_topic(topic_name, paper_data, force_new_topic=False):
    """Uses GPT-40 to validate or generate new topic labels."""
    action = "validate" if not force_new_topic else "generate a new topic label"
    prompt = f"""
    You are an expert in machine learning and academic research. Your task is to {action} whether a research paper belongs to a specific topic.

    Topic: {topic_name}
    Paper Title: {paper_data["title"]}
    Abstract: {paper_data["abstract"]}

    Return either:
    - "Topic Validated: {topic_name}"
    - "LLM Domain - Topic Needs Review"
    - "The document does not belong to the topic nor the LLM domain."
    """
    return call_gpt_api(prompt)
