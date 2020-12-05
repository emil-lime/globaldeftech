import seaborn
import matplotlib.ticker as ticker
import matplotlib.cm as cm
import matplotlib as mpl
from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
from wordcloud import WordCloud 

def word_cloud(data, target):
    all_words = ''.join([text for text in data])
    wordcloud = WordCloud(width=800, height=500, random_state=21, max_font_size=110).generate(all_words) 
    plt.figure(figsize=(10, 7)) 
    plt.imshow(wordcloud, interpolation="bilinear") 
    plt.axis('off') 
    plt.savefig(f'static/{target}.png', bbox_inches='tight')

def pie_chart(data):

    labels = 'Positive', 'Neutral', 'Negative'
    num_pos = len(data['label'][data['label'] == 2])
    num_neut = len(data['label'][data['label'] == 1])
    num_neg = len(data['label'][data['label'] == 0])
    sizes = [num_pos, num_neut, num_neg]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
    ax1.axis('equal') 
    plt.savefig(f'static/pie.png', bbox_inches='tight')