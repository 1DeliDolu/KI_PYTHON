"""
Wikipedia Query Module
Handles Wikipedia searches and content retrieval
"""

import wikipedia
import requests
from typing import List, Dict, Optional
import logging
import sys
import os

# Add parent directory to path for importing config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

class WikipediaQuery:
    def __init__(self):
        self.config = Config()
        wikipedia.set_lang(self.config.WIKIPEDIA_LANGUAGE)
        self.logger = logging.getLogger(__name__)
    
    def search(self, query: str, max_results: Optional[int] = None) -> Dict:
        """
        Search Wikipedia for the given query
        
        Args:
            query (str): Search query
            max_results (int): Maximum number of results to return
            
        Returns:
            Dict: Search results with titles, summaries, and URLs
        """
        try:
            if max_results is None:
                max_results = self.config.WIKIPEDIA_MAX_RESULTS
            
            # Search for pages
            search_results = wikipedia.search(query, results=max_results)
            
            if not search_results:
                return {
                    "success": False,
                    "message": f"No results found for '{query}'",
                    "results": []
                }
            
            results = []
            for title in search_results:
                try:
                    page_info = self.get_page_info(title)
                    if page_info:
                        results.append(page_info)
                except wikipedia.exceptions.DisambiguationError as e:
                    # Handle disambiguation pages
                    self.logger.warning(f"Disambiguation error for '{title}': {e}")
                    if e.options:
                        # Try the first option
                        try:
                            page_info = self.get_page_info(e.options[0])
                            if page_info:
                                results.append(page_info)
                        except Exception:
                            continue
                except Exception as e:
                    self.logger.error(f"Error processing page '{title}': {e}")
                    continue
            
            return {
                "success": True,
                "query": query,
                "total_results": len(results),
                "results": results
            }
            
        except Exception as e:
            self.logger.error(f"Error searching Wikipedia: {e}")
            return {
                "success": False,
                "message": f"Error searching Wikipedia: {str(e)}",
                "results": []
            }
    
    def get_page_info(self, title: str) -> Optional[Dict]:
        """
        Get detailed information about a Wikipedia page
        
        Args:
            title (str): Page title
            
        Returns:
            Dict: Page information including summary, URL, etc.
        """
        try:
            page = wikipedia.page(title, auto_suggest=self.config.WIKIPEDIA_AUTO_SUGGEST)
            
            return {
                "title": page.title,
                "summary": wikipedia.summary(title, sentences=3),
                "url": page.url,
                "categories": page.categories[:5] if page.categories else [],
                "images": page.images[:3] if page.images else [],
                "references": page.references[:5] if page.references else []
            }
            
        except wikipedia.exceptions.PageError:
            self.logger.warning(f"Page not found: {title}")
            return None
        except wikipedia.exceptions.DisambiguationError as e:
            self.logger.warning(f"Disambiguation error for '{title}': {e}")
            raise e
        except Exception as e:
            self.logger.error(f"Error getting page info for '{title}': {e}")
            return None
    
    def get_full_content(self, title: str) -> Optional[str]:
        """
        Get full content of a Wikipedia page
        
        Args:
            title (str): Page title
            
        Returns:
            str: Full page content
        """
        try:
            page = wikipedia.page(title, auto_suggest=self.config.WIKIPEDIA_AUTO_SUGGEST)
            return page.content
        except Exception as e:
            self.logger.error(f"Error getting full content for '{title}': {e}")
            return None
    
    def search_with_suggestions(self, query: str) -> Dict:
        """
        Search with automatic suggestions for misspelled queries
        
        Args:
            query (str): Search query
            
        Returns:
            Dict: Search results with suggestions
        """
        try:
            # Try to get suggestions first
            suggestions = wikipedia.suggest(query)
            
            if suggestions and suggestions != query:
                return {
                    "original_query": query,
                    "suggested_query": suggestions,
                    "results": self.search(suggestions)
                }
            else:
                return self.search(query)
                
        except Exception as e:
            self.logger.error(f"Error in search with suggestions: {e}")
            return self.search(query)
    
    def get_random_page(self) -> Dict:
        """
        Get a random Wikipedia page
        
        Returns:
            Dict: Random page information
        """
        try:
            random_title = wikipedia.random()
            page_info = self.get_page_info(random_title)
            
            if page_info:
                return {
                    "success": True,
                    "type": "random_page",
                    "result": page_info
                }
            else:
                return {
                    "success": False,
                    "message": "Could not retrieve random page"
                }
                
        except Exception as e:
            self.logger.error(f"Error getting random page: {e}")
            return {
                "success": False,
                "message": f"Error getting random page: {str(e)}"
            }
    
    def set_language(self, language: str) -> bool:
        """
        Set Wikipedia language
        
        Args:
            language (str): Language code (e.g., 'en', 'tr', 'de')
            
        Returns:
            bool: Success status
        """
        try:
            wikipedia.set_lang(language)
            self.config.WIKIPEDIA_LANGUAGE = language
            return True
        except Exception as e:
            self.logger.error(f"Error setting language to '{language}': {e}")
            return False