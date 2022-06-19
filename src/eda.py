import os
import requests
import shutil
from tqdm.auto import tqdm
from zipfile import ZipFile
import pickle

import pandas as pd
import matplotlib.pyplot as plt


class Gatherer:
    def __init__(self, urls: list):
        self.urls: list = urls

    def download(self, download_path: str):
        for url in self.urls:
            # make an HTTP request within a context manager
            with requests.get(url, stream=True) as r:
                # check header to get content length, in bytes
                total_length = int(r.headers.get("Content-Length"))

                # implement progress bar via tqdm
                filename = url.split('/')[-1]
                with tqdm.wrapattr(r.raw, "read", total=total_length, desc=f"Downloading \"{filename}\"") as raw:
                    # save the output to a file
                    with open(f"{download_path}/{filename}", 'wb') as output:
                        shutil.copyfileobj(raw, output)

    def extract(self, download_path: str, extract_path: str):

        filepaths = [os.path.join(download_path, filename) for filename in os.listdir(download_path) if os.path.isfile(os.path.join(download_path, filename))]

        for filepath in filepaths:
            with ZipFile(f"{filepath}", mode="r") as f:
                f.extractall(
                    path=f"{extract_path}/{filepath.split('/')[-1][:-4]}")
            print(
                f"{filepath} successfully extracted to {extract_path}/{filepath.split('/')[-1][:-4]}")


class Selector:
    def __init__(self):
        self.dfs: dict = {}

    def read(self, directory: str):

        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)

            if os.path.isfile(filepath) and filepath.endswith(".csv"):
                self.dfs[filename[:-4]] = pd.read_csv(filepath)

    def concatenate(self, keys: list, columns: list) -> pd.DataFrame:
        df = pd.DataFrame()

        for key in keys:
            if key in self.dfs.keys():
                df = pd.concat([df, self.dfs[key]]).reset_index(drop=True)[columns]

        return df

    @staticmethod
    def serialize(df: pd.DataFrame, serial_path: str):
        with open(serial_path, "wb") as f:
            pickle.dump(df, f)


class Cleaner:
    def __init__(self, serial_path: str):
        with open(serial_path, "rb") as f:
            self.df: pd.DataFrame = pickle.load(f)

    def duplicated(self, subset: list):
        return self.df[self.df.duplicated(subset=subset)]

    def drop_duplicates(self, subset: list):
        self.df = self.df.drop_duplicates(subset=subset).reset_index(drop=True)

    def fillna(self, column: str, value: str):
        column_type: type = self.df[column].dtypes

        value = column_type(value)

        self.df = self.df[column].fillna(value=value)

    def drop_na(self, subset: list):
        self.df = self.df.dropna(subset=subset).reset_index(drop=True)
