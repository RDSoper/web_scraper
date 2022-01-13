import requests  # Allows you to download the html.
from bs4 import BeautifulSoup  # Allows you to use the html to grab data to scrape it.
import pprint

res = requests.get('https://news.ycombinator.com/news')  # Grabs the html file for this url
# Prints out the html as a string.
soup = BeautifulSoup(res.text, 'html.parser')  # This takes the html file from res, and converts it to html.
# gives the body of the html file.
# Turns previous into a list.
# Finds all the a tags in the html files. Therefore finding all the links.
res2 = requests.get('https://news.ycombinator.com/news?p=2')
soup2 = BeautifulSoup(res2.text, 'html.parser')
"""
The select method for beautiful soup means that you can select certain attributes in the elements that give the 
information that you are after. In this case we want the link and the score as we are looking for news that has more 
than 100 votes. look in the html file to find this.
"""

links = soup.select(".titlelink")
subtext = soup.select(".subtext")
links2 = soup2.select(".titlelink")
subtext2 = soup2.select(".subtext")

super_links = links + links2
super_subtext = subtext + subtext2


def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)


def create_custom_hacker_news(links, subtext):
    '''
    Takes the link and the votes for that link and puts those recieving > 100 votes into a list that it returns.
    :param links: The link of the article.
    :param votes: The number of votes article recieved.
    :return: List of all articles with a score > 100
    '''
    hn = []
    for index, item in enumerate(super_links):
        title = item.getText()
        href = item.get('href', None)
        votes = subtext[index].select('.score')
        if len(votes):
            points = int(votes[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
            else:
                continue
    return sort_stories_by_votes(hn)


def grab_pages(url):
    superlink = []
    supersubtext = []
    i = 1
    while i < 21:
        res = requests.get(url + str(i))
        #print(url + str(i))
        soup = BeautifulSoup(res.text, 'html.parser')
        links = soup.select('.titlelink')
        subtext = soup.select(".subtext")
        superlink += links
        supersubtext += subtext
        i += 1
    return pprint.pprint(create_custom_hacker_news(superlink, supersubtext))


grab_pages('https://news.ycombinator.com/news?p=')