from sys import stdin, exit
from heypi.client import Client
from heypi.tools import Tools
from heypi.prompt import Prompt


if __name__ == '__main__':
    Tools.debug_flag = False  # Set to True for verbose output

    chatbot = Client()
    conversation = chatbot.create_conversation()

    print('Type "q" to quit')

    while not conversation.is_ended():
        print("\n> ", end='')

        text = input().rstrip()

        if text == 'q':
            break

        prompt = Prompt(text)

        print("- ", end='')

        try:
            def print_tokens(answer, tokens):
                print(tokens, end='')

            full_answer = conversation.ask(prompt, print_tokens)
        except Exception as e:
            print(f"Sorry, something went wrong: {str(e)}.")

    exit(0)
