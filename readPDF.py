import PyPDF2 
import textract 
import re

def remove_non_utf(text):
    return ' '.join([word.encode('ascii', 'ignore').decode('ascii') for word in text.split()])

def clean_text(text):
  text = text.decode('ascii') if 'byte' in str(type(text)) else text
  pattern = '(\.|!|-|_|/|,|:|\\|;)' + '{1,}'   #Remove multiple occurances of punctuation marks by single
  text = re.sub(pattern, r'\1', text) 
  text = re.sub(r'\s+([?.!"])', r'\1', text)    #Removes multiple spaces occuring together
  return remove_non_utf(text)

def extract_text(path):
    ''' This method extracts text from pdf.
    If PDF is generated from image file or scanning or an OCR, 
    then separate logic is used.
    Also there're issues with tesseract on windows.
    If that's the case, user would be diplayed a friendly error message'''
    pdfReader = PyPDF2.PdfFileReader(path)
    num_pages = pdfReader.numPages
    count = 0
    text = ""#The while loop will read each page.
    while count < num_pages:
        pageObj = pdfReader.getPage(count)
        count +=1
        text += pageObj.extractText()#This if statement exists to check if the above library returned words. It's done because PyPDF2 cannot read scanned files.if text != "":
    if text != '':
        text = text #If the above returns as False, we run the OCR library textract to #convert scanned/image based PDF files into text.else:
    else:
        try:
            text = textract.process(path, method='tesseract', language='eng')
        except Exception as e:
            return None
    return text