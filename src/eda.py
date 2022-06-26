import os
import requests
import shutil
from tqdm.auto import tqdm
from zipfile import ZipFile
import pickle
import datetime
import statistics as st
import numpy as np
import pandas as pd

import plotly.express as px



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
                    with open(rf"{download_path}/{filename}", 'wb') as output:
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
    def serialize(data: dict, serial_path: str):
        with open(serial_path, "wb") as f:
            pickle.dump(data, f)


class Cleaner:
    def __init__(self, serial_path: str):
        with open(serial_path, "rb") as f:
            self.data: dict = pickle.load(f)

    def duplicated(self, key: str, subset: list):
        df = self.data[key]
        return df[df.duplicated(subset=subset)]

    def drop_duplicates(self, key: str, subset: list):
        self.data[key] = self.data[key].drop_duplicates(subset=subset).reset_index(drop=True)

    def fillna(self, key: str, column: str, value: str):
        column_type: type = self.data[key][column].dtypes

        value = column_type(value)

        self.data[key] = self.data[key][column].fillna(value=value)

    def drop_na(self, key: str, subset: list):
        self.data[key] = self.data[key].dropna(subset=subset).reset_index(drop=True)

    def to_datetime(self, key: str, column: str):
        self.data[key][column] = self.data[key][column].apply(pd.to_datetime)

    @staticmethod
    def serialize(data: dict, serial_path: str):
        with open(serial_path, "wb") as f:
            pickle.dump(data, f)


class Explorer:
    def __init__(self, serial_path: str):
        with open(serial_path, "rb") as f:
            self.data: dict = pickle.load(f)

    @staticmethod
    def serialize(data: dict, serial_path: str):
        with open(serial_path, "wb") as f:
            pickle.dump(data, f)


class OutlierDetector:
    def __init__(self, data: list):
        self.data = data
        self.q1 = np.percentile(data, 25)
        self.q2 = np.percentile(data, 50)
        self.q3 = np.percentile(data, 75)
        #self.q1, self.q2, self.q3 = st.quantiles(data)
        self.a = self.q3 - self.q1
        self.extreme = []
        self.moderate = []
        self.regular = []

        for d in self.data:
            self.check_outlier(d)

    def check_outlier(self, value: float) -> str:
        if value < (self.q1 - 3 * self.a) or value > (self.q3 + 3 * self.a):
            self.extreme.append(value)
            self.moderate.append(value)
        elif value < (self.q1 - 1.5 * self.a) or value > (self.q3 + 1.5 * self.a):
            self.moderate.append(value)
        else:
            self.regular.append(value)

    def __str__(self):
        return f"Extreme:\t{len(self.extreme)}\nModerate:\t{len(self.moderate)}\nRegular:\t{len(self.regular)}"