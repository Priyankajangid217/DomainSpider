from googlesearch import search 
import msvcrt
import sys
currCount=0
finalCount=0
specialCase1=[':','*','->']
specialCase2=['->']
urlList=['http:','https:','www.','/']
urlList1=['->']
urlList2=['//']
startedFrom=0
searchResults=0
totalResults=0
lenLink=0

def Help():
    print('\nHow it Works:\nWebscrape uses google search API to search and extracts website links on search results for a search term.')
    print('\nHow to make it Work:\nInstall the googlesearch library using CMD then Run the script.')
    print('\nCommonly Known Issues:\nIt is recommended to Keep Results per Search at most 100.')
    print('If the script stopped working try deleting .google-cookie.txt file stored by google.')
    input()

def requestQuery():
    global searchResults, totalResults, lenLink
    lenLink=0
    query = input('Enter your search term: ')
    if query=='':
        sys.exit(1)
    searchResults=int(input('Enter Results to be shown per Search (Max=100): '))
    totalResults = searchResults
    queryCheck(query)

def queryCheck(query):
    global startedFrom
    print('Loading...')
    try:
        queryFile=query
        for specialChar in specialCase1:
            queryFile=queryFile.replace(specialChar,'')
        queryFile1=queryFile+' searchCache.txt'
        queryFile2=queryFile+' Webscrapped.txt'
        lastSearch= open(queryFile1,'r')
        print('\nPrevious Search Found!\nPress Enter to Continue from Previous Search or Press Space to start over')
        if msvcrt.getch()!=b' ':
            print('Loading...')
            startedFrom=int(lastSearch.readline())
        else:
            print('Loading...')
            startedFrom=0
            pastResults= open(queryFile2,'w')
            pastResults.truncate(0)
            pastResults.close()
        lastSearch.close()
    except:
        startedFrom = 0
    if any(urlParts in query for urlParts in specialCase2):
        queryList=query.split('->')
        query=queryList[0]
        startedFrom=int(queryList[1])
    Search(query, queryFile1, queryFile2)

def Search(query, queryFile1, queryFile2):
    global startedFrom, searchResults, totalResults, finalCount, lenLink
    try:
        count=len(open(queryFile2,'r').readlines())
    except:
        count=0
    links = []
    for link in search(query, tld="co.in", start=startedFrom, num=searchResults, stop=searchResults, pause=5):
        links.append(link)
    print('Webscrapped Links:')
    if len(links)==0:
        print('No Links Found!')
        print('\nWebscrapping tool wrote '+str(finalCount)+' links in the current session')
        endedAt=startedFrom+len(links)
        storeResult(query, queryFile1, queryFile2, endedAt)
        requestQuery()
    corpos = open(queryFile2, 'a')
    for line in links:
        count+=1
        finalCount+=1

        if any(urlParts in line for urlParts in urlList1):
            line=line.split('->')[1]
        if any(urlParts in line for urlParts in urlList2):
            line=line.split('/')[2]
        for urlParts in urlList:
            line=line.replace(urlParts,'')
            line=str(line.strip())

        print(str(count)+'->'+line)
        corpos.write(str(count)+'->'+line+'\n')
    corpos.close()
    endedAt=startedFrom+len(links)
    lenLink+=len(links)
    print('\nWebscrape Log:\nSearched '+str(searchResults)+' results and found '+ str(len(links))+ ' link(s)')
    print('Webscraped  '+str(totalResults)+' results for the search term '+query+' and found '+str(lenLink)+' link(s) written from line '+str(startedFrom+1)+' to '+str(endedAt))
    print('Webscrapping tool wrote '+str(finalCount)+' link(s) in the current session')
    storeResult(query, queryFile1, queryFile2, endedAt)
    startedFrom+=searchResults
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
    requestQuery()

