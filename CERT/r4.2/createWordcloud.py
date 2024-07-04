#!/usr/bin/env python
"""
Minimal Example
===============

#Generating a square wordcloud from the US constitution using default arguments.
"""

import os

from os import path
from wordcloud import WordCloud

# get data directory (using getcwd() is needed to support running example in generated IPython notebook)

path = os.getcwd()
file_name = path+'\\Outputs\\joinedWebAccess_1.csv'#'joinedEmails_1.csv'

# Read the whole text.
text = open(file_name, encoding='utf-8').read()

# Generate a word cloud image
wordcloud = WordCloud(collocations=False).generate(text)

# Display the generated image:
# the matplotlib way:
# import matplotlib.pyplot as plt
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis("off")

# lower max_font_size
# wordcloud = WordCloud(max_font_size=40).generate(text)
# plt.figure()
# plt.imshow(wordcloud, interpolation="bilinear")
# plt.axis("off")
# plt.show()

# The pil way (if you don't have matplotlib)
image = wordcloud.to_image()
image.show()