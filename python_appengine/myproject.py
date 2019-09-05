from flask import Flask
import random
app = Flask(__name__)

@app.route("/")
def hello():
    return str(random.randint(0, 1000000))


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
