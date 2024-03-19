import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from io import StringIO


def send_data(data_dict, form_id):
    """
    Submits data to a Google Form.
    
    Parameters:
        data_dict (dict): A dictionary containing form data where keys are form item names and values are corresponding data.
        form_id (str): The ID of the Google Form to which the data will be submitted.
        
    Returns:
        bool: True if the data was successfully submitted, False otherwise.
    """

    # Define the URLs for viewing and submitting the Google Form.
    view_form_url = f'https://docs.google.com/forms/d/e/{form_id}/viewform'
    post_form_url = f'https://docs.google.com/forms/d/e/{form_id}/formResponse'

    # Fetch the content of the view form page and extract the form data structure.
    page = requests.get(view_form_url)
    content = BeautifulSoup(page.content, "html.parser").find('script', type='text/javascript')
    content = content.text[27:-1]
    result = json.loads(content)[1][1]
    form_dict = {}
    
    # Prepare the data to be submitted to the Google Form.
    for item in result:
        if item[1] in data_dict:
            form_dict[f'entry.{item[4][0][0]}'] = data_dict[item[1]]
    
    # Submit the data to the Google Form using a POST request.
    post_result = requests.post(post_form_url, data=form_dict)
    return post_result.ok

def get_data(data_keys, sheet_id):
    """
    Fetches specified columns from a public Google Sheets document and returns the data as a list of lists.
    
    Parameters:
        data_keys (list of str): A list of strings representing the column names to retrieve.
        sheet_id (str): The unique identifier of the Google Sheets document.
    
    Returns:
        data_list (list of lists): A list where each sublist contains all the values from one of the specified columns.
    """
    
    # Initialize an empty list to store data from each specified column
    data_dict = {}
        
    # Define the URLs for viewing the Google Form.
    view_sheet_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv'

    # Fetch CSV and load into DataFrame
    response = requests.get(view_sheet_url)
    data = pd.read_csv(StringIO(response.text))
    
    # Save DataFrame to CSV
    csv_path = './Data/output.csv'
    data.to_csv(csv_path, index=False)
    
    # Read CSV back into DataFrame
    df = pd.read_csv(csv_path)
    
    # Extract data for each specified column
    for key in data_keys:
        key_list = df[key].dropna().tolist()
        data_dict[key] = key_list
    
    return data_dict