# Stock Sentiment Analysis from News Articles

This project fetches business news articles, performs sentiment analysis, identifies associated stock tickers, and stores the processed data in a structured CSV file. It's designed to analyze the sentiment of articles and link them to stock market symbols for financial insights.

## Features

- Fetches news articles using a REST API.
- Performs sentiment analysis using `TextBlob`.
- Extracts stock tickers mentioned in article titles and descriptions.
- Saves processed data into a CSV file for further analysis.

## Setup

### Prerequisites
- Python 3.7 or higher
- Install dependencies from `requirements.txt`:
  ```bash
  pip install -r requirements.txt
