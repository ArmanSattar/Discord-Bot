# imported the requests library 
import requests
import time
from bs4 import BeautifulSoup as bs

fileType = '.pptx'
counter = 0
path = 'https://www.drfrostmaths.com/getfile.php?fid='
listOfNames = [
    'Algebraic Expressions' + fileType,
    'Quadratics' + fileType,
    'Equations and Inequalities' + fileType,
    'Graphs and Inequalities' + fileType,
    'Straight Line Graphs' + fileType,
    'Circles' + fileType,
    'Algebraic Methods' + fileType,
    'Binomial Expansion' + fileType,
    'Trigonometric Ratios' + fileType,
    'Trigonometric Identities' + fileType,
    'Vectors' + fileType,
    'Differentiation' + fileType,
    'Integration' + fileType,
    'Exponentials and Logarithms' + fileType,
]
listOfLinks = [
    path + '1025',
    path + '1026',
    path + '1027',
    path + '1028',
    path + '1029',
    path + '1030',
    path + '1350',
    path + '1032',
    path + '1033',
    path + '1082',
    path + '1035',
    path + '814',
    path + '788',
    path + '857', 
]

# URL of the image to be downloaded is defined as image_url
# create HTTP response object 

# send a HTTP request to the server and save 
# the HTTP response in a response object called r
for paths in listOfLinks:
    #opens a new file and lets you manipulate it with f
    with open(listOfNames[counter], 'wb') as f: 

        r = requests.get(paths) 
        f.write(r.content)

    counter += 1
    time.sleep(1)
