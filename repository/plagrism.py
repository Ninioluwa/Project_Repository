import requests
import os

from shutil import rmtree

from django.conf import settings


BASE_DIR = settings.BASE_DIR


class Plagiarism:

    base_url = "https://api.unicheck.com"

    def __init__(self):
        data = {
            "grant_type": "client_credentials",
            "client_id": settings.UNICHECK_CLIENT_ID,
            "client_secret": settings.UNICHECK_CLIENT_SECRET
        }

        user_details = requests.post(
            f"{self.base_url}/oauth/access-token", data=data).json()

        self.headers = {
            "Authorization": "Bearer " + user_details["access_token"],
            "Accept": "application/vnd.api+json"
        }

    def re_authenticate(self):
        data = {
            "grant_type": "client_credentials",
            "client_id": settings.UNICHECK_CLIENT_ID,
            "client_secret": settings.UNICHECK_CLIENT_SECRET
        }

        user_details = requests.post(
            f"{self.base_url}/oauth/access-token", data=data).json()

        self.headers = {
            "Authorization": "Bearer " + user_details["access_token"],
            "Accept": "application/vnd.api+json"
        }

    def upload_file(self, instance):
        # Set up headers and URL for the API request
        url = f"{self.base_url}/files"

        # Make the API request to create a new check
        response = requests.post(
            url, headers=self.headers, files={"file": instance.document})

        instance.file_id = response.json()["data"]["id"]

    def start_plagiarism_check(self, instance):
        file_id = instance.file_id
        data = {
            "data": {
                "type": "similarityCheck",
                "attributes": {
                    "search_types": {
                        "web": True,
                        "library": False
                    },
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

        self.headers["Content-Type"] = "application/vnd.api+json"

        response = requests.post(f"{self.base_url}/similarity/checks",
                                 headers=self.headers,
                                 json=data
                                 )

        # Get the check ID from the response
        instance.similarity_check_id = response.json()["data"]["id"]

    def fetch_plagiarism_details(self, instance):
        # Make the API request to get the check status and score
        check_id = instance.similarity_check_id
        url = f"{self.base_url}/similarity/checks/{check_id}"
        response = requests.get(url, headers=self.headers)
        score = response.json()["data"]["attributes"]["similarity"]

        return (score, response.json())

    def export_report(self, instance):
        check_id = instance.similarity_check_id

        url = f"{self.base_url}/similarity/checks/{check_id}/report/export"
        self.headers["Content-Type"] = "application/vnd.api+json"
        data = {
            "data": {
                "type": "similarity-check-report-export",
                "attributes": {
                    "format": "pdf",
                    "locale_code": "EN"
                }
            }
        }

        requests.post(url, json=data, headers=self.headers)

    def download_report(self, instance, link):
        self.headers.pop("Accept")
        response = requests.get(link, headers=self.headers, stream=True)

        return response

    def delete_downloaded_report(self, instance):
        base_path = os.path.join(BASE_DIR, "static", "media",
                                 "repo", instance.project_id)

        rmtree(base_path)


if __name__ == "__main__":
    obj = Plagiarism()

    class Instance:
        document = None
        file_id = "42c15d96a6b54ff89bffc98a5954e751"
        similarity_check_id = "af62630cf72c404ab1a96c584db6e157"
        job_id = "6515002"
        project_id = "justatest-232829"

    instance = Instance()

    instance.document = open(
        "<file_path>", "rb")

    # Run To start Plagrism
    # obj.upload_file(instance)
    # print(instance.file_id)

    # Run Once File Is Done Checking
    # obj.start_plagiarism_check(instance)
    # print(instance.similarity_check_id)

    # Get Plagiarism Details
    # obj.fetch_plagiarism_details(instance)

    # Export Plagiarism report
    # obj.export_report(instance)
    # print(instance.job_id)

    # Download Report
    # obj.download_report(instance)

    # Delete Report
    # obj.delete_downloaded_report(instance)
