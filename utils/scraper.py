import requests
from bs4 import BeautifulSoup

def scrape_blog_post(url: str) -> str:
    """
    Scrapes the text content from a given blog post URL.
    Attempts to be generic but works best with standard HTML article tags.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Attempt to find the main article content
        # Common selectors for blog posts
        article = soup.find('article')
        if not article:
            article = soup.find('main')
        if not article:
            article = soup.find('div', class_='post-content') # Generic fallback
        
        # If still nothing, fall back to body but remove script/style
        if not article:
            article = soup.body

        # Remove scripts, styles, navs, footers from the found element
        for element in article(['script', 'style', 'nav', 'footer', 'header', 'iframe', 'aside']):
            element.decompose()

        # Extract text
        text = ' '.join(p.get_text().strip() for p in article.find_all(['p', 'h1', 'h2', 'h3', 'li']))
        
        # Clean up whitespace
        text = ' '.join(text.split())
        
        return text[:15000] # Return first 15k chars to avoid massive context
        
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None


