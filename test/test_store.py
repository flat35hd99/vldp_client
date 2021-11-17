import unittest
from vldp_client.store import Store
import tempfile
import os
import json
import shutil


class TestStore(unittest.TestCase):
    def setUp(self):
        self.tmpdirname = tempfile.mkdtemp()
        self.tmpfilename = os.path.join(self.tmpdirname, "jobs.json")

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdirname)
        return super().tearDown()

    def test_add_jobs(self):
        store = Store()
        job_url = "https://example.com"
        store.add_job(job_url)

        job = store.get_jobs()[0]
        expected = {"url": "https://example.com", "status": "running"}
        self.assertEqual(expected, job)

    def test_save_jobs(self):
        store = Store()
        job_url = "https://example.com"
        store.add_job(job_url)
        saved_json = self.tmpfilename
        store.save(saved_json)

        with open(saved_json) as f:
            jobs = json.load(f)
            expected = {"jobs": [{"url": job_url, "status": "running"}]}
            self.assertDictEqual(expected, jobs)

    def test_save_jobs_with_already_saved_jobs(self):
        saved_json = self.tmpfilename
        with open(saved_json, "w") as f:
            presaved_dict = {
                "jobs": [{"url": "https://example.com", "status": "running"}]
            }
            json.dump(presaved_dict, f, indent=4)

        store = Store()
        another_job_url = "https://another.example.com"
        store.add_job(another_job_url)
        store.save(saved_json)

        with open(saved_json, "r") as f:
            jobs = json.load(f)
            expected = {
                "jobs": [
                    {"url": "https://example.com", "status": "running"},
                    {"url": another_job_url, "status": "running"},
                ]
            }
            self.assertDictEqual(expected, jobs)

    def test_save_twice(self):
        store = Store()
        job_url = "https://example.com"
        store.add_job(job_url)
        saved_json = self.tmpfilename
        store.save(saved_json)
        store.save(saved_json)

        with open(saved_json) as f:
            jobs = json.load(f)
            expected = {"jobs": [{"url": job_url, "status": "running"}]}
            self.assertDictEqual(expected, jobs)
