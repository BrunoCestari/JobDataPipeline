import pandas as pd
import re
from geopy.geocoders import Nominatim
import sys

try:
    output_name = sys.argv[1]
except Exception as e:
    print(f"Error with file input. Error {e}")
    sys.exit(1)


# Read raw data:

df = pd.read_csv(f"/tmp/{output_name}.csv")

# Read the list of tools from the file
with open('/opt/airflow/extraction/tools.txt', 'r') as file:
    tools = [line.strip() for line in file]

# List of words to exclude from pattern match
exclude_words = ['for', "Language","Business", "Please", "Note", 'example', 'other_word', "Cloud", "Google", "Intelligence", "Data", "Machine", "This", "e.g", "Amazon", "I"]  # Add your personalized words here

# Function to extract tools from job descriptions using Regex
def extract_tools(text):
    pattern = r'\b(?:{})\b'.format('|'.join(map(re.escape, set(tools) - set(exclude_words))))
    tools_list = re.findall(pattern, text)
    return ', '.join(set(tools_list))  # Join the tools into a single string

# Function to extract years of experience from job descriptions using Regex
def extract_experience(text):
    pattern = r'(\d+)\+?\s*(?:years of experience|years\' experience|years of relevant experience|years\' relevant experience)'
    experience_list = re.findall(pattern, text, flags=re.IGNORECASE)
    
    # Add pattern for Portuguese
    pattern_pt = r'(\d+)\+?\s*(?:anos de experiência|anos de experiência relevantes)'
    experience_list_pt = re.findall(pattern_pt, text, flags=re.IGNORECASE)
    
    # Combine English and Portuguese results
    experience_list.extend(experience_list_pt)
    
    return list(set(experience_list))  # Return unique years of experience






def update_remote_value(df, city_column):
    df.loc[df[city_column] == "Qualquer lugar", city_column] = "Remote"
    return df

update_remote_value(df, "Remote")

# Extract tools from job descriptions
df['Tools'] = df['Job_Description'].apply(extract_tools)

# Extract years of experience from job descriptions
df['Years_of_Experience'] = df['Job_Description'].apply(extract_experience)


# Save the updated df
df.to_csv(f'/tmp/{output_name}.csv', index=False)
