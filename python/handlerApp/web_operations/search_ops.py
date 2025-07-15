import requests
from bs4 import BeautifulSoup
from typing import Dict, Any
from urllib.parse import quote_plus, urljoin

def clean_url(url: str) -> str:
    """Clean and normalize URL"""
    # Remove whitespace and newlines
    url = url.strip()
    # Remove any spaces or newlines within the URL
    url = ''.join(url.split())
    # Ensure proper protocol
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url

def fetch_and_parse_content(url: str) -> str:
    """Fetch and extract text content from a webpage"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        clean_target_url = clean_url(url)
        response = requests.get(clean_target_url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'footer', 'header']):
                element.decompose()
            
            # Get text content
            text = soup.get_text(separator=' ', strip=True)
            
            # Clean up the text
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            text = ' '.join(lines)
            
            return text[:2000]  # Limit content length
        return ""
    except Exception as e:
        print(f"Error fetching {clean_target_url}: {str(e)}")
        return ""

def get_duckduckgo_results(query: str, num_results: int = 3) -> list:
    """Get search results from DuckDuckGo"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    encoded_query = quote_plus(query)
    url = f'https://html.duckduckgo.com/html/?q={encoded_query}'
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            results = []
            for result in soup.select('.result__url'):
                if len(results) >= num_results:
                    break
                
                url = result.get_text()
                url = clean_url(url)
                results.append(url)
            
            return results
        return []
    except Exception as e:
        print(f"Error in DuckDuckGo search: {str(e)}")
        return []

def web_search(query: str, num_results: int = 10) -> Dict[str, Any]:
    """
    Search the web using DuckDuckGo and return text content for analysis
    """
    try:
        # Get search results from DuckDuckGo
        urls = get_duckduckgo_results(query, num_results)
        
        if not urls:
            return {
                "status": "error",
                "message": "No search results found",
                "query": query,
                "content": ""
            }
        
        # Fetch content from all URLs
        contents = []
        for url in urls:
            content = fetch_and_parse_content(url)
            if content.strip():
                contents.append(content)
        
        # Combine results
        combined_text = "\n\n".join([
            f"Source {i+1} content:\n{content}" 
            for i, content in enumerate(contents)
        ])
        
        if not combined_text.strip():
            return {
                "status": "error",
                "message": "No useful content found",
                "query": query,
                "content": ""
            }
        
        return {
            "status": "success",
            "message": f"Found content from {len(contents)} sources",
            "query": query,
            "content": combined_text
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Search failed: {str(e)}",
            "query": query,
            "content": ""
        }