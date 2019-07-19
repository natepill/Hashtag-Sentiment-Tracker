from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def landing_page():

    # NOTE: CSS linkage is using absolute path, may cause issue during deployment
    return render_template('index.html')

@app.route('/chart_visualization')
def show_chart():
    print("In chart chart_visualization")
    return "HELLO WORLD!!!!"

if __name__ == "__main__":
    app.run(debug=True, port=33507)
