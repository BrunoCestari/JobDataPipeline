import openai
import time
from dotenv import dotenv_values

# Load environment variables from .env file
config = dotenv_values(".env")
openai_api_key = config["API_KEY"]

# Set up OpenAI API credentials
openai.api_key = openai_api_key

# Define the job titles
job_titles = ['Data Scientist', 'Data Engineer', 'Machine Learning Engineer']

# Define the prompt to generate tools
prompt = '''
You are a helpful assistant that generates a list of tools likely mentioned in job postings for Data Scientists, Data Engineers, and Machine Learning Engineers.

Generate a list of tools that are commonly mentioned in job descriptions for these roles.
'''

# Set the maximum number of tools to generate
max_tools = 500

# Set batch size and calculate number of batches
batch_size = 3
num_batches = (max_tools + batch_size - 1) // batch_size

# Create an empty list to store tools
tools_list = []

# Iterate over each batch
for batch_num in range(num_batches):
    start_index = batch_num * batch_size
    end_index = min((batch_num + 1) * batch_size, max_tools)
    batch_tools = []

    # Generate tools for the batch
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.7
    )

    # Extract the generated tools from the API response
    generated_tools = response.choices[0].message.content.strip().split('\n')

    # Filter and clean the generated tools
    for tool in generated_tools:
        tool = tool.strip()
        if tool:
            batch_tools.append(tool)

    tools_list.extend(batch_tools)

    # Terminate the loop if the desired number of tools is reached
    if len(tools_list) >= max_tools:
        break

    # Delay between batches to comply with requests per minute limit
    if batch_num < num_batches - 1:
        time.sleep(20)

# Write the tools to the tools.txt file
with open('tools.txt', 'w') as file:
    for tool in tools_list:
        # Remove the numeration before the tool
        tool = tool.split(". ", 1)[-1]
        file.write(f"{tool}\n")

print(f"tools.txt file generated with {len(tools_list)} unique tools.")
