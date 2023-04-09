import os
import openai #remember to pip install pandas openai
from dotenv import load_dotenv  #remember to pip install python-dotenv
load_dotenv()

#Sign up for OpenAI here https://beta.openai.com/signup
# and obtain an API key from here https://platform.openai.com/account/api-keys
#Replace the OPEN_API_KEY below with your own key:
openai.api_key = "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"


#If you are using Anaconda Spyder, make sure it is updated to version 5.3.3
# or later
# from the Anaconda prompt, type 2 commands
#  conda update anaconda
#  conda install spyder=5.3.3d

def generate_response(prompt):
    # More details about the different engines here
    #  https://beta.openai.com/docs/models/gpt-3
    model_engine = "text-davinci-003"  # https://platform.openai.com/docs/models/overview
    prompt = (f"{prompt}")

    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=1,
    )

    message = completions.choices[0].text
    return message.strip()

while (True):
    prompt = input("\nEnter your question (or type 'quitme' to quit): \n")
    if(prompt == 'quitme'):
        break
    response = generate_response(prompt)
    print("\n" + response)



"""
GPT-3.5
GPT-3.5 models can understand and generate natural language or code. Our most capable and cost effective model in the GPT-3.5 family is gpt-3.5-turbo which has been optimized for chat but works well for traditional completions tasks as well.

LATEST MODEL	DESCRIPTION	MAX TOKENS	TRAINING DATA
gpt-3.5-turbo	Most capable GPT-3.5 model and optimized for chat at 1/10th the cost of text-davinci-003. Will be updated with our latest model iteration.	4,096 tokens	Up to Sep 2021
gpt-3.5-turbo-0301	Snapshot of gpt-3.5-turbo from March 1st 2023. Unlike gpt-3.5-turbo, this model will not receive updates, and will only be supported for a three month period ending on June 1st 2023.	4,096 tokens	Up to Sep 2021
text-davinci-003	Can do any language task with better quality, longer output, and consistent instruction-following than the curie, babbage, or ada models. Also supports inserting completions within text.	4,097 tokens	Up to Jun 2021
text-davinci-002	Similar capabilities to text-davinci-003 but trained with supervised fine-tuning instead of reinforcement learning	4,097 tokens	Up to Jun 2021
code-davinci-002	Optimized for code-completion tasks	8,001 tokens	Up to Jun 2021
We recommend using gpt-3.5-turbo over the other GPT-3.5 models because of its lower cost.
"""

