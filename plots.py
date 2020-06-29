from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np

def wordClouds(texts,countries):

    fig = plt.figure(figsize=(10,10))
    for i in range(0,len(countries)):
        ax = fig.add_subplot(5,2,i+1)
        wordcloud = WordCloud(max_words=50,
                background_color ='white',
                min_font_size = 10).generate(texts[i])

        ax.imshow(wordcloud)
        ax.axis('off')
    plt.subplots_adjust(wspace=0, hspace=0.1)
    plt.show()

def showEntities(entities,countries):
    print(entities)
    # set width of bar

    color_list = ['b', 'g', 'r', 'k', 'y','c','m','gray','navy']
    gap = .8 / len(entities)
    for i, row in enumerate(entities):
        X = np.arange(len(row))
        plt.bar(X + i * gap, row, label=countries[i],
            width = gap, color = color_list[i % len(color_list)])

    # # Add xticks on the middle of the group bars
    plt.xlabel('Entities', fontweight='bold')

    plt.xticks([r + gap*2 for r in range(len(entities[0]))], ['named', 'money', 'location', 'time', 'organistation'])
    #
    # # Create legend & Show graphic
    plt.legend()
    plt.show()

def heatmap(x_labels, y_labels, values):
    fig, ax = plt.subplots()
    im = ax.imshow(values)

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(x_labels)))
    ax.set_yticks(np.arange(len(y_labels)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(x_labels)
    ax.set_yticklabels(y_labels)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", fontsize=10,
         rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(y_labels)):
        for j in range(len(x_labels)):
            text = ax.text(j, i, "%.2f"%values[i, j],
                           ha="center", va="center", color="w", fontsize=6)

    fig.tight_layout()
    plt.show()

def showReadabilityPlot(readabilities,countries):
    print(readabilities)
    # set width of bar

    color_list = ['b', 'g', 'r', 'k', 'y','c','m','gray','navy']
    gap = .8 / len(readabilities)
    for i, row in enumerate(readabilities):
        X = np.arange(len(row))
        plt.bar(X + i * gap, row, label=countries[i],
            width = gap, color = color_list[i % len(color_list)])
    plt.xlabel('Readability Scores', fontweight='bold')

    plt.xticks([r + gap*2 for r in range(len(readabilities[0]))], ['flesch_reading_ease', 'flesch_kincaid_grade', 'SMOG'])
    #
    # # Create legend & Show graphic
    plt.legend()
    plt.show()