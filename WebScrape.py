from googlesearch import search 
import msvcrt
import sys
currCount=0
specialCase1=[':','*']
specialCase2=['->']
startFrom=0
startedFrom=0

def Help():
    print('\nHow it Works:\nWebscrape uses google search API to search and extracts website links on search results for a search term.')
    print('\nHow to make it Work:\nInstall the googlesearch library using CMD then Run the script.')
    print('\nCommonly Known Issues:\nIt is recommended to Keep Results per Search at most 100.')
    print('If the script stopped working try deleting .google-cookie.txt file stored by google.')
    input()

def requestQuery():
    query = input('Enter your search term: ')
    if query=='':
        sys.exit(1)
    queryCheck(query)

def queryCheck(query):
    global startFrom, startedFrom
    print('Loading...')
    try:
        queryFile=query
        for specialChar in specialCase1:
            queryFile=queryFile.replace(specialChar,'')
        queryFile1=queryFile+'-searchCache.txt'
        queryFile2=queryFile+'-Webscrapped.txt'
        lastSearch= open(queryFile1,'r')
        print('\nPrevious Search Found!\nPress Enter to Continue from Previous Search or Press Space to start over')
        if msvcrt.getch()!=b' ':
            print('Loading...')
            startFrom=int(lastSearch.readline())
            startedFrom=startFrom+1
            lastSearch.close()
        else:
            print('Loading...')
            startFrom=0
            startedFrom+=1
    except:
        startFrom=0
        startedFrom+=1
    if any(urlParts in query for urlParts in specialCase2):
        queryList=query.split('->')
        query=queryList[0]
        startFrom=int(queryList[1])
        startedFrom=startFrom+1
    Search(query, queryFile1, queryFile2)

def Search(query, queryFile1, queryFile2):
    global startFrom, startedFrom, searchResults, totalResults, currCount
    try:
        count=len(open(queryFile2,'r').readlines())
    except:
        count=0
    links = []
    for link in search(query, tld="co.in", start=startFrom, num=searchResults, stop=searchResults, pause=5):
        links.append(link)
    print('Webscrapped Links:')
    if len(links)==0:
        print('No Links Found!')
        print('\nWebscrapping tool wrote a total '+str(currCount)+' corpo links')
        endedAt=startFrom+searchResults
        storeResult(query, queryFile1, queryFile2, endedAt)
        requestQuery()
    corpos = open(queryFile2, 'a')
    for line in links:
        count+=1
        currCount+=1
        print('Webscrapped link for corpo '+str(count)+'->'+line)
        corpos.write('Webscrapped link for corpo '+str(count)+'->'+line+'\n')
    corpos.close()
    endedAt=startFrom+searchResults
    print('\nWebscrapping Done!\nWritten '+str(totalResults)+' Results Webscrapped for the search term '+query+' from '+str(startedFrom)+' to '+str(endedAt))
    print('Webscrapping tool wrote a total '+str(currCount)+' corpo links')
    storeResult(query, queryFile1, queryFile2, endedAt)
    startFrom+=searchResults
    totalResults+=searchResults
    
    print('\nPress Space to Load Next Resutlts or Enter to Search Again')
    if msvcrt.getch()==b' ':
        print('Loading Next Results...')
        Search(query, queryFile1, queryFile2)
    else:
        totalResults=searchResults
        requestQuery()

def storeResult(query,queryFile1, queryFile2, endedAt):
    for specialChar in specialCase2:
        query=query.replace(specialChar,'')
    lastSearch= open(queryFile1,"w")
    lastSearch.write(str(endedAt))
    lastSearch.close()

print('Welcome to Webscrapper tool!\nPress Enter to Webscrape / Press H for help')
userInput=msvcrt.getch()
if userInput==b'h':
    Help()
else:
    searchResults=int(input('Enter Results to be shown per Search: '))
    totalResults=searchResults
    requestQuery()

