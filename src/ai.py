from openai import OpenAI

import os
import dotenv

dotenv.load_dotenv()

client = OpenAI()

def get_openai_response(prompt: str, model="gpt-4o-mini", system_prompt=None) -> str:
    completion = client.chat.completions.create(
      model=model,
      messages=[
        {"role": "system", "content": system_prompt if system_prompt else "You are a helpful assistant, with the name \"robot\"."},
        {"role": "user", "content": prompt}
      ]
    )
    return str(completion.choices[0].message.content)



if __name__ == '__main__':
    print(get_openai_response("What's your favorite color?"))
