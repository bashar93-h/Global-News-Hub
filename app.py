import os
from flask import Flask, render_template, request, redirect, url_for
import requests
from dotenv import load_dotenv
from translations.translations import TRANSLATIONS
import math

load_dotenv()
GUARDIAN_API_KEY = os.getenv("GUARDIAN_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWSAPI_KEY = os.getenv('NEWSAPI_KEY')
GNEWS_API_KEY = os.getenv('GNEWS_API_KEY')

app = Flask(__name__)


# Category mappings
GUARDIAN_CATEGORIES = {
    'world': 'world',
    'sports': 'sport',
    'politics': 'politics',
    'technology': 'technology',
    'entertainment': 'culture',
    'business': 'business',
    'health': 'society',
    'science': 'science',
    'travel': 'travel'
}

NEWSAPI_CATEGORIES = {
    'world': 'general',
    'sports': 'sports',
    'politics': 'general',
    'technology': 'technology',
    'entertainment': 'entertainment',
    'business': 'business',
    'health': 'health',
    'science': 'science',
    'travel': 'general'
}



def fetch_guardian_news(query='world', category=None, page=1, page_size=20):
    """Fetch from Guardian API (English only, unlimited)"""
    url = 'https://content.guardianapis.com/search'
    
    params = {
        'api-key': GUARDIAN_API_KEY,
        'show-fields': 'thumbnail,trailText,bodyText,body',
        'page-size': page_size,
        "page": page,
        'order-by': 'newest'
    }
    
    # Add category if provided
    if category and category in GUARDIAN_CATEGORIES:
        params['section'] = GUARDIAN_CATEGORIES[category]
    
    # Add search query
    if query and query != 'world':
        params['q'] = query
    
    try:
        r = requests.get(url, params=params, timeout=10)
        print(f"Guardian Status: {r.status_code}")
        
        if r.ok:
            data = r.json()
            results = []
            
            total_results = data.get('response', {}).get('total', 0)
            print(f"📊 Total available: {total_results}")
            
            for item in data.get('response', {}).get('results', []):
                fields = item.get('fields', {})
                results.append({
                    'title': item.get('webTitle', ''),
                    'description': fields.get('trailText', 'No description available'),
                    'content': fields.get('bodyText', ''),
                    'content_html': fields.get('body', ''),
                    'link': item.get('webUrl', ''),
                    'image_url': fields.get('thumbnail', ''),
                    'pubDate': item.get('webPublicationDate', ''),
                    'source_id': 'The Guardian',
                    'author': item.get('tags', [{}])[0].get('webTitle', '') if item.get('tags') else ''
                })
            
            print(f"✅ Guardian articles: {len(results)}")
            return results, total_results
    except Exception as e:
        print(f"❌ Guardian error: {e}")
    
    return []


def fetch_gnews_news(query='world', category=None, lang='en', page=1, page_size=20):
    """Fetch from GNews API (Better multi-language support)"""
    url = 'https://gnews.io/api/v4/top-headlines'
    
    params = {
        'token': GNEWS_API_KEY,
        'lang': lang,
        'max': page_size,
        'page': page
    }
    
    # Add category
    if category and category in NEWSAPI_CATEGORIES:
        params['topic'] = NEWSAPI_CATEGORIES[category]
    
    # Add search query
    if query and query != 'world':
        url = 'https://gnews.io/api/v4/search'
        params['q'] = query
    
    try:
        r = requests.get(url, params=params, timeout=10)
        print(f"📊 GNews Status: {r.status_code}")
        
        if r.ok:
            data = r.json()
            results = []
            
            total_results = data.get('totalArticles', 0)
            print(f"📊 Total available: {total_results}")
            
            for item in data.get('articles', []):
                results.append({
                    'title': item.get('title', ''),
                    'description': item.get('description', 'No description available'),
                    'content': item.get('content', ''),
                    'link': item.get('url', ''),
                    'image_url': item.get('image', ''),
                    'pubDate': item.get('publishedAt', ''),
                    'source_id': item.get('source', {}).get('name', 'Unknown')
                })
            
            print(f"✅ GNews articles: {len(results)}")
            return results, total_results
    except Exception as e:
        print(f"❌ GNews error: {e}")
    
    return []

def fetch_newsapi_news(query='world', category=None, lang='en', page=1, page_size=20):
    """Fetch from NewsAPI (Multiple languages, 100/day limit)"""
    
    # Language to country mapping for NewsAPI
    LANG_TO_COUNTRY = {
        'en': 'us',
        'ar': 'sa',  # Saudi Arabia
        'es': 'es',  # Spain
        'fr': 'fr',  # France
        'de': 'de'   # Germany
    }
    
    url = 'https://newsapi.org/v2/top-headlines'
    
    params = {
        'apiKey': NEWSAPI_KEY,
        'pageSize': page_size,
        'page': page,
        'country': LANG_TO_COUNTRY.get(lang, 'us')  # Use country instead of language
    }
    
    # Add category (works with country parameter)
    if category and category in NEWSAPI_CATEGORIES:
        params['category'] = NEWSAPI_CATEGORIES[category]
    
    # Add search query (use 'everything' endpoint for search with language)
    if query and query != 'world':
        url = 'https://newsapi.org/v2/everything'  # Switch to 'everything' for search
        params = {
            'apiKey': NEWSAPI_KEY,
            'q': query,
            'language': lang,
            'pageSize': page_size,
            'page': page,
            'sortBy': 'publishedAt'
        }
    
    try:
        r = requests.get(url, params=params, timeout=10)
        print(f"NewsAPI Status: {r.status_code}")
        print(f"NewsAPI URL: {url}")
        print(f"NewsAPI Params: {params}")
        
        if r.ok:
            data = r.json()
            results = []
            
            total_results = data.get('totalResults', 0)
            print(f"📊 Total available: {total_results}")
            
            for item in data.get('articles', []):
                # Skip articles with [Removed] titles
                if item.get('title') == '[Removed]':
                    continue
                    
                results.append({
                    'title': item.get('title', ''),
                    'description': item.get('description', 'No description available'),
                    'content': item.get('content', ''),
                    'link': item.get('url', ''),
                    'image_url': item.get('urlToImage', ''),
                    'pubDate': item.get('publishedAt', ''),
                    'source_id': item.get('source', {}).get('name', 'Unknown'),
                    'author': item.get('author', '')
                })
            
            print(f"NewsAPI articles: {len(results)}")
            return results, total_results
        elif r.status_code == 429:
            print(" NewsAPI rate limit exceeded")
        else:
            print(f"NewsAPI Error Response: {r.text}")
    except Exception as e:
        print(f"NewsAPI error: {e}")
    
    return []

def fetch_articles(query='world', page=1, lang='en', page_size=20, category=None):
    """Main function - routes to appropriate API based on language"""
    
    if lang == 'en':
        # Use Guardian for English (unlimited)
        articles, total = fetch_guardian_news(query, category, page, page_size)
        
        # Fallback to NewsAPI if Guardian fails
        if not articles:
            print("⚠️ Guardian failed, trying NewsAPI...")
            articles, total = fetch_newsapi_news(query, category, lang, page, page_size)
    else:
        # Use NewsAPI for other languages
        articles, total = fetch_newsapi_news(query, category, lang, page, page_size)
        
        # Fallback to GNews if NewsAPI fails
        if not articles:
            print("⚠️ NewsAPI failed, trying GNews...")
            articles, total = fetch_gnews_news(query, category, lang, page, page_size)
    
    print(f"Total articles to display: {len(articles)}")
    return articles, total

@app.route('/')
def home():
    q = request.args.get("q", "world")
    page = int(request.args.get("page", 1))
    lang = request.args.get("lang", 'en')
    articles, total = fetch_articles(query=q, page=page, lang=lang)
    page_size = 20
    total_pages = math.ceil(total / page_size)

    translations = TRANSLATIONS.get(lang, TRANSLATIONS['en'])
    
    return render_template("index.html", articles=articles, query=q, page=page, lang=lang, total_pages=total_pages, t=translations)

# ADD THIS ROUTE FOR CATEGORIES
@app.route('/category/<category>')
def category_page(category):
    q = request.args.get("q", category)
    page = int(request.args.get("page", 1))
    lang = request.args.get("lang", 'en')
    articles, total = fetch_articles(query=q, page=page, lang=lang, category=category)
    
    page_size = 20
    total_pages = math.ceil(total / page_size)
    
    translations = TRANSLATIONS.get(lang, TRANSLATIONS['en'])

    return render_template("index.html", articles=articles, query=category, page=page, lang=lang, category=category, total_pages=total_pages, t=translations)

@app.route('/article')
def article():
    url = request.args.get("url")
    lang = request.args.get("lang", 'en')
    if not url:
        return redirect(url_for('home'))
    
    translations = TRANSLATIONS.get(lang, TRANSLATIONS['en'])
    
    article = {
        'title': request.args.get('title', 'Article'),
        'description': request.args.get('description', ''),
        'link': url,
        'image_url': request.args.get('image', ''),
        'source_id': request.args.get('source', 'Unknow'),
        'pubDate': request.args.get('date', ''),
        'author': request.args.get('author', ''),
        'content': request.args.get('content', ''),
    }
    return render_template("article.html", article=article, lang=lang, t=translations)


if __name__ == "__main__":
    app.run(debug=True)