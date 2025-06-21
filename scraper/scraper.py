import praw
import json
import time
import re
import os
from dotenv import load_dotenv
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
            "GenZ", "teenagers  ", "memes", "TikTokCringe", 
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
            
            print(f"  Fetching {limit} posts from r/{subreddit_name}...")
            submissions = list(subreddit.hot(limit=limit))
            
            # Get hot posts
            for i, submission in enumerate(submissions, 1):
                print(f"  Processing post {i}/{len(submissions)} in r/{subreddit_name} (Found: {len(self.collected_data)} entries)", end='\r')
                
                # Check title
                title_terms = self.contains_brainrot_terms(submission.title)
                if title_terms:
                    self.add_data_entry(submission.title)
                
                # Check selftext (for text posts)
                if submission.selftext:
                    selftext_terms = self.contains_brainrot_terms(submission.selftext)
                    if selftext_terms:
                        self.add_data_entry(submission.selftext)
                
                # Scrape comments
                self.scrape_comments(submission, subreddit_name)
                
                # Rate limiting
                #time.sleep(1)
            
            print(f"\n  Completed r/{subreddit_name}: {len(self.collected_data)} total entries found")
                
        except Exception as e:
            print(f"\n  Error scraping subreddit {subreddit_name}: {e}")
    
    def scrape_comments(self, submission, subreddit_name: str, max_comments: int = 20):
        """Scrape comments from a submission"""
        try:
            submission.comments.replace_more(limit=0)
            comments = submission.comments.list()[:max_comments]
            
            for comment in comments:
                if hasattr(comment, 'body') and comment.body:
                    comment_terms = self.contains_brainrot_terms(comment.body)
                    if comment_terms:
                        self.add_data_entry(comment.body)
        except Exception as e:
            print(f"Error scraping comments: {e}")
    
    def add_data_entry(self, content: str):
        """Add a data entry to the collection"""
        entry = {
            "brainrot": content.strip(),
            "English": ""  # Intentionally left blank as requested
        }
        self.collected_data.append(entry)
    
    def search_by_terms(self, limit_per_term: int = 20):
        """Search Reddit globally for specific brainrot terms"""
        total_terms = len(self.brainrot_terms)
        
        for term_index, term in enumerate(self.brainrot_terms, 1):
            try:
                print(f"\nSearching for term: '{term}' ({term_index}/{total_terms})")
                initial_count = len(self.collected_data)
                
                # Search across all of Reddit
                submissions = list(self.reddit.subreddit("all").search(term, limit=limit_per_term))
                
                for i, submission in enumerate(submissions, 1):
                    print(f"  Processing search result {i}/{len(submissions)} for '{term}' (Found: {len(self.collected_data)} total)", end='\r')
                    
                    # Check title
                    if self.contains_brainrot_terms(submission.title):
                        self.add_data_entry(submission.title)
                    
                    # Check comments (limited)
                    try:
                        submission.comments.replace_more(limit=0)
                        for comment in submission.comments.list()[:5]:
                            if hasattr(comment, 'body') and self.contains_brainrot_terms(comment.body):
                                self.add_data_entry(comment.body)
                    except:
                        pass
                
                new_entries = len(self.collected_data) - initial_count
                print(f"\n  Completed '{term}': +{new_entries} new entries ({len(self.collected_data)} total)")
                
            except Exception as e:
                print(f"\n  Error searching for term {term}: {e}")
    
    def save_to_json(self, filename: str = "brainrot_data.json"):
        """Save collected data to JSON file in the specified format"""
        # Save the clean format directly since we already have the right structure
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.collected_data, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(self.collected_data)} entries to {filename}")
    
    def run_scraper(self, posts_per_subreddit: int = 30, search_limit: int = 15):
        """Main scraping function"""
        start_time = time.time()
        print("Starting Reddit brainrot scraper...")
        print(f"Target: {len(self.target_subreddits)} subreddits, {len(self.brainrot_terms)} search terms")
        print("=" * 60)
        
        # Scrape target subreddits
        print(f"\nPhase 1: Scraping {len(self.target_subreddits)} target subreddits")
        for i, subreddit in enumerate(self.target_subreddits, 1):
            print(f"\n[{i}/{len(self.target_subreddits)}] Scraping r/{subreddit}...")
            initial_count = len(self.collected_data)
            self.scrape_submissions(subreddit, posts_per_subreddit)
            new_entries = len(self.collected_data) - initial_count
            print(f"  Completed r/{subreddit}: +{new_entries} entries")
        
        print(f"\nPhase 1 complete: {len(self.collected_data)} entries from subreddits")
        
        # Search by specific terms
        print(f"\nPhase 2: Searching by brainrot terms")
        initial_search_count = len(self.collected_data)
        self.search_by_terms(search_limit)
        search_entries = len(self.collected_data) - initial_search_count
        print(f"\nPhase 2 complete: +{search_entries} entries from term searches")
        
        # Remove duplicates based on content
        print(f"\nPhase 3: Cleaning data...")
        before_dedup = len(self.collected_data)
        self.remove_duplicates()
        removed_dupes = before_dedup - len(self.collected_data)
        print(f"Removed {removed_dupes} duplicates")
        
        # Save results
        print(f"\nPhase 4: Saving results...")
        self.save_to_json()
        
        # Summary
        elapsed_time = time.time() - start_time
        print("\n" + "=" * 60)
        print(f"Scraping complete!")
        print(f"Final count: {len(self.collected_data)} unique brainrot entries")
        print(f"Total time: {elapsed_time:.1f} seconds")
        print(f"File saved: brainrot_data.json")
        print("=" * 60)
    
    def remove_duplicates(self):
        """Remove duplicate entries based on content"""
        seen_content = set()
        unique_data = []
        
        total_entries = len(self.collected_data)
        for i, entry in enumerate(self.collected_data, 1):
            print(f"  Checking for duplicates: {i}/{total_entries}", end='\r')
            
            content_hash = entry["brainrot"].lower().strip()
            if content_hash not in seen_content and len(content_hash) > 10:  # Filter out very short entries
                seen_content.add(content_hash)
                unique_data.append(entry)
        
        self.collected_data = unique_data
        print(f"  Deduplication complete: {len(self.collected_data)} unique entries remaining" + " " * 20)

# Usage example
if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()

    CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
    if not CLIENT_ID:
        raise ValueError("REDDIT_CLIENT_ID environment variable not set")
    CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
    if not CLIENT_SECRET:
        raise ValueError("REDDIT_CLIENT_SECRET environment variable not set")
    USER_AGENT = os.getenv("REDDIT_USER_AGENT")
    if not USER_AGENT:
        raise ValueError("REDDIT_USER_AGENT environment variable not set")
    
    # Initialize and run scraper
    scraper = BrainrotScraper(CLIENT_ID, CLIENT_SECRET, USER_AGENT)
    scraper.run_scraper(posts_per_subreddit=25, search_limit=10)