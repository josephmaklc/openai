from openai import OpenAI
from dotenv import load_dotenv
import os

# See here for much more https://github.com/openai/openai-python

# Load environment variables using dotenv
# pip install python-dotenv
#
# In .env file, store
# OPENAI_API_KEY=<your open api key>

load_dotenv()
model="gpt-5-nano"

client = OpenAI(
      api_key=os.getenv("OPENAI_API_KEY"),
)

# Chat completion: Requires the client application to manage the conversation history by sending the full message history with 
# each new request to maintain context. It is inherently stateless from the API's perspective.

def chatCompletion(prompt, systemrole, maxToken=2000, outputs=1):
    
    # In Chat Completions, the primary roles are system, user, and assistant.  
    response = client.chat.completions.create(
        model=model,
        messages=[
			{"role": "system", "content": systemrole},
			{"role": "user", "content": prompt}
			],

        max_completion_tokens=maxToken,
        # number of outputs generated in one call
        n=outputs
    )
    #print("response")
    #print(response)
    #print("\n\n")
    # creating a list to store all the outputs
    output = list()
    for k in response.choices:
        output.append(k.message.content.strip())
    return output

#print(chatCompletion("what is your name","You talk like shakespeare"))

#-----------------------------------------------------------------------------
# Response API: A newer, more comprehensive API designed to unify and simplify interactions, including features from the previous Assistants API. 
def getResponseText(prompt,instructions=""):
	response = client.responses.create(
	    model=model,
	    input=prompt,
	    instructions=instructions
	)
	return response.output_text

#print(getResponseText("what is your name",instructions="You talk like Shakespeare"))
#print(getResponseText(input("What do you to ask OpenAPI? ")))

#-------------------------------------------------------------------------------------------------------------------------
# responses with context from previous questions

question=input("what's your first question for OpenAI? ") #Try "WHat's the capital for France"
#print(question) 

context = [
    { "role": "user", "content": question }
]

res1 = client.responses.create(
    model=model,
    input=context,
)
print(res1.output_text)
# Append the first response’s output to context
context += res1.output

question2=input("what's your follow up question for OpenAI? ") #Try "and its population?"

# Add the next user message
context += [
    { "role": "user", "content": question2 }
]

res2 = client.responses.create(
    model=model,
    input=context,
)
print(res2.output_text)


