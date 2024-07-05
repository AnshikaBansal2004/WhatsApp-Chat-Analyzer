from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd

def analyze_sentiment(df):
    sia = SentimentIntensityAnalyzer()
    
    # Apply VADER sentiment analysis to each message
    df['Sentiment'] = df['Message'].apply(lambda x: sia.polarity_scores(x)['compound'])
    
    # Classifying the sentiments
    df['Sentiment_Class'] = df['Sentiment'].apply(lambda score: 'Positive' if score > 0 else ('Negative' if score < 0 else 'Neutral'))
    df_sentiment = pd.DataFrame(df)
    
    return df_sentiment

