# MAG(i)C Random in Java on Google App Engine

## Overview
The Google App Engine version of the MAG(i)C Random Number Generator is virtually effort free to deploy.

## Prerequisites
* Google App Engine Account with valid billing
* Google Cloud SDK
* MAG(i)C Random Number code from Git repository

## Software Versions
The MAG(i)C Random Number Generator in Python relies on:
* Python 3.7
* Flask 1.0.2

Keep in mind that you may have success running other versions, however it is not guaranteed to work.

## Installing Google Cloud SDK
To install the Cloud SDK, using [Google's Documentation](https://cloud.google.com/sdk/docs/).

## Installing on App Engine
To install the web application onto App Engine, make sure that you have a clean project on Google Cloud Console.

### Step 1: Clone magic Folder from GitHub
```bash
$ cd /desired_parent_directory/
$ sudo git clone https://github.com/AndrewReaganM/magic.git
```

### Step 2: Navigate to the python_appengine Folder
```bash
$ cd /desired_parent_directory/magic/python_appengine/
```

### Step 3: Run the App Engine Deploy Command
```bash
$ gcloud app deploy
```
After running this command, you may need to link your Google account to your Cloud SDK installation. The deploy command above will walk you through this.

# Explanations of Files
This project consists of very few files, but the below sections outline the purpose of each of them.
## Application Backend
The application is very simple, here is a snippet of the main functionality:
```Python
app = Flask(__name__)

@app.route('/')
def hello():
    """Return a random integer as a string"""
    return str(random.randint(1,1000000))
```
This will be uploaded to App Engine and be ran when web requests come in.

## Google App Engine Configuration (app.yaml)
To tell App Engine what to do, we need an app.yaml file. These can be complex for large projects, but the file for Random is very simple.
```
runtime: python37
```
This simply tells App Engine that the program runs on Python 3.7.

## App Engine Requirements (requirements.txt)
This file tells App Engine what version of other dependencies we need for the app to function. For Random, we only need Flask.
```
Flask==1.0.2
```
