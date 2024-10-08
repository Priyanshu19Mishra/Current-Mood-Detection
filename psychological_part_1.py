# -*- coding: utf-8 -*-
"""Psychological Part 1

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zihpKblZVLsXW8VCEhxTIDPKnkfVJC0K
"""

from google.colab import drive
drive.mount('/content/drive')

import os
os.chdir('/content/drive/MyDrive/Data')

import pandas as pd

"""Creating Combined Dataset"""

depression_data = pd.read_csv('Depression.csv')
mental_health_twitter_data = pd.read_csv('Mental health twitter.csv')
mental_health_data = pd.read_csv('Mental health.csv')
reddit_mental_health_data = pd.read_csv('Reddit mental health.csv')
stress_data = pd.read_csv('Stress.csv')

print(depression_data.head())
print(mental_health_twitter_data.head())
print(mental_health_data.head())
print(reddit_mental_health_data.head())
print(stress_data.head())

label_mapping = {
    'depressed': 'depressed',
    'not depressed': 'not depressed',
    'mental': 'mental',
    'non-mental': 'non-mental',
    'stress': 'stress',
    'no stress': 'no stress',
    'bipolar disorder': 'bipolar disorder',
    'personality disorder': 'personality disorder',
    'anxiety': 'anxiety'
}

depression_data['label'] = depression_data['label'].map(label_mapping)
mental_health_twitter_data['label'] = mental_health_twitter_data['label'].map(label_mapping)
mental_health_data['label'] = mental_health_data['label'].map(label_mapping)
reddit_mental_health_data['label'] = reddit_mental_health_data['label'].map(label_mapping)
stress_data['label'] = stress_data['label'].map(label_mapping)

combined_data = pd.concat([
    depression_data,
    mental_health_twitter_data,
    mental_health_data,
    reddit_mental_health_data,
    stress_data
], ignore_index=True)

combined_data = combined_data.sample(frac=1).reset_index(drop=True)

print(combined_data.head())
print(combined_data['label'].value_counts())

combined_data.to_csv('combined_mental_health_dataset.csv', index=False)

"""Visualization of the dataset"""

import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

combined_data = pd.read_csv('combined_mental_health_dataset.csv')

combined_data.head()

combined_data.shape

plt.figure(figsize=(12, 6))
sns.countplot(y='label', data=combined_data, palette='viridis', order=combined_data['label'].value_counts().index)
plt.title('Distribution of Labels')
plt.xlabel('Count')
plt.ylabel('Label')
plt.show()

!pip install matplotlib seaborn wordcloud

combined_data = combined_data.dropna(subset=['text'])

combined_data.shape

labels = combined_data['label'].unique()
plt.figure(figsize=(20, 30))
for i, label in enumerate(labels):
    plt.subplot(len(labels), 1, i + 1)
    text = ' '.join(combined_data[combined_data['label'] == label]['text'].astype(str))
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(f'Word Cloud for {label}')
    plt.axis('off')
plt.show()

combined_data['text_length'] = combined_data['text'].apply(lambda x: len(x.split()))

plt.figure(figsize=(12, 6))
sns.histplot(data=combined_data, x='text_length', hue='label', multiple='stack', palette='viridis')
plt.title('Text Length Distribution by Label')
plt.xlabel('Text Length (Number of Words)')
plt.ylabel('Count')
plt.show()

"""Pre-Processing the dataset"""

import re
from transformers import BertTokenizer

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

combined_data['text'] = combined_data['text'].apply(preprocess_text)

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def tokenize_text(text):
    return tokenizer(text, padding='max_length', truncation=True, max_length=128, return_tensors='pt')

combined_data['tokenized_text'] = combined_data['text'].apply(tokenize_text)

combined_data['input_ids'] = combined_data['tokenized_text'].apply(lambda x: x['input_ids'].squeeze().tolist())
combined_data['attention_mask'] = combined_data['tokenized_text'].apply(lambda x: x['attention_mask'].squeeze().tolist())

print(combined_data.head(20))

