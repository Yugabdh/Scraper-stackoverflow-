import requests
import scraperdbconn
from bs4 import BeautifulSoup


# this is list for those laguages we are going to perform scrapping
# tags = ['python', 'java', 'c', 'sql']
# this is list for type of sort methods available on particular language tab
sorts = ['newest', 'frequent', 'votes', 'active']
try:
    # casting url for perticular tag and sorting options
    # for tag in tags:
    #     print(f"{tags.index(tag)+1}. {tag}")
    tags = scraperdbconn.getQueries()
    tag = int(input("Choose option from above: ")) - 1

    for sort in sorts:
        print(f"{sorts.index(sort)+1}. {sort}")
    sort = int(input("Choose sorting option from above: ")) - 1
    payload = {'pagesize': 50, 'sort': sorts[sort]}
    url = f"https://stackoverflow.com/questions/tagged/{tags[tag]}"

    # fetching document
    stackDoc = requests.get(url, params=payload).text
    # parsing doc to Beautifulsoup
    soup = BeautifulSoup(stackDoc, features='lxml')

    # finding question block i.e. div with id="questions"
    questionBlock = soup.find('div', id='questions')
    # finding question summary i.e.class="question-summary"
    AllquestionsSummary = questionBlock.find_all('div', class_='question-summary')
    # grading question and iterating over it
    i = 1
    for questionSummary in AllquestionsSummary:
        questionLinks = questionSummary.find('a', class_='question-hyperlink')
        print(f"{i}) Question: {questionLinks.text}")
        print(f"   link: https://stackoverflow.com{questionLinks.get('href')}")
        print()
        i += 1

except IndexError as e:
    print("Wrong input enter proper selection")
# except ValueError as e:
#     print("Enter proper value")
except ConnectionError as e:
    print("Error while resolving link")
