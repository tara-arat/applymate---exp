"""Setup script to initialize ApplyMate."""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from loguru import logger
from config import settings
from database import init_db


async def setup():
    """Initialize the application."""
    
    print("🎯 ApplyMate Setup")
    print("=" * 50)
    
    # Step 1: Create directories
    print("\n📁 Creating directories...")
    try:
        settings.ensure_directories()
        print("   ✅ Directories created")
    except Exception as e:
        print(f"   ❌ Error creating directories: {e}")
        return False
    
    # Step 2: Initialize database
    print("\n💾 Initializing database...")
    try:
        await init_db()
        print("   ✅ Database initialized")
    except Exception as e:
        print(f"   ❌ Error initializing database: {e}")
        return False
    
    # Step 3: Create .env file if not exists
    print("\n⚙️  Setting up configuration...")
    env_file = project_root / ".env"
    env_example = project_root / ".env.example"
    
    if not env_file.exists() and env_example.exists():
        import shutil
        shutil.copy(env_example, env_file)
        print("   ✅ Created .env file from .env.example")
    else:
        print("   ℹ️  .env file already exists")
    
    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("\n📚 Next Steps:")
    print("   1. Review and edit .env file if needed")
    print("   2. Install spaCy model: python -m spacy download en_core_web_sm")
    print("   3. Install Playwright browsers: playwright install chromium")
    print("   4. Run the app: streamlit run ui/app.py")
    print("\n🎯 Happy job hunting with ApplyMate!")
    
    return True


if __name__ == "__main__":
    success = asyncio.run(setup())
    sys.exit(0 if success else 1)
