from flask import Flask
import random
app = Flask(__name__)

@app.route("/")
def hello():
    return str(random.randint(1, 1000000))

if __name__ == "__main__":
    app.run(host='0.0.0.0')
