
# response_agent.py

from vertexai import generative_models
from vertexai.generative_models import GenerationConfig, GenerativeModel


model = GenerativeModel(
    "gemini-2.0-flash-exp",
    system_instruction=[
        "You are a helpful, knowledgeable, and human-like assistant.",
        "Generate a clear, concise, and fluent response in natural language based on the query and relevant chunks.",
        "Ensure the response is coherent, well-structured, and easy to understand.",
    ]
)

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
}

def generate_response(query, combined_input):
    response = model.generate_content(
        combined_input,
        generation_config=generation_config,
        safety_settings=safety_settings
    )
    return response.text

