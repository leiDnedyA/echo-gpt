from openai import OpenAI

import os
import dotenv

dotenv.load_dotenv()

client = OpenAI()

def get_openai_response(prompt: str, model="gpt-4o-mini") -> str:
    completion = client.chat.completions.create(
      model=model,
      messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
      ]
    )
    return str(completion.choices[0].message.content)

if __name__ == '__main__':
    print(get_openai_response("What's your favorite color?"))
