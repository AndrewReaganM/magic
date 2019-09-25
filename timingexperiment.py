from urllib.request import urlopen
import time
import yaml

def getURL(url):
    return url.split('@')[1]


def readURL(url):
    start_time = time.time()
    f = urlopen(url)
    randnum = f.read()
    end_time = time.time()
    return str(round((end_time-start_time)*1000)) + "ms  " + str(int(randnum))

stream = open("sites.yaml", "r")
docs = yaml.load(stream, Loader=yaml.FullLoader)

outputfile = open("outputfile.txt", "w")

for doc in docs['sites']:
    print(doc, end=' ')
    try:
        print(readURL(getURL(doc)))
    except Exception as e:
        print(e.__class__.__name__ + " raised on " + doc)
