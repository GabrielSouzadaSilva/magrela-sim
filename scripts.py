import os

os.chdir("../")
os.getcwd()

from src.eda import Gatherer

urls = [
    "https://web.archive.org/web/20170221074848/https://s3.amazonaws.com/pronto-data/open_data_year_one.zip",
    "https://web.archive.org/web/20220314100611/https://s3.amazonaws.com/pronto-data/open_data_year_two.zip",
    "https://web.archive.org/web/20170317213337/https://s3.amazonaws.com/pronto-data/open_data_2016-12.zip"
]

gatherer = Gatherer(urls=urls)
gatherer.download(download_path="data/raw")
gatherer.extract(download_path="data/raw", extract_path="data/extracted")

