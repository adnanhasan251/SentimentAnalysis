import requests
import pandas as pd
from datetime import datetime
from textblob import TextBlob
import time
import os
import csv

BASE_URL = "https://saurav.tech/NewsAPI/"
CATEGORY = "business"
COUNTRY = "in"

def load_tickers_from_csv(file_path):
    symbol_to_company = {}
    company_to_symbol = {}
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 2:
                symbol, company_name = row
                symbol_to_company[symbol.lower()] = company_name
                company_to_symbol[company_name.lower()] = symbol
    return symbol_to_company, company_to_symbol

symbol_to_company, company_to_symbol = load_tickers_from_csv('nyse-listed.csv')

def get_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0.1:
        return 1
    elif polarity < -0.1:
        return -1
    else:
        return 0

def extract_stock_tickers(text):
    found_tickers = []
    text_lower = text.lower()
    for company_name, ticker in company_to_symbol.items():
        if company_name in text_lower:
            found_tickers.append(ticker)
    return found_tickers if found_tickers else ["Unknown"]

def fetch_news_data(page=1):
    url = f"{BASE_URL}top-headlines/category/{CATEGORY}/{COUNTRY}.json?page={page}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])
        processed_articles = []
        
        for article in articles:
            title = article.get('title', '')
            description = article.get('description', '')
            published_at = article.get('publishedAt', '')
            url = article.get('url', '')
            content = article.get('content', '')
            source = article.get('source', {}).get('name', '')
            author = article.get('author', '')
            
            article_text = title + " " + description
            sentiment = get_sentiment(article_text)
            tickers = extract_stock_tickers(article_text)
            
            for ticker in tickers:
                row = {
                    'Date_Collected': datetime.now().strftime("%d-%m-%Y"),
                    'Sentiment_Label': sentiment,
                    'Stock_Ticker': ticker,
                    'Headline': title,
                    'Description': description,
                    'Article_Content': content if content else '',
                    'URL': url if url else '',
                    'Source': source if source else '',
                    'Author': author if author else '',
                    'Published_Date': published_at if published_at else '',
                    'Additional_Info': '',
                }
                processed_articles.append(row)
        
        return processed_articles
    else:
        return []

def collect_articles(target_row_count=1000):
    all_articles = []
    page = 1
    
    while len(all_articles) < target_row_count:
        articles = fetch_news_data(page)
        
        if not articles:
            break
        
        all_articles.extend(articles)
        
        page += 1
        time.sleep(1)

        if len(all_articles) >= target_row_count:
            break

    return all_articles[:target_row_count]

def save_to_csv(articles, folder_path="RTGCN/data", file_name="stock_sentiment_data.csv"):
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, file_name)
    
    df = pd.DataFrame(articles)
    df.to_csv(file_path, index=False, mode="w", header=True)

articles = collect_articles(target_row_count=1000)
save_to_csv(articles)
