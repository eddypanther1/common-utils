#inspired by Ng's Courera lab
# from helper_functions import print_llm_response, get_llm_response
# from helper_functions get_completion, get_completion_from_messages
# from helper_functions import debugprint

import os
import requests
import json


# needs LLAMA_API_KEY environment variable

BASE_URL = "https://api.llama.com/v1"
URL_REQUEST = "https://api.llama.com/v1/chat/completions"

MODEL = "Llama-4-Maverick-17B-128E-Instruct-FP8"
MODEL3 = "Llama-3.3-70B-Instruct"

API_KEY = os.environ.get('LLAMA_API_KEY')

if not API_KEY:
    raise ValueError("LLAMA_API_KEY environment variable not set.")




#debugprint(str)
import inspect
import re # For parsing the argument string
import sys # Not strictly needed for print, but good for potential stdout interaction


def debugprint(value):
    """
    by Gemini
    Prints the calling expression (or variable name) and its resulting value.
    Handles cases where the argument is an already evaluated expression.
    e.g., debugprint(my_function(x)) will attempt to show 'my_function(x): result_value'
   """
    caller_frame = None
    call_line_info = None
    caller_frame = inspect.currentframe().f_back

    try:
        # Get the source code line where debugprint was called
        call_line_info = inspect.getframeinfo(caller_frame)
        
        arg_text = "unknown_arg" # Default if source parsing fails
        if call_line_info and call_line_info.code_context:
            call_line = call_line_info.code_context[0].strip()
            # Attempt to extract the argument passed to debugprint
            # This regex tries to capture everything inside the outermost parentheses of debugprint()
                        # Using a non-greedy match (.*?) to correctly capture arguments even with trailing comments.
            match = re.search(r"debugprint\s*\((.*?)\)", call_line)
            if match:
                arg_text = match.group(1).strip()
        
        # The 'value' is already the evaluated result of 'arg_text'
        # The request "print a number in addition to a string" means the value
        # itself can be a number or a string, which is handled by printing 'value'.
        # Using !r for repr() to show quotes for strings, etc., which is good for debugging.
        print(f"{arg_text}): {value!r}")
    except Exception as e:
        # Fallback in case of any error during inspection or printing
        print(f"debugprint_error_value: {value!r} (Error during inspection: {e})")
    finally:
        del caller_frame # Avoid potential reference cycles
        if call_line_info:
            del call_line_info




def print_json_response(prompt):
    response=get_json_response(prompt)
    print(json.dumps(response, indent=4, ensure_ascii=False))

def get_json_response(prompt):
    """
    Given a prompt, print the response from the LLM API in a formatted way.
    """
    response = post_request(prompt, URL_REQUEST, MODEL, API_KEY)

    #print("--------json.dumps(response, indent=4, ensure_ascii=False)")  # Note: 'response' is not defined in this function's scope
    #print(json.dumps(response, indent=4, ensure_ascii=False))

    return response

def get_llm_response(prompt):
    response = post_request(prompt, URL_REQUEST, MODEL, API_KEY)
    response_data = response.json()
    try:
        text_content = response_data['completion_message']['content']['text']
        # print(f"{text_content}")
    
    except KeyError:
        print("Key 'text' or 'tool_calls' not found in 'completion_message'.")
    return text_content  

def get_completion(prompt, model="gpt-3.5-turbo"):
    #ignores the model parameter; placeholder for compatibility
    return get_llm_response(prompt)

def get_completion_from_messages(messages, model=MODEL3, temperature=0):
    from openai import OpenAI

    client=OpenAI(
        api_key=API_KEY,
        base_url=BASE_URL,  
    )    
    response = client.chat.completions.create(
        model=MODEL3,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    
    text=response.completion_message['content']['text']
    # double quote works too
    # text=response.completion_message["content"]["text"]
    # but this from Ng's course did not
    # return response.choices[0].message["content"]
    return text

def get_full_response_fromcompletion(messages, model=MODEL3, temperature=0):
    from openai import OpenAI

    client=OpenAI(
        api_key=API_KEY,
        base_url=BASE_URL,  
    )    
    response = client.chat.completions.create(
        model=MODEL3,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    
    return response

def print_llm_response(prompt):
    text_content=get_llm_response(prompt)

    return text_content  

def post_request(prompt, url_request, model, api_key):
    """
    Post a request to the LLM API and return A JSON response.
    """

    response = requests.post(
        url=url_request,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"  # This 'api_key' is the function parameter
        },
        json={
            "model": model,  # This 'model' is the function parameter
            "messages": [
                {"role": "user",
                 "content": prompt}
             ]
            }
        )

    # DEBUG MESSAGE
    """
    if response.status_code == 200:
        response_data = response.json()

        role = response_data['completion_message']['role']
 print(f"The role is: {role}")

        try:
            text_content = response_data['completion_message']['content']['text']
 print(f"The 'text' content is: {text_content}")

            tool_calls = response_data['completion_message']['tool_calls']['function']['name']
 print(f"The 'tool calls' name is: {tool_calls}")

        except KeyError:
            print("Key 'text' or 'tool_calls' not found in 'completion_message'.")


        print(f"--------json.dumps(response_data, indent=4, ensure_ascii=False)") 
        print(json.dumps(response_data, indent=4, ensure_ascii=False))
 else:
        print(f"Error: {response.status_code}")
        print(response.text)
    """

    return response


debugprint((MODEL3))


#Tested functions
# messages =  [  
# {'role':'system', 'content':'You are an assistant that speaks like Shakespeare.'},    
# {'role':'user', 'content':'tell me a joke'},   
# {'role':'assistant', 'content':'Why did the chicken cross the road'},   
# {'role':'user', 'content':'I don\'t know'}  ]

# response = get_completion_from_messages(messages, temperature=1)
# print(response)

# messages =  [  
# {'role':'system', 'content':'You are friendly chatbot.'},    
# {'role':'user', 'content':'Hi, my name is Isa'}  ]
# response = get_completion_from_messages(messages, temperature=1)
# print(response)

# messages =  [  
# {'role':'system', 'content':'You are friendly chatbot.'},    
# {'role':'user', 'content':'Yes,  can you remind me, What is my name?'}  ]
# response = get_completion_from_messages(messages, temperature=1)
# print(response)

# messages =  [  
# {'role':'system', 'content':'You are friendly chatbot.'},
# {'role':'user', 'content':'Hi, my name is Isa'},
# {'role':'assistant', 'content': "Hi Isa! It's nice to meet you. \
# Is there anything I can help you with today?"},
# {'role':'user', 'content':'Yes, you can remind me, What is my name?'}  ]
# response = get_completion_from_messages(messages, temperature=1)
# print(response)