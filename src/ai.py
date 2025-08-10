from openai import OpenAI

import json
import os
from datetime import datetime
import dotenv

from log import log_dict

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


def get_openai_response_with_tools(prompt: str, tools, tool_functions, system_prompt=None):
    response = client.responses.create(
      model="gpt-4o-mini",
      input=[
            {"role": "system", "content": system_prompt if system_prompt else "You are a helpful assistant, with the name \"robot\"."},
            {"role": "user", "content": prompt}
        ],
    tools=tools
    )
    call_results = []
    for item in response.output:
        if item.type == "function_call":
            name = item.name
            function_call_arguments = json.loads(item.arguments)
            if not name in tool_functions:
                print("Warning: function of name " + name + " not provided, but LLM tried to call it.")
                continue
            func = tool_functions[name]
            call_results.append({
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": json.dumps(func(function_call_arguments))
            })
            log_dict({ "event": "tool call", "function_call": item.name, "arguments": function_call_arguments })
    response = client.responses.create(
      model="gpt-4o-mini",
      input = list(response.output) + [
            {"role": "system", "content": system_prompt if system_prompt else "You are a helpful assistant, with the name \"robot\"."},
            {"role": "user", "content": prompt},
        ] + call_results,
      tools=tools
    )
    return response.output_text
    


if __name__ == '__main__':
    def get_weather(argument_dict):
        city = argument_dict["city"]
        if city == "Chicago":
            return "Rainy"
        if city == "New York":
            return "Sunny"
        if city == "London":
            return "Terrible"
        return "Cloudy"
    tools = [
        {
            "type": "function",
            "name": "get_weather",
            "description": "Get today's weather for a specific city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "A city name, such as 'New York' or 'Chicago'",
                    },
                },
                "required": ["city"],
            },
        },
    ]
    tool_functions = {"get_weather": get_weather}
    get_openai_response_with_tools("What's the weather like in Chicago, New York, and Beijing?", tools=tools, tool_functions=tool_functions)
