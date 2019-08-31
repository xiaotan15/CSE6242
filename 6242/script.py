#v3 auth
#9f4669e3cb6c357ae9ca0907fa103a9e
#v4 auth
#eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5ZjQ2NjllM2NiNmMzNTdhZTljYTA5MDdmYTEwM2E5ZSIsInN1YiI6IjViOGY0NmRjMGUwYTI2N2Y2ODAwNTBkMyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.vE0Z6gRLo1QjJgN8wnoH3QQvT7DJs8Y4R-mw3yFLodE
#https://api.themoviedb.org/3/movie/550?api_key=9f4669e3cb6c357ae9ca0907fa103a9e

#Setting up Data
import http.client
import json
import csv
import time
import sys
import re


##codes from the website 
conn = http.client.HTTPSConnection("api.themoviedb.org")
payload = "{}"
#conn.request("GET", "/3/discover/movie?with_genres=35&primary_release_date.gte=2000&page=1&include_video=false&include_adult=false&sort_by=popularity.desc&language=en-US&api_key=9f4669e3cb6c357ae9ca0907fa103a9e", payload)
#res = conn.getresponse()
#data = res.read()
#print(data.decode("utf-8"))


#codes written by myself
#question: a
APIkey = sys.argv[1]
page = 1
movieNumber = 1
myfile = open('movie_ID_name.csv', 'w') #create a csv file in python

while movieNumber <= 300: #start from a smaller number
    conn.request("GET", "/3/discover/movie?with_genres=35&primary_release_date.gte=2000&page=" +str(page) + "&include_video=false&include_adult=false&sort_by=popularity.desc&language=en-US&api_key="+str(APIkey), payload)
    movieList = json.loads(conn.getresponse().read())["results"] ##needs to store it in a json file 
    for movie in movieList:
        if  movieNumber <= 300: 
            movieListLine = "%d, %s \n"%(movie['id'], movie['title']) #extract "id" and "title" from the jason file and store them in one line 
            myfile.write(movieListLine) #add the line to the final file
            movieNumber += 1 
        else:
            break 
    page += 1

myfile.close()
#final product: 353486,Jumanji: Welcome to the Jungle

text_file = open('movie_ID_sim_movie_ID.csv', 'w')

page = 1
movieLimit = 300
movieNumber = 1

while movieNumber <= movieLimit:
    time.sleep(0.5)
    conn.request("GET", "/3/discover/movie?with_genres=35&primary_release_date.gte=2000&page=" +str(page) + "&include_video=false&include_adult=false&sort_by=popularity.desc&language=en-US&api_key="+str(APIkey), payload)
    movieList = json.loads(conn.getresponse().read())["results"]
    page += 1
    for movie in movieList:
        if movieNumber > movieLimit: break
        print("movie id " + str(movie["id"]))
        simNumber = 1
        simPageNum = 1
        while simNumber <= 5:
            #print("----> sim page " + str(simPageNum))
            time.sleep(0.5)
            conn.request("GET", "/3/movie/"+str(movie['id']) +"/similar?page="+str(simPageNum)+"&language=en-US&api_key="+str(APIkey), payload)
            response = conn.getresponse().read()
            #print(response)
            movieSimList = json.loads(response)["results"]
            if len(movieSimList) == 0:
                break
            for sim in movieSimList: 
                if  simNumber <= 5:
                    simListLine = "%d, %s \n"%(movie['id'], sim['id'])
                    text_file.write(simListLine) #add the line to the final file
                    simNumber += 1
                else:
                    break
            simPageNum += 1
        movieNumber += 1

text_file = open('movie_ID_sim_movie_ID.csv', 'r+')
pairs = text_file.read().split('\n')
del pairs[-1]
for pair in pairs:
    numPair = list(map(int, re.findall(r'\d+', pair)))
    reversePair = '<%d, %d>' % (numPair[1],numPair[0])
    if reversePair in pairs and numPair[1] < numPair[0]:
        pairs.remove(pair)

text_file = open('movie_ID_sim_movie_ID.csv','w')
for pair in pairs:
    text_file.write(pair+'\n')
    
##reduce replicates 
text_file.close()

#with open('movie_ID_name.csv', mode = 'r') as myfile:
    #csv_reader = csv.DictReader(myfile)
    #line_count = 0
           


#final product
#A,X
#A,Y
#A,Z
#X,B











