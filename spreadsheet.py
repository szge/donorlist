"""Create a spreadsheet file with all donors and their information"""
import os
from bs4 import BeautifulSoup
import pandas as pd


def create_spreadsheet():
    pass


def insert_donor(donor_name: str, donor_info: dict) -> None:
    """
    insert donor into spreadsheet
    :param donor_name:
    :param donor_info:
    :return:
    """
    df = pd.read_csv("donors.csv")
    print(df)
    # if df["Name"].apply(lambda x: compare_names(x, donor_name)).any():
    #     # if donor exists update
    #     df.loc[df["Name"] == donor_name, list(donor_info.keys())] = list(donor_info.values())
    # else:
    #     # else insert
    #     df = df.append(donor_info, ignore_index=True)
    # df.to_csv("donors.csv", index=False)


def compare_names(name1: str, name2: str) -> bool:
    # remove all instances of the word "and"
    words1 = set([word for word in name1.split() if word != "and"])
    words2 = set([word for word in name2.split() if word != "and"])
    if len(words1.intersection(words2)) >= 2:
        return True
    return False


if __name__ == "__main__":
    for file in os.listdir("people"):
        if file.endswith(".md"):
            with open("people/" + file, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f.read(), "html.parser")
                donor_name = soup.find("h1", class_="entry-title").text
                # print(donor_name)
                insert_donor(donor_name, {})

