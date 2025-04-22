from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # This assumes your HTML file is in a folder called 'templates'

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask server
