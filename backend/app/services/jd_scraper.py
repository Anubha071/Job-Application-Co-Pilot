import requests

from bs4 import BeautifulSoup

def job_description(url):
    response = requests.get(url, timeout = 10)
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # BROKEN CODE: "get_test" typo, should be "get_text"
    return soup.get_text(separator=" ", strip=True)
