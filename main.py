from bs4 import BeautifulSoup
import requests
import time


def get_donor_list() -> None:
    """
    fetch Top Donor list from https://www.insidephilanthropy.com/tech-philanthropy-guide
    :return:
    """
    url = "https://www.insidephilanthropy.com/tech-philanthropy-guide"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    donor_list = soup.find_all("a", href=lambda href: href and href.startswith("https://www.insidephilanthropy.com/guide-to-individual-donors"))
    # print(donor_list)
    for donor in donor_list:
        # print(donor.text)
        # create_donor_profile(donor.get("href"))
        # # wait for 5 seconds
        # time.sleep(5)
        # attempt 5 times to create donor profile
        for i in range(5):
            if create_donor_profile(donor.get("href")):
                break
            time.sleep(3)


def create_donor_profile(page_url: str) -> bool:
    """
    create donor profile from the page url
    :param page_url:
    :return: success or not
    """
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, "html.parser")
    post = soup.find("div", class_="post")
    if post is None:
        print(page_url)
        return False
    base_url = "https://www.insidephilanthropy.com"
    # replace all links with absolute links
    for link in post.find_all("a"):
        if link["href"].startswith("/"):
            link["href"] = base_url + link["href"]

    donor_name = post.find("h1", class_="entry-title").text
    # write to markdown
    with open("people/" + donor_name + ".md", "w", encoding="utf-8") as file:
        # write the html
        file.write(str(post))

    return True


if __name__ == "__main__":
    get_donor_list()
