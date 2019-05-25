import requests
import scraperdbconn
from bs4 import BeautifulSoup


def fetchDoc():
    try:
        stackDoc = None
        # this is list for those laguages we are going to perform scrapping
        # tags = ['python', 'java', 'c', 'sql']
        # this is list for type of sort methods available on particular language tab
        # casting url for perticular tag and sorting options
        sorts = ['newest', 'frequent', 'votes', 'active']

        tags = scraperdbconn.getQueries()
        print()
        print("Previously searched keyword:")
        print("0. Want to search for something else?")
        for i, tag in enumerate(tags, 1):
            print(f"{i}. {tag}")
        tag = int(input("Choose option from above: "))
        if tag == 0:
            userTag = input("Enter Your own choice: ")
        else:
            userTag = tags[tag - 1]
        print()
        # Final url
        url = f"https://stackoverflow.com/questions/tagged/{userTag}"

        if not tag == 0:
            for i, sort in enumerate(sorts, 1):
                print(f"{i}. {sort}")
            sort = int(input("Choose sorting option from above: "))
            sort = sort - 1
            # payloads are parameters to be passed in request url in browsers
            payload = {'pagesize': 50, 'sort': sorts[sort]}
            # fetching document
            stackDocReq = requests.get(url, params=payload)
        else:
            payload = {'pagesize': 50, 'tab': 'relevance'}
            url = f"https://stackoverflow.com/search"
            payload = {'tab': 'relevance', 'q': userTag}
            stackDocReq = requests.get(url, params=payload)
        print()

        if stackDocReq:
            stackDoc = stackDocReq.text
        else:
            print("Error Fetching document(FetchDoc())")
        if tag == 0:
            print("[*]Adding currently searched query to DataBase")
            scraperdbconn.addQuery(userTag)
        return stackDoc, userTag

    except IndexError as e:
        print("[!] Wrong input enter proper selection")
        return stackDoc
    except ValueError as e:
        print("[!] Enter proper value")
        return stackDoc
    except ConnectionError as e:
        print("[!] Failed to fetch website. Maybe your connection is broken.")
    except Exception as e:
        raise e


def scrap(stackDoc, userTag):
    tags = scraperdbconn.getQueries()
    queref = tags.index(userTag) + 1
    # passing fetched document to BeautifulSoup constructor
    soup = BeautifulSoup(stackDoc, features='lxml')

    # finding question block i.e. div with id="questions"
    questionBlock = soup.find('div', id='content')
    # finding question summary i.e.class="question-summary"
    AllquestionsSummary = questionBlock.find_all('div', class_='question-summary')

    # iterating over question
    data = list()
    for i, questionSummary in enumerate(AllquestionsSummary, 1):
        questionLinks = questionSummary.find('a', class_='question-hyperlink')
        votes = questionSummary.find('span', class_='vote-count-post').find('strong').text
        answered = questionSummary.find('div', class_='status').find('strong').text
        print(f"{i}) Question: {questionLinks.text}")
        linkForQus = questionLinks.get('href')
        print(f"   link: https://stackoverflow.com{linkForQus}")
        flink = f"https://stackoverflow.com{linkForQus}"
        print(f"Votes: {votes} || Answers: {answered}")
        currentScrappedData = (int(queref), str(questionLinks.text), str(flink), int(votes), int(answered))
        data.append(currentScrappedData)
        print()

    toStore = input("Want to store currently scrapped Data to DataBase?(y/n):").lower()
    if toStore == 'y':
        scraperdbconn.insertScrappedData(data)


print("[*] Welcome user!")
c = 0
while c != 5:
    print("___________Menu___________")
    print("1. Fetch document")
    print("2. Scrap fetched document")
    print("3. Get Data From DB")
    print("4. Delete Data From DB")
    print("5. Quit")
    c = input("choice: ").strip()
    c = int(c)
    if c == 1:
        stackDoc, userTag = fetchDoc()
    elif c == 2:
        if stackDoc:
            scrap(stackDoc, userTag)
    elif c == 3:
        scraperdbconn.getDatafromDB()
    elif c == 4:
        scraperdbconn.deleteScrapped()
    elif c == 5:
        pass
    else:
        print("[!] Error fetching document")
