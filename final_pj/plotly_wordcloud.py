import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import  Counter
import plotly.graph_objs as go
import ast

def plotly_wordcloud(df1, df2):

    fig, ax = plt.subplots(nrows=1, ncols=2)
    font_path = '/usr/share/fonts/NanumGothic.ttf'

    word_cross = []
    tmp = []

    for idx, df in enumerate([df1, df2]):
        hash_tags = []
        for words in df['hashtag']:
            try:
                tmp = ast.literal_eval(words)
            except:
                continue
            hash_tags += tmp

        common_words = Counter(hash_tags).most_common(20)
        wc = WordCloud(font_path = font_path, max_font_size=50, background_color='white')
        cloud = wc.generate_from_frequencies(dict(common_words))
    
        
        ax[idx].imshow(cloud)
        # ax[idx].set_title(df['channel'].unique()[0], color = 'white')
        ax[idx].axis('off')
        ax[idx].set_facecolor('white')
        
        # for key in dict(common_words).keys():
        #     if idx == 0:
        #         tmp.append(key)
        #     else:
        #         if key in tmp:
        #             word_cross.append(key)

    fig.patch.set_alpha(0)  
    
    return fig
    # return fig, word_cross