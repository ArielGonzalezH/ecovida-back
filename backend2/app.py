from flask import Flask
app = Flask(__name__)

@app.route('/api/v2/')
def hello():
    return 'Hello from Backend 2'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000)
