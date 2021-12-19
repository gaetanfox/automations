import requests
import json
from send_email import send_email

URL = "https://remoteok.io/api/"
keys = ["date", "company", "position", "tags", "location", "url"]

wanted_tags = ["python"]


def get_jobs():
    resp = requests.get(URL)
    job_results = resp.json()

    jobs = []
    for job_res in job_results:
        job = {k: v for k, v in job_res.items() if k in keys}

        if job:
            tags = job.get("tags")
            tags = {tags.lower() for tags in tags}
            if tags.intersection(wanted_tags):
                jobs.append(job)
    return jobs


if __name__ == "__main__":
    python_jobs = get_jobs()

    if python_jobs:
        message = "Subject: New python jobs!!\n\n"

        for job in python_jobs:
            message += f"{json.dumps(job)}\n\n"

        send_email(message)
