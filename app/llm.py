from ollama import Client
client = Client(host="http://localhost:11434")

def ask_llm(question: str) -> str:
 response = client.chat(
    model="qwen2.5-coder:7b",
    messages=[
     {
       "role": "user",
       "content": question
     }
    ]
 )
 return response["message"]["content"]