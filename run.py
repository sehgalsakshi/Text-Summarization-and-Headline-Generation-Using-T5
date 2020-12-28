import os
from flask import Flask, render_template, request
import readPDF, word_cloud
import modelInitialization as model_initialize
import predictions

__author__ = 'Sakshi'

# to be executed at start of server
# so that subsequent calls are not affected by this initialization
device, model, heading_model, tokenizer = model_initialize.initialize_model_and_tokenizer()
app = Flask(__name__)
MAX_FILE_SIZE = 2 * 1024 * 1000
OUTPUT_DIR = './output/'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

#method to render the default view for the app
@app.route("/")
def index():
    return render_template("upload.html")

'''method to take input pdf and perform summarization and heading generation 
 and also creates word cloud
 Only allowed method for this is POST'''
@app.route("/proccess_pdf", methods=['POST'])
def proccess_pdf():
    ''' pdf proccessing takes place in following steps:
       1. Extract Text from PDF
       2. Text Summarization with pretrained T5 model
       3. Heading Generation with finetuned T5 model
       4. Word Cloud generated by cleaning the original text and generating it with word frequency.
       5. PDF Generation of result on frontend'''
    try:
        summary = None
        text = None
        title = None
        for file in request.files.getlist("file"):
            if '.pdf' not in file.filename:
                return render_template("upload.html", error="File must be pdf only."), 400
            path = OUTPUT_DIR + file.filename
            file.save(path)  
            if os.stat(path).st_size > MAX_FILE_SIZE:
                return render_template("upload.html", error="File size too large. File Size should be less than or equal to 2MB"), 400
            text = readPDF.extract_text(path)
            if text is None:
                return render_template("upload.html", error="OCR/ PDF with images is not yet supported. Please try with some other pdf"), 400
            summary = predictions.predict(device, model, tokenizer, text)
            title = predictions.predict(device, heading_model, tokenizer, text)
        plot_url = word_cloud.clean_data_and_generate_word_cloud(text)
        return render_template("complete.html", title = title, summary = summary, plot_url = plot_url)
    except Exception as e:
        print(e)
        return ({'Error': str(e)})

if __name__ == "__main__":
    app.run(port=4555, debug=True)