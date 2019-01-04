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
sites = []
titles = []
pages = int(712 / 50) + 1
for i in range(0, pages):
    page = (50*i) + 1
    sites.append("https://www.imdb.com/search/title?title_type=feature&keywords=superhero&explore=genres&view=simple&start={}".format(page))

for site in sites:
    raw_html = simple_get(site)
    html = BeautifulSoup(raw_html, 'html.parser')

    for p in html.find_all("span", class_='lister-item-header'):
        for l in p:
            if str(l).startswith("<span title="):
                for r in l:
                    b = str(r)
                    if b.startswith("<a"):
                        titles.append(b[(b.find(">") + 1):b.rfind("<")])

    with open('superhero_films.py', 'w', encoding="utf8") as f:
        f.write(str(titles))