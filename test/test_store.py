import unittest
from vldp_client.store import Store


class TestStore(unittest.TestCase):
    def test_save_jobs(self):
        store = Store()
        store.add_job()
