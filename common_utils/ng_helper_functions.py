from openai import AzureOpenAI, DefaultHttpxClient

import ipywidgets as widgets
from IPython.display import display
import io
import os

client = AzureOpenAI(
    api_key="abcdefg",
    api_version="2024-02-01",
    azure_endpoint = "https://cour-external-playground.openai.azure.com/",
    http_client=DefaultHttpxClient(verify=False)
    )


# +
#

# ### If you want to use your own OpenAI key, uncomment these lines below

# from openai import OpenAI

# ### Add your key as a string
# openai_api_key = "Add your key in here"

# # Set up the OpenAI client
# client = OpenAI(api_key=openai_api_key)

#
# -

def print_llm_response(prompt):
    """This function takes as input a prompt, which must be a string enclosed in quotation marks,
    and passes it to OpenAI's GPT 4o-mini model. The function then prints the response of the model.
    """
    try:
        if not isinstance(prompt, str):
            raise ValueError("Input must be a string enclosed in quotes.")
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful but terse AI assistant who gets straight to the point.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
        )
        response = completion.choices[0].message.content
        print(response)
    except TypeError as e:
        print("Error:", str(e))


def upload_txt_file():
    """
    Uploads a text file and saves it to the specified directory.
    
    Args:
        directory (str): The directory where the uploaded file will be saved. 
        Defaults to the current working directory.
    """
    # Create the file upload widget
    upload_widget = widgets.FileUpload(
        accept='.txt',  # Accept text files only
        multiple=False  # Do not allow multiple uploads
    )
    # Impose file size limit
    output = widgets.Output()
    
    # Function to handle file upload
    def handle_upload(change):
        with output:
            output.clear_output()
            # Read the file content
            content = upload_widget.value[0]['content']
            name = upload_widget.value[0]['name']
            size_in_kb = len(content) / 1024
            
            if size_in_kb > 3:
                print(f"Your file is too large, please upload a file that doesn't exceed 3KB.")
                return
		    
            # Save the file to the specified directory
            with open(name, 'wb') as f:
                f.write(content)
            # Confirm the file has been saved
            print(f"The {name} file has been uploaded.")

    # Attach the file upload event to the handler function
    upload_widget.observe(handle_upload, names='value')

    display(upload_widget, output)

def list_files_in_directory(directory='.'):
    """
    Lists all non-hidden files in the specified directory.
    
    Args:
        directory (str): The directory to list files from. Defaults to the current working directory.
    """
    try:
        files = [f for f in os.listdir(directory) if (not f.startswith('.') and not f.startswith('_'))]
        for file in files:
            print(file)
    except Exception as e:
        print(f"An error occurred: {e}")