import argparse
from flask import Flask, request, redirect, url_for, render_template_string
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

def init_web(host: str = "0.0.0.0", port: int = 5000):
    tools = launch_media_tools
    tool_functions = launch_media_tool_functions
    messages = []

    app = Flask(__name__)

    PAGE_TEMPLATE = """
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>Echo GPT - Chat</title>
      <style>
        body { font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; margin: 2rem; }
        .chat { max-width: 720px; margin: 0 auto; }
        .msg { padding: 0.75rem 1rem; border-radius: 10px; margin: 0.5rem 0; }
        .user { background: #e6f0ff; }
        .assistant { background: #f3f4f6; }
        .role { font-weight: 600; margin-right: 0.5rem; }
        form { display: flex; gap: 0.5rem; margin-top: 1rem; }
        input[type=text] { flex: 1; padding: 0.75rem 1rem; border: 1px solid #d1d5db; border-radius: 8px; }
        button { padding: 0.75rem 1rem; border: none; border-radius: 8px; background: #2563eb; color: white; cursor: pointer; }
        button:hover { background: #1d4ed8; }
      </style>
    </head>
    <body>
      <div class="chat">
        <h2>Echo GPT</h2>
        {% if messages %}
        <div>
          {% for m in messages %}
            <div class="msg {{ m.role }}">
              <span class="role">{{ m.role.title() }}:</span>
              <span class="content">{{ m.content }}</span>
            </div>
          {% endfor %}
        </div>
        {% else %}
          <p>No messages yet. Say hi!</p>
        {% endif %}
        <form method="post" action="{{ url_for('send_message') }}">
          <input type="text" name="message" placeholder="Type your message..." autofocus required />
          <button type="submit">Send</button>
        </form>
      </div>
    </body>
    </html>
    """

    @app.get("/")
    def index():
        return render_template_string(PAGE_TEMPLATE, messages=messages)

    @app.post("/send")
    def send_message():
        prompt = (request.form.get("message") or "").strip()
        if prompt:
            response = get_openai_response_with_tools(
                prompt=prompt,
                tools=tools,
                tool_functions=tool_functions,
                previous_messages=messages,
            )
            messages.append({"role": "user", "content": prompt})
            messages.append({"role": "assistant", "content": response})
            log_dict({"prompt": prompt, "response": response, "mode": "web"})
        return redirect(url_for("index"))

    print(f"Starting web UI on http://{host}:{port}")
    app.run(host=host, port=port, debug=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='NLControl',
        description="Can take actions on a user's behalf based on natural-language commands.",
    )
    parser.add_argument('--cli', action=argparse.BooleanOptionalAction)
    parser.add_argument('--web', action=argparse.BooleanOptionalAction, help='Start a simple web chat UI')
    args = parser.parse_args()
    if getattr(args, 'web', False):
        init_web()
    elif args.cli:
        init_cli()
    else:
        init_voice()

