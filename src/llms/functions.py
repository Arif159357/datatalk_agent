from llms.clients import GoogleGenAIClient


model_clients = {
    "google": GoogleGenAIClient(),
}


def call_model(model_name, messages, system_prompt, temperature=0.0, top_p=1.0):
    client = model_clients[model_name]
    return client.call(messages, system_prompt, temperature, top_p)
