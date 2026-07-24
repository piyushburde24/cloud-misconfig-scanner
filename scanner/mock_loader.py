"""
Load mock AWS data from JSON files.
"""

import json
from pathlib import Path


class MockLoader:

    def __init__(self):

        self.base_path = Path("mock_data")

    def load(self, filename):

        file_path = self.base_path / filename

        with open(file_path, "r") as file:

            return json.load(file)
