# 🚀 LinkedIn Post Generator

**Automated AI-powered LinkedIn content creation for tech professionals**

> Automatically surf the web for the latest AI, ML, Data Science, Cloud, and DevOps news, then generate engaging LinkedIn posts optimized for maximum engagement.

---

## 📖 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Documentation](#documentation)
- [Quick Start](#quick-start)
- [Project Status](#project-status)
- [Tech Stack](#tech-stack)
- [License](#license)

---

## 🎯 Overview

This tool helps you maintain an active, valuable LinkedIn presence by:

1. **Automatically collecting** tech news from multiple sources (ArXiv, Hacker News, Dev.to, Reddit)
2. **Intelligently filtering** content based on relevance and engagement
3. **Generating LinkedIn posts** using Google Gemini AI
4. **Optimizing for engagement** with proper formatting, hashtags, and CTAs
5. **Providing drafts** for manual review before posting

**No auto-posting** - You stay in control and maintain your authentic voice.

---

## ✨ Features

### Content Aggregation
- 📚 **ArXiv** - Latest AI/ML research papers
- 🔥 **Hacker News** - Top tech stories
- 💻 **Dev.to** - DevOps and Cloud articles
- 🗨️ **Reddit** - Posts from r/MachineLearning, r/devops

### AI-Powered Generation
- 🤖 Uses **Google Gemini API** (free tier)
- 🎨 **LinkedIn-optimized** formatting
- 📝 Multiple post templates (news, research, tips)
- ✍️ Professional yet engaging tone

### Smart Features
- 🔍 Intelligent content ranking
- 🚫 Duplicate detection
- 📊 Engagement tracking
- 💾 Post history management
- 📈 Performance statistics

### Content Mix
- **75%** News/Research-based posts
- **25%** Experience-based tips
- **2 posts/week** optimal frequency

---

## 📚 Documentation

This project includes comprehensive documentation:

| Document | Description |
|----------|-------------|
| [DESIGN_DOCUMENTATION.md](DESIGN_DOCUMENTATION.md) | Complete system architecture, components, database schema |
| [FLOWCHARTS_AND_DIAGRAMS.md](FLOWCHARTS_AND_DIAGRAMS.md) | Visual workflows, decision trees, and data flows |
| [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md) | Step-by-step implementation guide with code examples |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Git
- Google Gemini API key ([Get it free](https://makersuite.google.com/app/apikey))
- Reddit API credentials (optional, but recommended)

### Installation

```powershell
# Clone or navigate to project directory
cd "d:\Project\Linkedin Post maker"

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Copy .env.example to .env and add your API keys
Copy-Item .env.example .env
# Edit .env with your actual API keys
```

### Configuration

Edit `.env` file:

```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional (for Reddit scraping)
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=linkedin_post_generator/1.0
```

### Initialize Database

```powershell
python src/database/models.py
```

### First Run

```powershell
# Fetch latest content
python main.py fetch

# Generate your first post
python main.py generate --type news

# List all drafts
python main.py list-drafts

# Review a specific draft
python main.py review --id 1
```

---

## 📁 Project Structure

```
Linkedin Post maker/
│
├── README.md                          # This file
├── DESIGN_DOCUMENTATION.md            # System architecture
├── FLOWCHARTS_AND_DIAGRAMS.md        # Visual diagrams
├── IMPLEMENTATION_ROADMAP.md         # Step-by-step guide
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment variables template
├── .gitignore                        # Git ignore rules
│
├── config/                           # Configuration files
├── data/                             # Database & data storage
│   ├── linkedin_posts.db            # SQLite database
│   └── tips/                        # Curated tips library
│
├── drafts/                           # Generated post drafts
│
├── src/                              # Source code
│   ├── aggregator/                  # Content scrapers
│   ├── filter/                      # Content ranking
│   ├── generator/                   # AI post generation
│   ├── formatter/                   # Post formatting
│   ├── database/                    # Database management
│   ├── scheduler/                   # Task scheduling
│   ├── cli/                         # Command-line interface
│   └── utils/                       # Utility functions
│
├── tests/                            # Unit tests
└── main.py                           # Entry point
```

---

## 🏗️ Project Status

### Current Phase: Foundation Setup ✅

- [x] Project structure defined
- [x] Documentation completed
- [x] Implementation roadmap created
- [ ] Development environment setup
- [ ] Database implementation
- [ ] Content scrapers
- [ ] AI integration
- [ ] CLI interface
- [ ] Testing & optimization

### Roadmap

#### Phase 1: Foundation (Week 1)
- Project setup
- Database schema
- Basic scrapers (ArXiv, Hacker News)

#### Phase 2: Content Aggregation (Week 1-2)
- All scrapers implemented
- Content ranking algorithm
- Duplicate detection

#### Phase 3: AI Integration (Week 2)
- Gemini API integration
- Prompt engineering
- Post generation

#### Phase 4: CLI & Automation (Week 3)
- Command-line interface
- Draft management
- Scheduling

#### Phase 5: Polish (Week 3-4)
- Testing
- Documentation
- Optimization

#### Phase 6: Web Dashboard (Future)
- Optional web interface
- Visual post editor

---

## 🛠️ Tech Stack

### Core
- **Python 3.11+** - Main language
- **SQLite** - Database
- **Google Gemini API** - AI content generation

### APIs & Libraries
- `google-generativeai` - Gemini API client
- `requests` - HTTP requests
- `praw` - Reddit API
- `feedparser` - RSS parsing
- `click` - CLI framework
- `rich` - Terminal formatting
- `pandas` - Data manipulation

### Development
- `pytest` - Testing
- `black` - Code formatting
- `pylint` - Linting

---

## 🎨 Example Output

### Generated News Post
```
🚀 OpenAI just dropped GPT-5, and it's a game-changer!

The new model shows 40% improvement in reasoning and can now 
handle multi-step problem solving that previously required 
human intervention.

Here's why this matters:
• Real-time code debugging with context awareness
• Natural language to SQL queries with 95% accuracy
• Multi-lingual support for 100+ languages

This isn't just an incremental update—it's redefining what's 
possible with AI assistants.

What applications are you most excited to build with this?

#AI #GPT5 #MachineLearning #OpenAI #TechNews
```

### Generated Tip Post
```
💡 "Always write Dockerfiles" they said.
"It's best practice" they said.

Then I spent 3 hours debugging why my Python app worked 
locally but failed in production.

The culprit? Layer caching gone wrong.

Here's what I learned about Docker best practices:

1. Order matters - Put least-changing commands first
2. Use .dockerignore - Saved me 80% build time
3. Multi-stage builds - Reduced image from 1.2GB to 180MB
4. Never run as root - Security 101
5. Pin versions - "latest" is your enemy in production

Docker is powerful, but the devil is in the details.

What Docker gotcha caught you off guard?

#DevOps #Docker #Kubernetes #TechTips
```

---

## 📊 Content Strategy

### Weekly Schedule
- **2 posts per week** (optimal LinkedIn frequency)
- **Mondays/Tuesdays**: Primary post
- **Thursdays/Fridays**: Secondary post

### Content Mix (Monthly)
- **6 posts** (75%): News, research, breakthroughs
  - 3 AI/ML topics
  - 2 DevOps/Cloud topics
  - 1 Data Science topic
- **2 posts** (25%): Experience-based tips & advice

---

## 🔐 Privacy & Ethics

- ✅ Only public data sources
- ✅ Respects API rate limits
- ✅ No personal data collection
- ✅ Proper attribution to sources
- ✅ Manual review before posting

---

## 🤝 Contributing

This is a personal project, but suggestions are welcome!

### To suggest improvements:
1. Review the documentation
2. Open an issue with your idea
3. Be specific about the use case

---

## 📝 License

This project is for personal use. Feel free to adapt for your own needs.

---

## 🙏 Acknowledgments

### Data Sources
- [ArXiv](https://arxiv.org/) - Research papers
- [Hacker News](https://news.ycombinator.com/) - Tech news
- [Dev.to](https://dev.to/) - Developer articles
- [Reddit](https://reddit.com/) - Community discussions

### AI
- [Google Gemini](https://ai.google.dev/) - Content generation

---

## 📞 Questions?

Before starting implementation, please review:
1. [DESIGN_DOCUMENTATION.md](DESIGN_DOCUMENTATION.md) - System design
2. [FLOWCHARTS_AND_DIAGRAMS.md](FLOWCHARTS_AND_DIAGRAMS.md) - Visual guides
3. [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md) - Build guide

---

## 🎯 Next Steps

1. ✅ Review all documentation
2. [ ] Set up development environment
3. [ ] Get API keys (Gemini, Reddit)
4. [ ] Follow implementation roadmap
5. [ ] Test with sample data
6. [ ] Generate your first post!

---

**Ready to get started?** Head over to [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md) for detailed setup instructions!

---

*Built with ❤️ for maintaining an active, valuable LinkedIn presence without the daily grind.*
