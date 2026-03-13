import requests
from newspaper import Article

def scrape_article(url):
    """Extract article text from a URL"""
    try:
        article = Article(url)
        article.download()
        article.parse()
        
        return {
            "title": article.title,
            "text": article.text,
            "authors": article.authors,
            "publish_date": str(article.publish_date),
            "source": url,
            "success": True
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def get_text_from_input(user_input):
    """Check if input is a URL or plain text"""
    
    if user_input.startswith("http://") or user_input.startswith("https://"):
        # It's a URL - scrape it
        return scrape_article(user_input)
    else:
        # It's plain text - use directly
        return {
            "title": "Manual Input",
            "text": user_input,
            "authors": [],
            "publish_date": "Unknown",
            "source": "Direct Input",
            "success": True
        }