"""
The script makes API requests to the OpenAI API to generate text responses for each prompt in a CSV file.
Here's a step-by-step tutorial on how the script works:
"""

# import necessary libraries
import csv
import requests
API_KEY = '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'

# makefile
# Define the API endpoint URL, the OpenAI model to use, and the name of the column that contains the prompts in the CSV file.
url = "https://api.openai.com/v1/engines/text-davinci-002/jobs"
model = "text-davinci-002"
prompt_column = "prompt"

# css
# Define the API key to be used in the API request in the headers variable:
# Make sure to replace <API_KEY> with your own OpenAI API key.
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer API_KEY'
}

# py
# Define the generate_text function, which makes a POST request to the API endpoint
# with the prompt as input and returns the text response:
def generate_text(prompt):
    data = """
    {
        """
    data += f'"model": "{model}",'
    data += f'"prompt": "{prompt}",'
    data += """
        "max_tokens":2048,
        "temperature":0.5,
        "top_p":1,
        "frequency_penalty":0,
        "presence_penalty":0
    }
    """

    response = requests.post(url, headers=headers, data=data)
    result = response.json()

    return result['choices'][0]['text']

def search_prompt(prompts, search_term):
    search_results = [prompt for prompt in prompts if search_term in prompt[prompt_column]]
    return search_results

def edit_prompt(prompt):
    edited_prompt = input(f"Enter edited prompt (current prompt: {prompt[prompt_column]}): ")
    prompt[prompt_column] = edited_prompt
    return prompt


# py
# Open the CSV file with the prompts using the with open statement and use the csv.DictReader method to read each row as a dictionary.
# For each row in the CSV file, extract the prompt using the row[prompt_column] dictionary access, pass it to the generate_text function,
# and print the prompt and the text response.

# #new
# with open('prompts.csv', encoding='utf-8') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         prompt = row[prompt_column]
#         response = generate_text(prompt)
#         print(prompt)
#         print(response)

# #new/
with open('prompts.csv', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    prompts = list(reader)
    for row in reader:
        prompt = row[prompt_column]
        response = generate_text(prompt)
        print(prompt)
        print(response)

    search_term = input("Enter search term: ")
    search_results = search_prompt(prompts, search_term)

    if not search_results:
        print("No matches found.")
    else:
        for i, result in enumerate(search_results):
            print(f"{i + 1}. {result[prompt_column]}")

        selected_index = int(input("Enter the number of the prompt to generate text for: ")) - 1
        selected_prompt = search_results[selected_index]
        edited_prompt = edit_prompt(selected_prompt)

        response = generate_text(edited_prompt[prompt_column])
        print(f"Prompt: {edited_prompt[prompt_column]}")
        print(f"Response: {response}")
