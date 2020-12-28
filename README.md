# Text-Summarization-and-Headline-Generation-Using-T5

Flask based restful api that takes a pdf file from user as input and performs text summarization and headline generation. Both these tasks are very similar at the core. 
Capturing the gist of text in minimum words possible. Length of words and thus the words chosen to summarize differentiates between the two.

There are two types of text summarization techniques:
<ul><li>Extractive Summarization</li>
  <li>Abstractive Summarization</li></ul>
  Extractive summarization means identifying important sections of the text and<b> generating them verbatim producing a subset of the sentences from the original text</b> while Abstractive summarization reproduces <b>important material in a new way after interpretation and examination of the text using advanced natural language</b>

# Relevance of Text Summarization
Text summarization refers to the technique of shortening long pieces of text. The intention is to create a coherent and fluent summary having only the main points outlined in the document.

Automatic text summarization methods are greatly needed to address the ever-growing amount of text data available online to both better help discover relevant information and to consume relevant information faster. And with heading, we don't even need to go through summarized piece of text if heading is not of our interest. 

And ofcoarse the better headings, the more people would be glued to the text. It is even more relevant in this digital era with lots of information floating all around us 

# Choice of Model
With such increasing number of transformer models, we're often left in a dilemma to make a choice here. BERT has been one of the most widely used SOTA NLP models. But due to the way it has been trained, it can just perform Extractive Summarization.

Another competing transformer model is <b> Google's T5</b> which provides Abstractive Summarization (a more radical approach to summarization!). Not just this, T5 follows most radical and simplistic approach for fine tuning for the different nlp tasks. 

It's a text to text transformer. Whatever the task is, input and output are both sequence of text along with a flag in input to tell what task do we need to fine tune it for.
T5 (Text-to-Text Transfer Transformer) is pre-trained on several unsupervised and supervised objectives, such as token and span masking, as well as translation, classification, reading comprehension, and summarization. Importantly, each objective is treated as a language-generation task, where the model is conditioned to generate the correct output based on a textual prompt included in the input sequence

# Problem Solving Approach
<ul><li>Text Extraction From PDF</li>
  using Textract since that's the only library that works for both normal and ocr pdfs without converting it into image files
  <li> Text Summarization </li>
  Since T5 is trained on such a large corpus, it is sufficient to use T5 pretrained model for <b>non domain specific</b> needs.
  <li> Heading Generation</li>
  For this, the logic for text summarization had to be tweaked a bit. Text Summarization produces a summary of about 30-100 words, but for headings I had to fine tune T5 to generate summarization for a length of maximum 20 words. Thus, it fetched us the headings.
  
  For analysis on heading prediction, do check out the file "Predictions.csv".
  <li>Word Cloud for Actual Text</li>
  For this, I'm using texthero since it's fast and provides a vast variety of preprocessing steps. Though it's better sometimes to use custom preprocessing pipeline, especially when there are words in your native languages in the corpus. Due to derth of time, I went ahead with this!
  
  After cleaning, word cloud is generated using word frequency
  <li>PDF Generation For Results</li>
  There are various libraries for generating pdfs both at frontend and backend. 
  
  My choice is to generate pdf at the front end since we already have response so why add latency for going back to server for pdf generation.</ul>

# Assumption
Since it's a simple poc, I've mostly considered a happy path as far as user input is concerned. It's assumed the pdf user provides is a simple text preferably for maximum 520 characters. 
Although code is capable of handling OCR pdfs as well.

# Time to Walk through the Code

Create a conda environment

conda create --name summary-headline-generation

conda activate summary-headline-generation


Install libraries

pip install -r requirements.txt


Model Generation for Headlines

Execute HeadLinesGeneration-T5.ipynb so as to fine tune T5 for generating headings. 

Make sure the torch version and device type used while developing the model is same as the one used while making predictions


Start the server

Start flask rest server (rest server run on localhost:4555): python run.py The server will start on the address http://127.0.0.1:4555


Call REST API

Since it's developed with flask template. It already has the most minimilistic UI for uploading.

After the pdf gets uploaded successfully, user is shown the heading, summary and word cloud and user would also be given the facility to download the results in pdf.


To execute unit tests:

Start flask rest server (rest server run on localhost:4555): python run.py

Run unittest: python rest_tester.py
