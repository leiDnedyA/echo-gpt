from openai import OpenAI

client = OpenAI()

def get_openai_response(prompt: str, model="gpt-4o-mini") -> str:
    completion = client.chat.completions.create(
      model=model,
      messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
      ]
    )
    print(completion.choices[0].message.content)
    return str(completion.choices[0].message.content)
