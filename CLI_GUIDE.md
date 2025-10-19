# 🚀 LinkedIn Post Generator - Quick Start Guide

**Version:** 1.0.0  
**Status:** ✅ Fully Operational

A powerful automated tool for generating professional LinkedIn posts from aggregated tech content using AI.

---

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [Commands](#commands)
- [Workflow](#workflow)
- [Examples](#examples)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

---

## ⚡ Quick Start

```powershell
# 1. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 2. Fetch fresh content
python main.py fetch

# 3. Generate a post
python main.py generate --type news

# 4. Review the draft
python main.py review --id 1

# 5. Post to LinkedIn (manually)

# 6. Mark as posted
python main.py mark-posted --id 1
```

---

## 📦 Installation

### Prerequisites
- Python 3.11+
- Virtual environment (included)
- API Keys (Gemini required, Reddit optional)

### Setup
```powershell
# Virtual environment is already created and configured
.\venv\Scripts\Activate.ps1

# All dependencies are installed
# Ready to use!
```

### API Keys Required

**Gemini API (Required):**
- Get key: https://aistudio.google.com/apikey
- Add to `.env`: `GEMINI_API_KEY=your_key_here`

**Reddit API (Optional but Recommended):**
- Create app: https://www.reddit.com/prefs/apps
- Add to `.env`:
  ```
  REDDIT_CLIENT_ID=your_client_id
  REDDIT_CLIENT_SECRET=your_secret
  REDDIT_USER_AGENT=linkedin_post_generator/1.0 by /u/username
  ```

---

## 🎯 Usage

### Basic Commands

```powershell
# Show all commands
python main.py --help

# Show workflow
python main.py workflow

# Show statistics
python main.py stats
```

---

## 📝 Commands

### `fetch` - Get New Content
Fetches content from ArXiv, Hacker News, Dev.to, and Reddit.

```powershell
python main.py fetch
python main.py fetch --days 7
```

**Options:**
- `--days` - Days to look back (default: 7)

---

### `generate` - Create LinkedIn Post
Generates a professional LinkedIn post using AI.

```powershell
# Generate news post
python main.py generate --type news

# Generate AI-focused post
python main.py generate --type news --category AI

# Generate tip post
python main.py generate --type tip

# Save to file
python main.py generate --type news --save-file
```

**Options:**
- `--type` - Post type: `news` or `tip` (default: news)
- `--category` - Content category: `AI`, `DevOps`, `Cloud`, `DataScience`
- `--days` - Days to look back (default: 7)
- `--save-file` - Save draft as markdown file

---

### `list-drafts` - View All Drafts
Lists all unpublished draft posts.

```powershell
python main.py list-drafts
python main.py list-drafts --limit 10
```

**Options:**
- `--limit` - Maximum drafts to show (default: 10)

---

### `review` - View Specific Draft
Reviews a specific draft post in detail.

```powershell
python main.py review --id 1
python main.py review --id 1 --save
```

**Options:**
- `--id` - Post ID (required)
- `--save` - Save to markdown file

---

### `mark-posted` - Track Published Posts
Marks a draft as posted to LinkedIn.

```powershell
python main.py mark-posted --id 1
python main.py mark-posted --id 1 --engagement 50
```

**Options:**
- `--id` - Post ID (required)
- `--engagement` - Likes + comments count

---

### `preview-content` - Browse Available Content
Shows top-ranked content without generating a post.

```powershell
python main.py preview-content
python main.py preview-content --limit 10 --category AI
```

**Options:**
- `--days` - Days to look back (default: 7)
- `--limit` - Number of items (default: 10)
- `--category` - Filter by category

---

### `stats` - View Statistics
Displays system statistics.

```powershell
python main.py stats
```

Shows:
- Total content items
- Last fetch date
- Generated posts count
- Posted vs draft count

---

### `workflow` - Show Recommended Process
Displays the step-by-step posting workflow.

```powershell
python main.py workflow
```

---

## 🔄 Recommended Workflow

### Daily (5 minutes)
```powershell
python main.py fetch
```
Keeps your content database fresh.

### 2x Per Week (15 minutes each)
```powershell
# Monday morning
python main.py generate --type news
python main.py review --id [ID]
# Copy to LinkedIn and post
python main.py mark-posted --id [ID]

# Thursday evening
python main.py generate --type news
python main.py review --id [ID]
# Copy to LinkedIn and post
python main.py mark-posted --id [ID]
```

### Weekly (Optional)
```powershell
python main.py stats
```
Check your progress.

---

## 💡 Examples

### Example 1: Quick Daily Routine
```powershell
# Morning: Fetch content
python main.py fetch

# Check what's available
python main.py preview-content --limit 5

# Generate a post
python main.py generate --type news

# Review it
python main.py list-drafts
python main.py review --id 1
```

### Example 2: AI-Focused Post
```powershell
# Generate AI-specific post
python main.py generate --type news --category AI --save-file

# Review and save
python main.py review --id 2 --save

# After posting to LinkedIn
python main.py mark-posted --id 2 --engagement 75
```

### Example 3: Check Performance
```powershell
# View statistics
python main.py stats

# See all drafts
python main.py list-drafts

# Review specific posts
python main.py review --id 1
python main.py review --id 2
```

---

## ⚙️ Configuration

### Environment Variables (`.env`)

```env
# Required
GEMINI_API_KEY=your_gemini_api_key

# Optional (but recommended)
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_secret
REDDIT_USER_AGENT=linkedin_post_generator/1.0

# Settings
MAX_CONTENT_AGE_DAYS=7
POSTS_PER_WEEK=2
DEFAULT_POST_LENGTH=200
DATABASE_PATH=data/linkedin_posts.db
```

---

## 🎨 Post Quality

Generated posts include:
- ✅ Engaging hook (question or bold statement)
- ✅ Clear context and explanation
- ✅ Professional analysis
- ✅ Call-to-action question
- ✅ 3-5 relevant hashtags
- ✅ 2-3 strategic emojis
- ✅ Proper line breaks for readability
- ✅ 150-300 words

---

## 📊 Content Sources

The tool aggregates content from:

| Source | Content Type | Update Frequency |
|--------|--------------|------------------|
| **ArXiv** | AI/ML research papers | Daily |
| **Hacker News** | Top tech stories | Daily |
| **Dev.to** | DevOps & Cloud articles | Daily |
| **Reddit** | ML & DevOps discussions | Daily |

---

## 🔍 Content Ranking Algorithm

Posts are ranked using:
- **Recency (40%)** - How recent the content is
- **Engagement (30%)** - Social signals (upvotes, comments)
- **Relevance (30%)** - Topic match with your focus areas

---

## 🐛 Troubleshooting

### API Key Issues
```powershell
# Check if API key is valid
python -m src.generator.gemini_client
```

### Database Issues
```powershell
# Check database status
python main.py stats
```

### Content Not Fetching
```powershell
# Test individual scrapers
python -m src.aggregator.arxiv_scraper
python -m src.aggregator.hackernews_scraper
python -m src.aggregator.devto_scraper
python -m src.aggregator.reddit_scraper
```

### General Errors
```powershell
# Run with Python directly
python main.py [command] --help
```

---

## 📁 Project Structure

```
LinkedIn Post maker/
├── main.py                 # CLI entry point
├── .env                    # API keys and config
├── requirements.txt        # Dependencies
├── data/
│   ├── linkedin_posts.db  # SQLite database
│   └── tips/              # Personal tips library
├── drafts/                # Saved draft files
├── src/
│   ├── aggregator/        # Content scrapers
│   ├── generator/         # AI post generation
│   ├── filter/            # Content ranking
│   ├── formatter/         # Post formatting
│   ├── database/          # Database operations
│   └── cli/               # Command-line interface
└── venv/                  # Virtual environment
```

---

## 📈 Tips for Success

1. **Fetch Daily** - Keep content fresh
2. **Post Consistently** - 2x per week is ideal
3. **Review Before Posting** - Always check drafts
4. **Track Engagement** - Use `--engagement` flag
5. **Edit When Needed** - AI is a starting point
6. **Vary Categories** - Alternate between AI, DevOps, Cloud
7. **Add Personal Touch** - Edit to match your voice

---

## 🚀 Next Steps

1. **Start Posting** - Generate your first post today
2. **Build Routine** - Set calendar reminders
3. **Track Progress** - Use `stats` command weekly
4. **Optimize** - Refine based on engagement
5. **Scale Up** - Increase to 3x/week once comfortable

---

## 🎯 Success Metrics

### Week 1
- [ ] Generate 2 posts
- [ ] Post to LinkedIn
- [ ] Track engagement

### Month 1
- [ ] 8 posts published
- [ ] Average 30+ likes per post
- [ ] Building consistent presence

### Month 3
- [ ] 24 posts published
- [ ] Growing engagement
- [ ] Established thought leadership

---

## 💬 Support

For issues or questions:
1. Check this README
2. Run `python main.py workflow`
3. Review documentation files
4. Check TEST_RESULTS.md for examples

---

## ✅ Current Status

- **Content Database:** 102 items
- **Generated Posts:** 3 total (1 posted, 2 drafts)
- **Last Fetch:** 2025-10-19
- **System Status:** ✅ Fully Operational

---

**Happy Posting! 🎉**

Remember: Consistency is key. Set a schedule and stick to it!
