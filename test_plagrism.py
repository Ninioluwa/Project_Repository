import requests
import os
from dotenv import load_dotenv


load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

data = {
    "grant_type": "client_credentials",
    "client_id": os.getenv("UNICHECK_CLIENT_ID"),
    "client_secret": os.getenv("UNICHECK_CLIENT_SECRET")
}

user_details = requests.post(
    "https://api.unicheck.com/oauth/access-token", data=data).json()

print(user_details)

api_token = user_details["access_token"]
file_path = "/home/toluhunter/Downloads/Request letter to the VPSD.pdf"

# Set up headers and URL for the API request
headers = {
    "Authorization": "Bearer " + api_token,
    "Accept": "application/vnd.api+json"
}
url = "https://api.unicheck.com/files"

# Read in the file to be checked
file = open(file_path, "rb")

# Make the API request to create a new check
response = requests.post(url, headers=headers, files={"file": file})

# Get the check ID from the response
# check_id = response.json()["data"]["id"]
file_id = response.json()["data"]["id"]
data = {
    "data": {
        "type": "similarityCheck",
        "attributes": {
            "search_types": {
                "web": True,
                "library": False
            },
            "parameters": {
                "sensitivity": {
                    "percentage": 0,
                    "words_count": 8
                }
            }
        }
    },
    "relationships": {
        "file": {
            "data": {
                "id": file_id,
                "type": "file"
            }
        }
    }
}

headers["Content-Type"] = "application/vnd.api+json"

response = requests.post("https://api.unicheck.com/similarity/checks",
                         headers=headers,
                         json=data
                         )

similarity_check_id = response.json()["data"]["id"]
# Make the API request to get the check status and score
# url = f"https://api.unicheck.com/v1/checks/{check_id}/status"
# response = requests.get(url, headers=headers)
# status = response.json()["data"]["status"]
# score = response.json()["data"]["score"]

# Print out the plagiarism score
# if status == "done":
#     print(f"Plagiarism score: {score}%")
# else:
#     print("Check is still in progress. Please try again later.")

# file.close()
