import argparse
from src.ai import get_openai_response, get_openai_response_with_tools
from src.tts import tts 
from src.stt import await_speech_command, stt_from_mic, init_mic
from src.log import log_dict, set_stdout
from src.tools.launch_media import tools as launch_media_tools
from src.tools.launch_media import tool_functions as launch_media_tool_functions

def init_cli():
    tools = launch_media_tools
    tool_functions = launch_media_tool_functions
    messages = []
    def callback():
        prompt = input("> ")
        if prompt == "exit":
            print("Goodbye :/")
            exit(0)
        response = get_openai_response_with_tools(
            prompt,
            tools=tools,
            tool_functions=tool_functions,
            previous_messages=messages
        )
        messages.append({"role": "user", "content": prompt})
        messages.append({"role": "assistant", "content": response})
        log_dict({"prompt": prompt, "response": response})
        print("----------\n" + response)
    print("What's up?")
    while True:
        callback()

def init_voice():
    set_stdout(True)
    def callback():
        tts("What's up?")
        prompt = stt_from_mic(10)
        response = get_openai_response(prompt)
        log_dict({"prompt": prompt, "response": response})
        tts(response)
        exit(0)

    init_mic()
    tts("Say, \"Hey, robot\", wait for my response, and then ask a question.")

    await_speech_command(callback)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='NLControl',
        description="Can take actions on a user's behalf based on natural-language commands.",
    )
    parser.add_argument('--cli', action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    if args.cli:
        init_cli()
    else:
        init_voice()

