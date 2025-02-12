
import requests

def getResponse(user_input):
    headers = {"Content-Type": "application/json"}
    base_url = "https://6efe-35-186-188-51.ngrok-free.app"  
    endpoint = f"{base_url}/generate"
    response = requests.post(endpoint, headers=headers, json={
        "inputs": "\n\n### Instructions:\n" + user_input + "\n\n### Response:\n",  
        "parameters": {"stop": ["\n", "###"]}  
    })

    print("Raw response:", response.text)  

    return response.json()
    