from flask import Flask

app = Flask(__name__)

@app.route('/',methods=['GET'])
def root():
    return '<h1>App is running</h1>'


@app.route('/ingest/<index>',methods=['POST'])
def ingestDoc():
    return '<h1>Feature is under development</h1>'


if __name__=='__main__':
    app.run(debug=True)
