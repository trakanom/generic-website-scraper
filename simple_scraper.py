# %%
import requests
from collections import OrderedDict
import re
import html5lib
from bs4 import BeautifulSoup

parsing_library = "html5lib"
storage = OrderedDict()

def quick_parse(URL):
    '''Downloads and prepares a webpage's content for parsing.'''
    html_text = requests.get(URL).text #Downloads the contents of the webpage
    soup = BeautifulSoup(html_text, parsing_library) #Converts the contents into a parsing object. 
    return soup

def get_main_points(soup):
    '''Returns a formatted text object of all the headers on the webpage. This is the function that creates our result.'''
    body = soup #.find("div", class_="right_sec singlePost") # Commented this second part out to generalize better.
    headerings = [item.text for item in body.find_all(re.compile(r"^h\d$"))]
    sections = [item.text for item in body.find_all(re.compile("h1|h2"))]
    headerings_string = "\n".join([("\n" if (item in sections) else "\t") + item for item in headerings])
    return headerings_string

def save_my_results(URL, label):
    '''Ties all these functions together. Inserts the result from parsing a webpage and scraping the titles into storage.'''
    global storage
    results = get_main_points(quick_parse(URL)) 
    entry = {label:{"results":results, "URL":URL}} #storing our results with 
    storage |= entry #Adds entry to storage dictionary
    return entry

def get_last_result():
    '''Returns and prints the last entry in our storage dictionary'''
    result = storage[next(reversed(storage))]['results']
    print(result)
    return result


# %%
my_url="https://www.mydegreeguide.com/how-to-study-tips/"
save_my_results(URL=my_url,label="2023 Ultimate Study Tips Guide")
print(get_last_result())






# %%
next_URL="https://learningcenter.unc.edu/tips-and-tools/studying-101-study-smarter-not-harder/"
save_my_results(URL=next_URL,label="Studying 101: Study Smarter Not Harder")
get_last_result()

# %%
storage.keys()

# %%
item = list(storage.keys())[0]
storage[item].__str__()

# %%
#WIP
quotes = [re.search(r"\d{1,3}\.(\w+)$",paragraph.text).group(1).strip() for paragraph in html.find("div", class_="m-detail--body").find_all("p")]


