from googlesearch import search 
import msvcrt
currCount=0
finalCount=0
specialCase=[':','*']
urlList1=['//']
urlList2=['http:','https:','www.','/']
startedFrom=0
searchResults=0
totalResults=0
lenLink=0
uniqLenLink=0

def Help():
    print('\nHow it Works:\nWebscrape uses google search API and extracts unique domain names (e.g. xyz.com) from the search results.')
    print('\n"Last Search" is the number of results previously obtained from the script for a particular search term.')
    print('User can continue from the Last Search, which is previously saved in a .cache file by the script\nor it can be user specified in the search term.')
    print('To specify just add -> to the search term and specify a number after it.\nwhich will be taken as user specified Last Search for the search term.')
    print('\nHow to make it Work:\nInstall the googlesearch library using CMD then Run the script.')
    print('\nCommonly Known Issues:\nIt is recommended to Keep Results per Search at most 100.')
    print('If the script stopped working try deleting .google-cookie.txt file stored by google.')

def requestQuery():
    global searchResults, totalResults
    query = input('Enter your search term: ')
    if query=='':
        exit()
    searchResults=int(input('Enter Results to be shown per Search (Max=100): '))
    totalResults = searchResults
    queryCheck(query)

def queryCheck(query):
    global startedFrom
    print('Loading...')
    queryFile=query
    for specialChar in specialCase:
        queryFile=queryFile.replace(specialChar,'')
    if '->' in query:
        queryList=queryFile.split('->')
        queryFile=queryList[0]
    queryFile1=queryFile+'.cache'
    queryFile2=queryFile+'.txt'
    try:
        lastSearch= open(queryFile1,'r')
        print('\nPrevious Search Found!\nPress Enter to continue from Last Search (found in cache file / specified by user) or Press Space to start over')
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
    if '->' in query:
        print('\nStarting from user specified Last Search...')
        startedFrom=int(queryList[1])
        query=query.split('->')[0]
    Search(query, queryFile1, queryFile2)

def Search(query, queryFile1, queryFile2):
    global startedFrom, searchResults, totalResults, finalCount, lenLink, uniqLenLink
    uniqLenLink=0
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
        storeResult(queryFile1, endedAt)
        requestQuery()
    
    for line in links:
        if any(urlParts in line for urlParts in urlList1):
            line=line.split('/')[2]
        for urlParts in urlList2:
            line=line.replace(urlParts,'')
            line=str(line.strip())
        exception=False
        try:
            corpos = open(queryFile2, 'r+')
            for txtLine in corpos:
                if line in txtLine:
                    exception=True
                    break

            if exception==False:
                count+=1
                finalCount+=1
                print(str(count)+'->'+line)
                corpos.write(str(count)+'->'+line+'\n')
                uniqLenLink+=1
            
        except:
            corpos = open(queryFile2, 'w')
            count+=1
            finalCount+=1
            print(str(count)+'->'+line)
            corpos.write(str(count)+'->'+line+'\n')
            uniqLenLink+=1

    corpos.close()
    endedAt=count=len(open(queryFile2,'r').readlines())
    lenLink+=len(links)

    print('\nWebscrape Log:\nSearched for '+str(searchResults)+' result(s) and found '+ str(len(links))+ ' link(s).')
    print('Searched a total of '+str(totalResults)+' result(s) and found '+str(lenLink)+' link(s) for the current search term.')
    print('Webscrape wrote '+str(uniqLenLink)+' link(s) with now a total of '+str(endedAt)+' unique Domain name(s) for the search term "'+query+'".')
    print('Webscrapping tool wrote '+str(finalCount)+' link(s) in the current session.')
    
    storeResult(queryFile1, endedAt)
    startedFrom+=searchResults
    totalResults+=searchResults
    
    print('\nPress Space to Load Next Resutlts or Enter to Search Again')
    if msvcrt.getch()==b' ':
        print('Loading Next Results...')
        Search(query, queryFile1, queryFile2)
    else:
        totalResults=searchResults
        requestQuery()

def storeResult(queryFile1, endedAt):
    lastSearch= open(queryFile1,"w")
    lastSearch.write(str(endedAt))
    lastSearch.close()

print('Welcome to Webscrapper tool!\nPress Enter to Webscrape / Press H for help')
userInput=msvcrt.getch()
if userInput==b'h':
    Help()
    input('\nPress Enter to Webscrape')
    requestQuery()
else:
    requestQuery()