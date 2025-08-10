
from src.ai import get_openai_response_with_tools
from src.tools.launch_media import tools as launch_media_tools
from src.tools.launch_media import tool_functions as launch_media_tool_functions


def launch_show_from_prompt():
    prompt = "Please put on Regular Show for me."
    response = get_openai_response_with_tools(
        prompt=prompt,
        tools=launch_media_tools,
        tool_functions=launch_media_tool_functions
    )
    print(response)

def answer_simple_question():
    prompt = "What did Oppenheimer like to do for fun?"

tests = [launch_show_from_prompt, answer_simple_question]

if __name__ == '__main__':
    results = {}
    for test in tests:
        test_name = test.__name__
        try:
            test()
            results[test_name] = True
        except Exception as e:
            results[test_name] = e
    for result in results:
        print(result + ": " + ("passed" if results[result] == True else "failed"))
        if results[result] != True:
            print("\tWith error: ", results[result])
