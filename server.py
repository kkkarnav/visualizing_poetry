from flask import Flask, render_template, request, redirect, url_for
from final_project import main
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/output')
def output():
    images = []
    for image in os.listdir("static"):
        if image.endswith(".png"):
            images.append(""+image)
    print(images)
    return render_template('output.html', images=images)


@app.route('/run_script', methods=['POST'])
def run_script():
    length = (request.form.get('length'))
    print(length)
    length = int(length)
    main(length)

    return redirect("/output", code=302)


if __name__ == '__main__':
    app.run(debug=True)
