!pip install transformers

from transformers import pipeline
import pandas as pd
import numpy as np
from joblib import Parallel, delayed
import multiprocessing
import warnings

# Ignore the specific UserWarning related to resource_tracker
warnings.filterwarnings("ignore", category=UserWarning, message="resource_tracker: There appear to be")



# Function to initialize the classifier inside the parallel process
def init_classifier():
    return pipeline('sentiment-analysis', model="distilbert-base-uncased-finetuned-sst-2-english")

# Function to analyze sentiment in batches and return labels and scores
def analyze_sentiment_in_batches(classifier, texts, batch_size=32):
    results = classifier(texts, batch_size=batch_size)
    labels = [result['label'] for result in results]
    scores = [result['score'] for result in results]
    return labels, scores

# Function to process a slice of the DataFrame
def process_slice(df_slice, batch_size):
    classifier = init_classifier()
    texts = df_slice['feedback'].tolist()
    labels, scores = analyze_sentiment_in_batches(classifier, texts, batch_size)
    return labels, scores

df = pd.read_csv('feedback_data.csv')

n_cores = multiprocessing.cpu_count() - 1  # Leave one core free for other operations

# Adjust the batch size according to your system's capabilities
batch_size = 16  # You may need to reduce this if you encounter memory issues

# Ensure not to exceed the number of chunks over the number of data rows
n_chunks = min(len(df), n_cores)

chunks = np.array_split(df, n_chunks)
results = Parallel(n_jobs=n_chunks)(delayed(process_slice)(chunk, batch_size) for chunk in chunks)

labels, scores = zip(*results)
df['Sentiment'] = [label for sublist in labels for label in sublist]
df['Confidence'] = [score for sublist in scores for score in sublist]

df.to_csv('feedback_data_with_sentiment.csv', index=False)

print("Sentiment analysis completed and saved to feedback_data_with_sentiment.csv")
