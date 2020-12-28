import texthero as hero
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

''' Method to clean original text
 This text could not be cleaned earlier since 
 Sequence Generation requires minimum preproccessing
 Takes text as input and calls another method to return image'''

def clean_data_and_generate_word_cloud(text):
    df = pd.DataFrame({'text':text}, index=[0])
    df['clean_content'] = hero.clean(df.text)
    return get_word_cloud_image(df)

''' Generate word cloud using texthero
and matplotlib convert the returned figure from word cloud to image''' 
def get_word_cloud_image(df):
    hero.wordcloud(df.clean_content, max_words=100, height=500, width=500, return_figure= True)
    img = BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return plot_url