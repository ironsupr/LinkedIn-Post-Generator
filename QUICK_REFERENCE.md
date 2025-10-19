# 🎯 LinkedIn Post Generator - Quick Reference Card

**Print this and keep it handy!**

---

## 🚀 DAILY COMMANDS

```powershell
# Start your session
cd "D:\Project\.In Progress\Linkedin Post maker"
.\venv\Scripts\Activate.ps1
```

---

## 📅 WEEKLY ROUTINE

### Monday & Thursday (Post Days)

```powershell
# 1. Generate a post (2 min)
python main.py generate --type news

# 2. Review it (2 min)
python main.py review --id [ID]

# 3. Copy to LinkedIn & Post

# 4. Mark as posted (30 sec)
python main.py mark-posted --id [ID] --engagement [num]
```

### Any Day (Content Refresh)

```powershell
# Fetch new content (5 min)
python main.py fetch
```

---

## 🔍 COMMON COMMANDS

```powershell
# List all drafts
python main.py list-drafts

# Check stats
python main.py stats

# Preview content
python main.py preview-content --limit 5

# Get help
python main.py --help
```

---

## 🎨 GENERATE VARIATIONS

```powershell
# AI-focused post
python main.py generate --type news --category AI

# DevOps post
python main.py generate --type news --category DevOps

# Cloud post
python main.py generate --type news --category Cloud

# Tip post
python main.py generate --type tip

# Save to file
python main.py generate --type news --save-file
```

---

## 📊 TRACKING

```powershell
# Review specific post
python main.py review --id 1

# Mark as posted with engagement
python main.py mark-posted --id 1 --engagement 75

# View statistics
python main.py stats
```

---

## 🔧 TROUBLESHOOTING

```powershell
# If virtual env not active
.\venv\Scripts\Activate.ps1

# Check system status
python main.py stats

# Show workflow
python main.py workflow

# Get command help
python main.py [command] --help
```

---

## 📈 SUCCESS CHECKLIST

**Week 1:**
- [ ] Fetch content daily
- [ ] Generate 2 posts
- [ ] Post to LinkedIn
- [ ] Track engagement

**Month 1:**
- [ ] 8 posts published
- [ ] Consistent schedule
- [ ] Average 30+ likes/post
- [ ] Building momentum

**Month 3:**
- [ ] 24 posts published
- [ ] Growing engagement
- [ ] Established presence
- [ ] Thought leadership

---

## 💡 QUICK TIPS

1. **Post Timing:** Best times are:
   - Tuesday-Thursday
   - 8-10 AM or 12-2 PM
   - Avoid weekends

2. **Always Edit:** Review AI output before posting

3. **Be Consistent:** Stick to 2x/week schedule

4. **Track Metrics:** Use --engagement flag

5. **Vary Topics:** Alternate categories

---

## 🎯 GOALS

- **Minimum:** 2 posts/week
- **Target:** 8 posts/month
- **Engagement:** 30+ likes per post
- **Time Investment:** 30 min/week

---

## 📞 EMERGENCY COMMANDS

```powershell
# API key expired?
# Update in .env file, then test:
python -m src.generator.gemini_client

# Database issues?
python main.py stats

# Can't remember command?
python main.py workflow
```

---

## ✅ PRE-POST CHECKLIST

Before posting each draft:
- [ ] Read entire post
- [ ] Check hashtags (3-5)
- [ ] Verify emojis (2-3)
- [ ] Ensure CTA question
- [ ] Check formatting
- [ ] Edit if needed
- [ ] Copy & post
- [ ] Mark as posted

---

## 📚 DOCUMENTATION

- **CLI_GUIDE.md** - Complete command reference
- **PROJECT_COMPLETE.md** - Full project summary
- **TEST_RESULTS.md** - Examples & testing
- **DESIGN_DOCUMENTATION.md** - Architecture

---

## 🔗 USEFUL LINKS

- Gemini API: https://aistudio.google.com/apikey
- Reddit Apps: https://www.reddit.com/prefs/apps
- Project Folder: D:\Project\.In Progress\Linkedin Post maker

---

## 🎉 YOUR WORKFLOW IN 3 STEPS

```
1. GENERATE → python main.py generate --type news
                ↓
2. REVIEW   → python main.py review --id [ID]
                ↓
3. POST     → python main.py mark-posted --id [ID]
```

---

**Keep this handy for quick reference!** 📌

**Questions? Run:** `python main.py workflow`
