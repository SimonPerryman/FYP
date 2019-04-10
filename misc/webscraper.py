# Code from https://realpython.com/python-web-scraping-practical-introduction/
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)
# End of Code Snippet

def get_imdb_film_details(FilmID):
    details = []
    raw_html = simple_get("https://www.imdb.com/title/{}".format(FilmID))
    html = BeautifulSoup(raw_html, 'html.parser')
    for tag in html.find_all("img"):
        title = tag.attrs.get('title', '')
        if title and title[-6:] == 'Poster':
            details.append(tag.attrs.get('src', ''))
    for tag in html.find_all("div", "summary_text"):
        details.append(tag.text.strip())
    return details[0], details[1]

if __name__ == "__main__":
    print(get_imdb_film_details("tt0110912"))