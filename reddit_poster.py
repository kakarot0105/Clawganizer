#!/usr/bin/env python3
"""
Clawganizer Reddit Auto-Poster
Post to Reddit subreddits automatically using PRAW (Python Reddit API Wrapper)
"""

import praw
import json
import time
from datetime import datetime
import os

class RedditPoster:
    def __init__(self, client_id, client_secret, user_agent, username, password):
        """Initialize Reddit API connection"""
        try:
            self.reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent,
                username=username,
                password=password
            )
            print("✅ Connected to Reddit API")
        except Exception as e:
            print(f"❌ Failed to connect: {e}")
            exit(1)

    def post_to_subreddit(self, subreddit_name, title, body):
        """Post to a specific subreddit"""
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            submission = subreddit.submit(title=title, selftext=body)
            print(f"✅ Posted to r/{subreddit_name}")
            print(f"   URL: https://reddit.com{submission.permalink}")
            return submission
        except Exception as e:
            print(f"❌ Failed to post to r/{subreddit_name}: {e}")
            return None

    def schedule_posts(self, posts_config):
        """
        Schedule multiple posts
        posts_config = [
            {
                "subreddit": "opensource",
                "title": "Post title",
                "body": "Post body",
                "delay_minutes": 0
            }
        ]
        """
        for i, post in enumerate(posts_config):
            if i > 0:
                delay = post.get("delay_minutes", 0)
                print(f"\n⏳ Waiting {delay} minutes before next post...")
                time.sleep(delay * 60)
            
            print(f"\n📤 Posting {i+1}/{len(posts_config)}...")
            self.post_to_subreddit(
                post["subreddit"],
                post["title"],
                post["body"]
            )

# Example usage
if __name__ == "__main__":
    # Get credentials from environment variables
    REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
    REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
    REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "Clawganizer-Poster/1.0")
    REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
    REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")

    if not all([REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USERNAME, REDDIT_PASSWORD]):
        print("❌ Missing Reddit API credentials")
        print("\nSet these environment variables:")
        print("  export REDDIT_CLIENT_ID=your_client_id")
        print("  export REDDIT_CLIENT_SECRET=your_client_secret")
        print("  export REDDIT_USERNAME=your_username")
        print("  export REDDIT_PASSWORD=your_password")
        print("  export REDDIT_USER_AGENT=optional_user_agent")
        exit(1)

    # Initialize poster
    poster = RedditPoster(
        REDDIT_CLIENT_ID,
        REDDIT_CLIENT_SECRET,
        REDDIT_USER_AGENT,
        REDDIT_USERNAME,
        REDDIT_PASSWORD
    )

    # Define posts
    posts = [
        {
            "subreddit": "opensource",
            "title": "Clawganizer: Free Open Source Project Organizer for Developers",
            "body": """Hey everyone! 👋

We just open-sourced Clawganizer - a free tool that organizes your development workspace automatically.

**The Problem:** Developers waste hours managing folder structures and project organization.

**The Solution:** One command to organize everything.

```
/clawganizer "create project MyApp"
```

That's it. Clean structure. Every time.

**Features:**
- Create projects with proper structure
- Auto-organize workspace
- Archive old projects
- List active/archived projects
- Track workspace status
- Generate documentation

**Why we built it:**
Managing 10+ projects was chaos. We automated it and thought others might find it useful too.

**Tech Stack:**
- OpenClaw skill
- Bash shell
- MIT licensed
- 100% free, forever

**Get started:**
```
git clone https://github.com/kakarot0105/Clawganizer.git ~/.openclaw/skills/clawganizer
/clawganizer "create project MyApp"
```

Full docs: https://github.com/kakarot0105/Clawganizer

We'd love feedback! Any questions, feature requests, or issues - drop them in the GitHub repo.""",
            "delay_minutes": 0
        },
        {
            "subreddit": "devtools",
            "title": "Show HN: Clawganizer - Organize Your Dev Projects in Seconds (Open Source)",
            "body": """Hi everyone!

Built Clawganizer because managing multiple development projects was a nightmare. Figured other developers might have the same problem.

It's a simple tool that:
- Creates project folders with proper structure instantly
- Organizes your entire workspace automatically
- Lets you archive old projects to stay clean
- Tracks everything with simple commands

Works with any development workflow.

**Live Example:**
```
/clawganizer "create project backend"
/clawganizer "create project frontend"
/clawganizer "list projects"
/clawganizer "archive old-project"
```

Built as an OpenClaw skill, so it integrates with your workflow.

GitHub: https://github.com/kakarot0105/Clawganizer

It's completely free and open source. Would love to hear what developers think!

Happy to answer questions about development, design, or how it works.""",
            "delay_minutes": 360  # 6 hours later
        },
        {
            "subreddit": "programming",
            "title": "Clawganizer: Open Source Project Organization Tool (Show HN)",
            "body": """Released Clawganizer today - an open-source tool for organizing development projects.

**Problem it solves:**
Developers spend way too much time on folder structure and workspace organization. Especially when managing multiple projects.

**How it works:**
Simple command interface:
- Create projects with one command
- Auto-organize workspace structure
- Archive old projects
- Track everything

**Example:**
```
/clawganizer "create project new-feature"
```

Creates:
```
~/.openclaw/projects/active/new-feature/
├── src/
├── tests/
├── docs/
└── .gitignore
```

**Why open source:**
Workspace organization shouldn't be a commercial tool. It should be free and community-driven.

**Built for:**
OpenClaw developers, but adaptable to any workflow.

**Stats:**
- 100% free
- MIT licensed
- ~500 lines of bash
- Zero dependencies
- Production ready

GitHub: https://github.com/kakarot0105/Clawganizer
Docs: Full documentation included

Happy to discuss project organization, OpenClaw integration, or anything else!""",
            "delay_minutes": 720  # 12 hours later
        }
    ]

    # Schedule posts
    print("=" * 80)
    print("CLAWGANIZER REDDIT AUTO-POSTER")
    print("=" * 80)
    print(f"Posts to schedule: {len(posts)}")
    print("Starting in 5 seconds... (Ctrl+C to cancel)\n")
    
    time.sleep(5)
    
    poster.schedule_posts(posts)
    
    print("\n" + "=" * 80)
    print("✅ All posts completed!")
    print("=" * 80)
