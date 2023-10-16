import urllib.request
import json
import pandas as pd
data = {
        "Inputs": {
                "input1":
                [
                    {
                            'user_id': "383219",  
                            'fi': '0' 
                            #'product_id': "30709",   
                            #'rating': "2",   
                    }
                ],
        },
    "GlobalParameters":  {
    }
}

body = str.encode(json.dumps(data))

url = 'https://ussouthcentral.services.azureml.net/workspaces/9e5845a3789249e78ea17a4756b576c4/services/287523582c2a4bdc840f903dd0eb8f41/execute?api-version=2.0&format=swagger'
api_key = 'kZJBEf54Z6MKK5qoA4X6gjDTjkO6gfWPg1x+JU2FuLaE1Ys1qIy5ReMm1oqTY6Myxo1ZylKkr07n+AMCr88d/w==' # Replace this with the API key for the web service
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

req = urllib.request.Request(url, body, headers)

try:
    response = urllib.request.urlopen(req)
    result = response.read()
    result_json = json.loads(result.decode('utf-8'))

    # Extracting data
    results_list = result_json['Results']['output1']

    # Convert to DataFrame
    df = pd.DataFrame(results_list)

    # Save to CSV
    df.to_csv('output_data.csv', index=False)

except urllib.error.HTTPError as error:
    print(json.loads(error.read().decode("utf8", 'ignore')))