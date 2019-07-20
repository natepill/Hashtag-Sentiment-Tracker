from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/')
def landing_page():
    # NOTE: CSS linkage is using absolute path, may cause issue during deployment
    return render_template('index.html')

@app.route('/get_data')
def start_streaming():
    # Grab user input from url parameter and remove whitespace
    hashtag = request.args.get('hashtag').replace(" ", "")


    return hashtag

if __name__ == "__main__":
    app.run(debug=True, port=33507)
