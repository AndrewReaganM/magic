from urllib.request import urlopen
import time
import yaml

def readURL(url):
    start_time = time.time()
    f = urlopen(url)
    myfile = f.read()
    end_time = time.time()
    return str(int(round((end_time-start_time)*1000, 0))) + "ms - " + url + "\n"

stream = open("sites.yaml", "r")
docs = yaml.load(stream, Loader=yaml.FullLoader)

outputfile = open("outputfile.txt", "w")

for doc in docs['sites']:
    try:
        outputfile.write(readURL(doc))
    except:
        outputfile.write("Timeout Error on " + doc)
