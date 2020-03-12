from werkzeug.utils import secure_filename
from flask import Flask, jsonify, render_template, request, redirect, make_response
app = Flask(__name__)
import os

#Location of where the images will be saved, and types of images 
app.config["IMAGE_UPLOADS"] = "images"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]

@app.route("/")
def hello():
    return jsonify({"content" : "Hello World!"})

if __name__ == '__main__':
    app.run(debug=True)

#Check if uploaded image is valid, via the extension
def allowedImages(filename):

    #ensure it has extension
    if not "." in filename:  
        return False
    
    #remove extension
    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

#Route to upload image
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if request.files:
            #"image" is the name given to the input field in the html
            image = request.files["image"]

            if image.filename == "":
                print("No Filename")
                return redirect(request.url)
            
            #check if image is of right type and secure the name (removes path is associated with filename) if it is
            if allowedImages(image.filename):
                filename = secure_filename(image.filename)
                print(filename, flush=True)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                return redirect(request.url)
            else:
                print("The file extension is not allowed")
                return redirect(request.url)

    return render_template("upload_image.html")