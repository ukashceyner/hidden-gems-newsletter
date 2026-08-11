#!/usr/bin/env python3
"""
Hidden Gems CLI - Search and analyze the newsletter archive
"""

import json
import glob
import os
from pathlib import Path
from collections import Counter

DATA_DIR = Path(__file__).parent

# Override to point to the actual repo location
REPO_DIR = Path("/tmp/hidden-gems-newsletter")

def load_all_repos():
    """Load all repos from JSON files"""
    repos = []
    # Check local first, then repo location
    search_dir = DATA_DIR if list(DATA_DIR.glob("*.json")) else REPO_DIR
    
    for filepath in glob.glob(str(search_dir / "*.json")):
        if filepath.endswith("README.md"):
            continue
        with open(filepath, 'r') as f:
            repos.extend(json.load(f))
    return repos

def search(query, lang=None, min_stars=0):
    """Search repos by keyword and optional filters"""
    repos = load_all_repos()
    results = []
    
    query_lower = query.lower()
    
    for repo in repos:
        # Filter by stars
        if repo.get('stars', 0) < min_stars:
            continue
        
        # Filter by language
        if lang and lang.lower() != repo.get('lang', '').lower():
            continue
        
        # Search in name and description
        if query_lower in repo.get('name', '').lower() or query_lower in repo.get('desc', '').lower():
            results.append(repo)
    
    # Sort by stars
    results.sort(key=lambda x: x.get('stars', 0), reverse=True)
    return results

def stats():
    """Show archive statistics"""
    repos = load_all_repos()
    
    # Top languages
    languages = [r.get('lang', 'Unknown') for r in repos if r.get('lang')]
    lang_counts = Counter(languages).most_common(10)
    
    # Total stars
    total_stars = sum(r.get('stars', 0) for r in repos)
    
    # Date range
    dates = [r.get('createdAt', '')[:10] for r in repos if r.get('createdAt')]
    
    print(f"📊 Hidden Gems Archive Stats")
    print(f"=" * 40)
    print(f"Total repos: {len(repos)}")
    print(f"Total stars: {total_stars:,}")
    print(f"\n🗣️ Top Languages:")
    for lang, count in lang_counts:
        print(f"  {lang}: {count}")
    
    if dates:
        print(f"\n📅 Date range: {min(dates)} to {max(dates)}")

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  hidden-gems.py search <query> [--lang Python] [--min-stars 100]")
        print("  hidden-gems.py stats")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "stats":
        stats()
    
    elif command == "search":
        query = sys.argv[2] if len(sys.argv) > 2 else ""
        
        # Parse flags
        lang = None
        min_stars = 0
        for arg in sys.argv[3:]:
            if arg.startswith("--lang="):
                lang = arg.split("=")[1]
            elif arg.startswith("--min-stars="):
                min_stars = int(arg.split("=")[1])
        
        results = search(query, lang=lang, min_stars=min_stars)
        
        print(f"🔍 Found {len(results)} results for '{query}'")
        if lang:
            print(f"   (filtered by language: {lang})")
        print("-" * 60)
        
        for repo in results[:20]:
            print(f"⭐ {repo.get('stars', 0):,} | {repo.get('lang', '-')}")
            print(f"   {repo.get('name')}")
            print(f"   {repo.get('desc', 'no description')[:80]}")
            print()

if __name__ == "__main__":
    main()
