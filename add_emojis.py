import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Add emojis to the sidebar items
content = content.replace("Overview", "🏠 Overview")
content = content.replace("Make Deposit", "💸 Make Deposit")
content = content.replace("Withdraw Funds", "🏧 Withdraw Funds")
content = content.replace("Virtual Cards", "💳 Virtual Cards")
content = content.replace("Loans", "🏦 Loans")
content = content.replace("History", "📜 History")
content = content.replace("Settings / Update Profile", "⚙️ Update Profile")
content = content.replace("Edit Profile", "✏️ Edit Profile")
content = content.replace("Good day", "👋 Good day")
content = content.replace("Sign Out", "🚪 Sign Out")

# Add some emojis to the landing page
content = content.replace("Why Choose VaultX?", "✨ Why Choose VaultX? ✨")
content = content.replace("Comprehensive Banking Services", "💼 Comprehensive Banking Services")
content = content.replace("Trusted by Thousands", "❤️ Trusted by Thousands")
content = content.replace("Your Complete Console Banking Solution.", "Your Complete Console Banking Solution. 🚀✨")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
