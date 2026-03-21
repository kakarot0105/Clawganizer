# Clawganizer Reddit API Setup Guide

## Automated Reddit Posting with PRAW

Auto-post to Reddit subreddits using the Reddit API.

---

## Step 1: Create Reddit App

1. **Go to:** https://www.reddit.com/prefs/apps
2. **Scroll to bottom** → "Create another app..."
3. **Fill out form:**
   - **Name:** Clawganizer-Poster
   - **App type:** Script
   - **Description:** Automated poster for Clawganizer
   - **Redirect URI:** http://localhost:8080 (or any localhost URL)
4. **Click "Create app"**
5. **Save these credentials:**
   - `Client ID` (below app name)
   - `Client Secret` (click "show")

---

## Step 2: Install Python Library

```bash
pip install praw
```

Requires Python 3.6+

---

## Step 3: Set Up Environment Variables

### Option A: Export in Terminal (One-time)
```bash
export REDDIT_CLIENT_ID="your_client_id_here"
export REDDIT_CLIENT_SECRET="your_client_secret_here"
export REDDIT_USERNAME="your_reddit_username"
export REDDIT_PASSWORD="your_reddit_password"
export REDDIT_USER_AGENT="Clawganizer-Poster/1.0"
```

### Option B: Create `.env` File (Permanent)
Create `~/.reddit_env`:
```bash
export REDDIT_CLIENT_ID="your_client_id"
export REDDIT_CLIENT_SECRET="your_client_secret"
export REDDIT_USERNAME="your_username"
export REDDIT_PASSWORD="your_password"
export REDDIT_USER_AGENT="Clawganizer-Poster/1.0"
```

Then load it:
```bash
source ~/.reddit_env
```

---

## Step 4: Run the Poster

```bash
python3 reddit_poster.py
```

**What it does:**
- Posts to r/opensource immediately
- Waits 6 hours
- Posts to r/devtools
- Waits 12 hours
- Posts to r/programming

---

## Step 5: Monitor Posts

The script will output:
```
✅ Posted to r/opensource
   URL: https://reddit.com/r/opensource/comments/...

✅ Posted to r/devtools
   URL: https://reddit.com/r/devtools/comments/...

✅ Posted to r/programming
   URL: https://reddit.com/r/programming/comments/...
```

---

## Customizing Posts

Edit `reddit_poster.py` and modify the `posts` list:

```python
posts = [
    {
        "subreddit": "opensource",  # Which subreddit
        "title": "Your post title",
        "body": "Your post body",
        "delay_minutes": 0  # Wait this long before posting
    }
]
```

---

## Adding More Subreddits

Add more posts to the list:

```python
posts = [
    # ... existing posts ...
    {
        "subreddit": "webdev",
        "title": "Built a Project Organizer Tool",
        "body": "Your post content here...",
        "delay_minutes": 1440  # 24 hours later
    }
]
```

---

## Reddit API Best Practices

### ✅ DO
- **Space out posts** (6-24 hours between subreddits)
- **Vary your content** slightly for each community
- **Respond to comments** manually (show you care)
- **Read rules** of each subreddit before posting
- **Be authentic** (not spammy)

### ❌ DON'T
- Post same content to multiple subreddits at once
- Spam the same message repeatedly
- Ignore community rules/guidelines
- Use multiple accounts to upvote your post
- Post more than once per subreddit
- Auto-respond to comments (Reddit doesn't like that)

---

## Troubleshooting

### "Authentication failed"
- Check credentials are correct
- Make sure password is correct (not email)
- Verify Reddit account has 2FA disabled for API access

### "Subreddit not found"
- Subreddit name is case-sensitive
- Use name without "r/" prefix
- Check subreddit exists

### "You are doing that too much"
- Reddit rate limits posts
- Space them out (6+ hours between posts)
- Use the delay_minutes parameter

### "Access denied"
- Check Reddit app credentials
- Verify Client ID and Secret are correct
- Re-create the Reddit app if needed

---

## Monitor Engagement

After posting, check:
1. **Upvotes** - How many people liked it
2. **Comments** - Questions/feedback
3. **Shares** - How many people shared it
4. **Awards** - If Reddit gold was given

**Always respond to comments manually!**

Reddit values authentic engagement. Don't use automated responses.

---

## Success Metrics

**Good engagement:**
- 100+ upvotes = Good post
- 500+ upvotes = Great post
- 1000+ upvotes = Viral

**Post making top of subreddit = 5-15K traffic**

---

## Safety Notes

⚠️ **Important:**
- Never share `Client Secret` publicly
- Never commit `.env` file to GitHub
- Use environment variables for credentials
- Don't post frequently to same subreddit (violates rules)
- Read each subreddit's posting rules

---

## Example Run

```bash
$ source ~/.reddit_env
$ python3 reddit_poster.py

================================================================================
CLAWGANIZER REDDIT AUTO-POSTER
================================================================================
Posts to schedule: 3
Starting in 5 seconds... (Ctrl+C to cancel)

📤 Posting 1/3...
✅ Posted to r/opensource
   URL: https://reddit.com/r/opensource/comments/abc123...

⏳ Waiting 360 minutes before next post...

📤 Posting 2/3...
✅ Posted to r/devtools
   URL: https://reddit.com/r/devtools/comments/def456...

⏳ Waiting 720 minutes before next post...

📤 Posting 3/3...
✅ Posted to r/programming
   URL: https://reddit.com/r/programming/comments/ghi789...

================================================================================
✅ All posts completed!
================================================================================
```

---

## Pro Tips

1. **Run in background:**
   ```bash
   nohup python3 reddit_poster.py > reddit_posts.log &
   ```

2. **Schedule with cron:**
   ```bash
   0 9 * * 1 cd /path/to/clawganizer && python3 reddit_poster.py
   ```
   (Runs every Monday at 9 AM)

3. **Monitor logs:**
   ```bash
   tail -f reddit_posts.log
   ```

4. **Dry run first:**
   - Edit one post temporarily
   - Run script with just one subreddit
   - Make sure it works
   - Then run full batch

---

## Support

If you hit errors:
1. Check credentials
2. Verify Reddit app exists
3. Check subreddit names
4. Review Reddit API documentation: https://praw.readthedocs.io

---

**Ready to auto-post?** 🚀

1. Get Reddit credentials
2. Set environment variables
3. Run `python3 reddit_poster.py`
4. Monitor posts
5. Respond to comments manually

That's it!
