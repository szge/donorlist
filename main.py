import bs4
from bs4 import BeautifulSoup
import requests
import time
import os


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


def contact_element(tag: bs4.Tag) -> bool:
    """check if the tag is a contact element"""
    return "contact" in tag.text.lower()


def create_contact_list() -> None:
    """create contact.md from people/"""
    # clear contact.md
    with open("contact.md", "w", encoding="utf-8") as contact_file:
        contact_file.write("# Contact List\n\n")  # Initialize with a title

    for donor in os.listdir("people"):
        if donor.endswith(".md"):
            with open("people/" + donor, "r", encoding="utf-8") as donor_file:
                donor_html = donor_file.read()
                soup = BeautifulSoup(donor_html, "html.parser")
                post = soup.find("div", class_="post")
                donor_name = post.find("h1", class_="entry-title").text

                # Assuming the contact element is defined by the text 'CONTACT:'
                contact_element = soup.find("strong", string='CONTACT:')

                # If contact element exists
                if contact_element:
                    # Get the position of the end of the contact element in the raw HTML
                    end_pos = donor_html.find(str(contact_element)) + len(str(contact_element))

                    # Extract everything after the contact element
                    content_after_contact = donor_html[end_pos:]

                    # make sure content_after_contact is valid html
                    # content_after_contact = BeautifulSoup(content_after_contact, "html.parser").prettify()
                    content_after_contact = BeautifulSoup(content_after_contact, "html.parser").decode()

                    # remove everything after and including <!--POST FOOTER-->
                    post_footer = content_after_contact.find("<!--POST FOOTER-->")
                    if post_footer != -1:
                        content_after_contact = content_after_contact[:post_footer]

                    # Append the donor's name and content to the contact.md
                    with open('contact.md', 'a', encoding='utf-8') as contact_file:
                        contact_file.write(f"\n### {donor_name}\n\n")
                        contact_file.write(content_after_contact)
                        contact_file.write('\n')


if __name__ == "__main__":
    # get_donor_list()
    create_contact_list()
