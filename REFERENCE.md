# ApplyMate Quick Reference Card

## 🚀 Quick Start

```powershell
# Setup (first time only)
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m spacy download en_core_web_sm
playwright install chromium
python setup.py

# Run
streamlit run ui/app.py
```

## 📋 Common Commands

```powershell
# Start application
streamlit run ui/app.py

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Deactivate virtual environment
deactivate

# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Initialize database
python -m database.db_manager

# Run setup
python setup.py

# View logs (last 50 lines)
Get-Content data/logs/applymate.log -Tail 50

# View logs (live)
Get-Content data/logs/applymate.log -Wait
```

## 🗂️ File Locations

| Item | Location |
|------|----------|
| Database | `data/database/applymate.db` |
| Logs | `data/logs/applymate.log` |
| Resumes | `data/uploads/<user_id>/` |
| Config | `.env` |
| Main App | `ui/app.py` |

## 🔧 Configuration (.env)

```ini
# Show/hide browser
BROWSER_HEADLESS=False

# Browser timeout (ms)
BROWSER_TIMEOUT=30000

# Minimum match confidence (0.0-1.0)
MIN_FIELD_MATCH_SCORE=0.6

# Log level
LOG_LEVEL=INFO

# Debug mode
DEBUG=False
```

## 🎯 Keyboard Shortcuts (in browser)

| Key | Action |
|-----|--------|
| `Ctrl + C` | Stop Streamlit server |
| `R` | Refresh page (in Streamlit) |
| `Alt + F4` | Close window |

## 📊 Database Tables

```sql
-- Users
users(id, username, email, password_hash, is_active, created_at, updated_at)

-- Profiles
profiles(id, user_id, first_name, last_name, email, phone, ...)

-- Applications
applications(id, user_id, job_title, company_name, job_url, status, ...)

-- Field Mappings (learning)
field_mappings(id, field_label, profile_field, confidence_score, ...)
```

## 🔍 Troubleshooting

### Browser doesn't open
```powershell
playwright install chromium
```

### Database errors
```powershell
# Backup first!
Remove-Item data/database/applymate.db
python setup.py
```

### Import errors
```powershell
pip install -r requirements.txt --force-reinstall
```

### spaCy model not found
```powershell
python -m spacy download en_core_web_sm
```

### Port already in use
```powershell
# Kill process on port 8501
Get-Process | Where-Object {$_.ProcessName -like "*streamlit*"} | Stop-Process

# Or run on different port
streamlit run ui/app.py --server.port 8502
```

## 📱 UI Pages

| Page | Purpose |
|------|---------|
| 📊 Dashboard | View all applications |
| ➕ New Application | Start new application |
| 👤 Profile Manager | Edit profile |
| ℹ️ About | App information |

## 🔄 Application Workflow

```
1. Profile Manager
   └─> Fill out profile information

2. New Application
   ├─> Enter job URL
   ├─> Detect fields (automatic)
   ├─> Review matches
   └─> Open browser

3. Manual Submit
   └─> Fill & submit in browser

4. Update Status
   ├─> ✅ Mark as Submitted
   ├─> ⏭️ Skip
   └─> 💾 Save as Draft

5. Dashboard
   └─> View all applications
```

## 🎨 Application Status

| Status | Icon | Color | Meaning |
|--------|------|-------|---------|
| Draft | 📝 | Blue | In progress |
| Submitted | ✅ | Green | Completed |
| Skipped | ⏭️ | Gray | Not pursuing |

## 💡 Pro Tips

1. **Complete profile first** - Better auto-fill results
2. **Test with simple forms** - Get familiar with workflow
3. **Keep browser open** - Until you mark status
4. **Add notes** - Track important details
5. **Check logs** - If something goes wrong
6. **Backup database** - Copy `data/database/applymate.db`

## 🚨 Common Errors

### "Module not found"
```powershell
pip install <module-name>
# or
pip install -r requirements.txt
```

### "Database locked"
```powershell
# Close all connections and restart
Get-Process | Where-Object {$_.ProcessName -like "*streamlit*"} | Stop-Process
streamlit run ui/app.py
```

### "Permission denied"
```powershell
# Run as administrator or check folder permissions
```

### "spaCy model not found"
```powershell
python -m spacy download en_core_web_sm
```

## 📈 Performance Tips

- Close unused applications
- Clear browser cache periodically
- Restart app if slow
- Keep database small (delete old apps)
- Check internet connection

## 🔐 Security Checklist

- ✅ Keep `.env` private
- ✅ Don't share database file
- ✅ Use strong passwords (v0.2+)
- ✅ Backup data regularly
- ✅ Keep dependencies updated

## 📞 Getting Help

1. Check `QUICKSTART.md` for setup
2. Check `ARCHITECTURE.md` for technical details
3. Check logs: `data/logs/applymate.log`
4. Review error messages carefully
5. Check dependencies are installed

## 🎓 Learning Resources

- **README.md** - Overview
- **QUICKSTART.md** - Setup guide
- **ARCHITECTURE.md** - Technical details
- **ROADMAP.md** - Future plans
- **PROJECT_SUMMARY.md** - Full summary

## 🆘 Emergency Recovery

### Reset Everything
```powershell
# Backup important data first!
Remove-Item -Recurse data/
python setup.py
```

### Reinstall Dependencies
```powershell
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### Fresh Start
```powershell
deactivate
Remove-Item -Recurse venv/
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m spacy download en_core_web_sm
playwright install chromium
python setup.py
```

## 📝 Notes

- **Port**: Default is `8501`
- **Timeout**: Default is `30000ms` (30 seconds)
- **User ID**: Default is `1` (single-user mode)
- **Browser**: Chromium (headless available)
- **Database**: SQLite (local file)

---

**Version**: v0.1.0  
**Updated**: January 12, 2026  
**URL**: `http://localhost:8501`

---

**Quick Links**:
- 📖 [Full Documentation](README.md)
- 🏗️ [Architecture](ARCHITECTURE.md)
- 🚀 [Quick Start](QUICKSTART.md)
- 🗺️ [Roadmap](ROADMAP.md)

**Happy Job Hunting! 🎯**
