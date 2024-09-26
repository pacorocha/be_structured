import os
import google.generativeai as genai
import requests
from groq import Groq

ollama_model = 'qwen2:1.5b'

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

genai.configure(api_key=os.getenv("GENAI_API_KEY"))


def call_ollama_local(prompt):
    url = "http://localhost:11434/v1/completions"

    data = {
        'model': ollama_model,
        'prompt': prompt
    }

    try:
        response = requests.post(url, json=data)

        if response.status_code == 200:
            return response.json()['choices'][0]['text']
        else:
            return f"Local Ollama API error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Local Ollama connection error: {str(e)}"


def call_groq(prompt):

    try:
        chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192",)

        print(chat_completion.choices[0].message.content)
        return chat_completion.choices[0].message.content

    except Exception as e:
        return f"Groq connection error: {str(e)}"


def call_gemini(prompt):

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini connection error: {str(e)}"


def format_prompt(job_description):
    prompt = f"""
    Analize this job description and extract the information in an structured order:

    Job description:
    {job_description}

    Structure:
    - Name of role
    - Working hours
    - Country
    - Tech skills
    """
    return prompt


def query_all_models(formatted_prompt):
    return {
        "Ollama (local)": call_ollama_local(formatted_prompt),
        "Groc": call_groq(formatted_prompt),
        "Gemini": call_gemini(formatted_prompt)
    }

def main():
    with open("job_description.txt", "r") as file:
        job_description = file.read()

    formatted_prompt = format_prompt(job_description)

    results = query_all_models(formatted_prompt)

    for model, response in results.items():
        print(f"\nAnálise do {model}:")
        print(response)
        print("-" * 50)

if __name__ == "__main__":
    correcting
    main()
