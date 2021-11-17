import json
import os


class Store:
    def __init__(self):
        self.jobs = []

    def add_job(self, job_url):
        job = {"url": job_url, "status": "running"}
        self.jobs.append(job)

    def get_jobs(self):
        return self.jobs

    def save(self, filename):
        dict = self.load(filename)
        new_saved_jobs = [job for job in self.jobs if job not in dict["jobs"]]
        dict["jobs"].extend(new_saved_jobs)
        with open(filename, "w") as f:
            json.dump(dict, f, indent=4)

    def load(self, filename):
        if os.path.exists(filename):
            with open(filename, "r") as f:
                saved = json.load(f)
            return saved
        else:
            return {"jobs": []}
