import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import matplotlib.pyplot as plt
import math

example = "This is an example sentence! However, it " \
          "is a very informative one,"

# print(word_tokenize(example, language='english'))

tokenizer = RegexpTokenizer(r'\w+')
# print(tokenizer.tokenize(example))

stop_words = set(stopwords.words('english'))
# print(stop_words)

all_words_pos = []
with open("pos_news_titles.txt", "r", encoding='utf-8',
          errors='ignore') as f_pos:
    for line in f_pos.readlines():
        words = tokenizer.tokenize(line)
        for w in words:
            if w.lower() not in stop_words:
                all_words_pos.append(w.lower())


pos_res = nltk.FreqDist(all_words_pos)
# print(pos_res.most_common(8))

all_words_neg = []
with open("neg_news_titles.txt", "r", encoding='utf-8',
          errors='ignore') as f_neg:
    for line in f_neg.readlines():
        words = tokenizer.tokenize(line)
        for w in words:
            if w.lower() not in stop_words:
                all_words_neg.append(w.lower())

neg_res = nltk.FreqDist(all_words_neg)
# print(neg_res.most_common(8))

# Code for log-log plots
# Not mentioned in the article
plt.style.use('ggplot')

y_val = [x[1] for x in pos_res.most_common(len(all_words_pos))]
y_final = []
for i, k, z, t in zip(y_val[0::4], y_val[1::4], y_val[2::4], y_val[3::4]):
    y_final.append(math.log(i+k+z+t))
x_val = [math.log(i+1) for i in range(len(y_final))]

plt.xlabel("Words (Log)")
plt.ylabel("Frequency (Log)")
plt.title("Word Frequency Distribution (Positive)")
plt.plot(x_val, y_final)
plt.show()

y_val = [x[1] for x in neg_res.most_common(len(all_words_neg))]
y_final = []
for i, k, z in zip(y_val[0::3], y_val[1::3], y_val[2::3]):
    if i+k+z == 0:
        break
    y_final.append(math.log(i+k+z))
x_val = [math.log(i+1) for i in range(len(y_final))]

plt.xlabel("Words (Log)")
plt.ylabel("Frequency (Log)")
plt.title("Word Frequency Distribution (Negative)")
plt.plot(x_val, y_final)
plt.show()
