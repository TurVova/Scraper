import random
import time
import requests
from bs4 import BeautifulSoup as bs4
from fake_useragent import UserAgent
from ipdb import set_trace
BASIC_URL = "https://www.work.ua"
DNIPRO_VAC = "/jobs-dnipro/"
def random_sleep():
    time.sleep(random.randint(1, 2))
def main():
    url = BASIC_URL + DNIPRO_VAC
    pages_count = get_pages_count()
    UA = UserAgent()
    with open("test.txt", "w") as f:
        for page in range(1, pages_count+1):
            print(page, "OUT OF:", pages_count)
            headers = {
                'User-Agent': UA.random,
            }
            payload = {
                'page': page,
            }
            response = requests.get(url, params=payload, headers=headers)
            random_sleep()
            soup = bs4(response.text, "html.parser")
            job_divs = soup.findAll("div", { "class" : "job-link" })
            for elem in job_divs:
                r = elem.find("h2").find("a")
                href = r.get("href", "")
                content = r.text
                company = elem.find_all("div")[-1].find("span").text
                vacancy_id = "".join([i for i in href if i.isdigit()])
                f.write("VAC_ID: {}, CONTENT: {}, HREF: {}, COMPANY: {}\n".format(
                    vacancy_id, content, href, company
                ))
def get_pages_count():
    url = BASIC_URL + DNIPRO_VAC
    response = requests.get(url)
    soup = bs4(response.text, "html.parser")
    pages = soup.find_all("ul", {"class": "pagination hidden-xs"})[0]
    return max([to_int(i.text) for i in pages.find_all("a")])
def to_int(value):
    try:
        return int(value)
    except ValueError:
        return 0
if __name__ == "__main__":
    main()
