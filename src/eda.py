import os
import requests
import shutil
from tqdm.auto import tqdm
from zipfile import ZipFile

import pandas as pd


class Gatherer:
    def __init__(self, urls: dict):
        self.urls = urls

    def download(self, download_path: str):
        for year in self.urls.keys():
            # make an HTTP request within a context manager
            with requests.get(self.urls[year], stream=True) as r:
                # check header to get content length, in bytes
                total_length = int(r.headers.get("Content-Length"))

                # implement progress bar via tqdm
                with tqdm.wrapattr(r.raw, "read", total=total_length, desc=f"Downloading data for {year}") as raw:
                    # save the output to a file
                    with open(f"{download_path}/{year}.zip", 'wb') as output:
                        shutil.copyfileobj(raw, output)

    def extract(self, download_path: str, extract_path: str):

        filepaths = [os.path.join(download_path, filename) for filename in os.listdir(download_path) if os.path.isfile(os.path.join(download_path, filename))]

        for filepath in filepaths:
            with ZipFile(f"{filepath}", mode="r") as f:
                f.extractall(path=f"{extract_path}/{filepath.split('/')[-1][:4]}")
            print(f"{filepath} successfully extracted to {extract_path}/{filepath.split('/')[-1][:4]}")


class Selector:
    def __init__(self):
        self.dfs: dict = {}

    def read(self, directory: str):

        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            # checking if it is a file
            if os.path.isfile(filepath) and filepath.endswith(".csv"):
                self.dfs[filename[:-4]] = pd.read_csv(filepath)
