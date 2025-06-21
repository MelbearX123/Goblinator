import praw
import json
import time
import re
import dotenv
import os
from datetime import datetime
from typing import List, Dict

class BrainrotScraper:
    def __init__(self, client_id: str, client_secret: str, user_agent: str):
        """Initialize Reddit API connection"""
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        
        # Define brainrot terms to search for
        self.brainrot_terms = [
            "skibidi", "sigma", "rizz", "gyatt", "ohio", "fanum tax", 
            "bussin", "cap", "sus", "no cap", "bet", "fr fr", "periodt",
            "slay", "based", "cringe", "mid", "W", "L", "ratio"
        ]
        
        # Target subreddits
        self.target_subreddits = [
            "GenZ", "teenagers", "memes", "TikTokCringe", 
            "gaming", "Minecraft", "dankmemes", "shitposting"
        ]
        
        self.collected_data = []
    
    def contains_brainrot_terms(self, text: str) -> List[str]:
        """Check if text contains any brainrot terms and return matched terms"""
        if not text:
            return []
        
        text_lower = text.lower()
        found_terms = []
        
        for term in self.brainrot_terms:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(term.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found_terms.append(term)
        
        return found_terms
    
    def scrape_submissions(self, subreddit_name: str, limit: int = 50):
        """Scrape submissions from a specific subreddit"""
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            
            # Get hot posts
            for submission in subreddit.hot(limit=limit):
                # Check title
                title_terms = self.contains_brainrot_terms(submission.title)
                if title_terms:
                    self.add_data_entry(
                        content=submission.title,
                        source="title",
                        subreddit=subreddit_name,
                        terms_found=title_terms,
                        post_id=submission.id
                    )
                
                # Check selftext (for text posts)
                if submission.selftext:
                    selftext_terms = self.contains_brainrot_terms(submission.selftext)
                    if selftext_terms:
                        self.add_data_entry(
                            content=submission.selftext,
                            source="selftext",
                            subreddit=subreddit_name,
                            terms_found=selftext_terms,
                            post_id=submission.id
                        )
                
                # Scrape comments
                self.scrape_comments(submission, subreddit_name)
                
                # Rate limiting
                time.sleep(1)
                
        except Exception as e:
            print(f"Error scraping subreddit {subreddit_name}: {e}")
    
    def scrape_comments(self, submission, subreddit_name: str, max_comments: int = 20):
        """Scrape comments from a submission"""
        try:
            submission.comments.replace_more(limit=0)
            comments = submission.comments.list()[:max_comments]
            
            for comment in comments:
                if hasattr(comment, 'body') and comment.body:
                    comment_terms = self.contains_brainrot_terms(comment.body)
                    if comment_terms:
                        self.add_data_entry(
                            content=comment.body,
                            source="comment",
                            subreddit=subreddit_name,
                            terms_found=comment_terms,
                            post_id=submission.id,
                            comment_id=comment.id
                        )
        except Exception as e:
            print(f"Error scraping comments: {e}")
    
    def add_data_entry(self, content: str, source: str, subreddit: str, 
                      terms_found: List[str], post_id: str, comment_id: str = None):
        """Add a data entry to the collection"""
        entry = {
            "brainrot": content.strip(),
            "English": "",  # Intentionally left blank as requested
            "metadata": {
                "source": source,
                "subreddit": subreddit,
                "terms_found": terms_found,
                "post_id": post_id,
                "comment_id": comment_id,
                "timestamp": datetime.now().isoformat()
            }
        }
        self.collected_data.append(entry)
    
    def search_by_terms(self, limit_per_term: int = 20):
        """Search Reddit globally for specific brainrot terms"""
        for term in self.brainrot_terms:
            try:
                print(f"Searching for term: {term}")
                
                # Search across all of Reddit
                for submission in self.reddit.subreddit("all").search(term, limit=limit_per_term):
                    # Check title
                    if self.contains_brainrot_terms(submission.title):
                        self.add_data_entry(
                            content=submission.title,
                            source="search_title",
                            subreddit=submission.subreddit.display_name,
                            terms_found=[term],
                            post_id=submission.id
                        )
                    
                    # Check comments (limited)
                    try:
                        submission.comments.replace_more(limit=0)
                        for comment in submission.comments.list()[:5]:
                            if hasattr(comment, 'body') and self.contains_brainrot_terms(comment.body):
                                self.add_data_entry(
                                    content=comment.body,
                                    source="search_comment",
                                    subreddit=submission.subreddit.display_name,
                                    terms_found=[term],
                                    post_id=submission.id,
                                    comment_id=comment.id
                                )
                    except:
                        pass
                
                # Rate limiting
                time.sleep(2)
                
            except Exception as e:
                print(f"Error searching for term {term}: {e}")
    
    def save_to_json(self, filename: str = "brainrot_data.json"):
        """Save collected data to JSON file in the specified format"""
        # Create the final format - array of objects with brainrot and English fields
        output_data = []
        
        for entry in self.collected_data:
            formatted_entry = {
                "brainrot": entry["brainrot"],
                "English": entry["English"]
            }
            output_data.append(formatted_entry)
        
        # Save with metadata file as well
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        # Save full data with metadata to separate file
        metadata_filename = filename.replace('.json', '_with_metadata.json')
        with open(metadata_filename, 'w', encoding='utf-8') as f:
            json.dump(self.collected_data, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(output_data)} entries to {filename}")
        print(f"Saved full data with metadata to {metadata_filename}")
    
    def run_scraper(self, posts_per_subreddit: int = 30, search_limit: int = 15):
        """Main scraping function"""
        print("Starting Reddit brainrot scraper...")
        
        # Scrape target subreddits
        for subreddit in self.target_subreddits:
            print(f"Scraping r/{subreddit}...")
            self.scrape_submissions(subreddit, posts_per_subreddit)
            time.sleep(2)  # Be nice to Reddit's servers
        
        # Search by specific terms
        print("Searching by brainrot terms...")
        self.search_by_terms(search_limit)
        
        # Remove duplicates based on content
        self.remove_duplicates()
        
        # Save results
        self.save_to_json()
        
        print(f"Scraping complete! Collected {len(self.collected_data)} unique entries.")
    
    def remove_duplicates(self):
        """Remove duplicate entries based on content"""
        seen_content = set()
        unique_data = []
        
        for entry in self.collected_data:
            content_hash = entry["brainrot"].lower().strip()
            if content_hash not in seen_content and len(content_hash) > 10:  # Filter out very short entries
                seen_content.add(content_hash)
                unique_data.append(entry)
        
        self.collected_data = unique_data
        print(f"Removed duplicates, {len(self.collected_data)} unique entries remaining")

if __name__ == "__main__":
    # Load environment variables from .env file
    dotenv.load_dotenv()

    CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
    CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
    if not CLIENT_ID or not CLIENT_SECRET:
        raise ValueError("Please set the REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET environment variables.")
    USER_AGENT = "Goblinator"
    
    # Initialize and run scraper
    scraper = BrainrotScraper(CLIENT_ID, CLIENT_SECRET, USER_AGENT)
    scraper.run_scraper(posts_per_subreddit=25, search_limit=10)