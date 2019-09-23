from urllib.request import urlopen
import time
import yaml

def readURL(url):
    start_time = time.time()
    f = urlopen(url, timeout=3)
    myfile = f.read()
    end_time = time.time()
    return str(int(round((end_time-start_time)*1000, 0))) + "ms - " + url + "\n"

print("Testing URLs...")
stream = open("sites.yaml", "r")
docs = yaml.load(stream, Loader=yaml.FullLoader)

outputfile = open("outputfile.txt", "w")

for doc in docs['sites']:
    print("Testing " + doc)
    try:
        outputfile.write(readURL(doc))
    except:
        outputfile.write("Timeout Error on " + doc + "\n")

print("Testing Complete.\nResults written to outputfile.txt")
