# Simple Git Setup for ApplyMate (Windows)

# Initialize git repository
git init

# Add all files
git add .

# Initial commit
git commit -m "Initial commit - ApplyMate v0.1"

Write-Host "Git repository initialized!"
Write-Host ""
Write-Host "To push to GitHub (optional):"
Write-Host "1. Create a private repo on GitHub"
Write-Host "2. Run: git remote add origin https://github.com/yourusername/applymate.git"
Write-Host "3. Run: git branch -M main"
Write-Host "4. Run: git push -u origin main"
