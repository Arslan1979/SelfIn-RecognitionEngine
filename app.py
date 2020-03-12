
from flask import Flask, jsonify, render_template, request, redirect, make_response
app = Flask(__name__)
import os

#Location of where the images will be saved
app.config["IMAGE_UPLOADS"] = "images"

@app.route("/")
def hello():
    return jsonify({"content" : "Hello World!"})

if __name__ == '__main__':
    app.run(debug=True)

@app.route("/more")
def more():
    return render_template("index.html")

#Route to upload image
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if request.files:
            #"image" is the name given to the input field in the html
            image = request.files["image"]

            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
            #flush is to prevent the print to get stuck in a buffer
            print("image saved", flush=True)
            return redirect(request.url)

    return render_template("upload_image.html")