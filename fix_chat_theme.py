import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Fix user bubble in Javascript
# Old (after general replace): bg-brass text-walnut text-cream p-3 rounded-2xl rounded-tr-sm shadow-sm max-w-[85%] leading-relaxed
user_bubble = r'class="bg-[^"]* rounded-2xl rounded-tr-sm[^"]*"'
content = re.sub(user_bubble, 'class="bg-navy text-cream p-3 rounded-2xl rounded-tr-sm shadow-sm max-w-[85%] leading-relaxed font-sans"', content)

# Fix bot bubble in Javascript
# Old (after general replace): bg-cream border border-ledgerline text-navy p-3 rounded-2xl rounded-tl-sm shadow-sm max-w-[85%] leading-relaxed whitespace-pre-wrap
bot_bubble = r'class="bg-cream border border-ledgerline text-navy[^"]* rounded-2xl rounded-tl-sm[^"]*"'
content = re.sub(bot_bubble, 'class="bg-cream border border-ledgerline text-sage p-3 rounded-2xl rounded-tl-sm shadow-sm max-w-[85%] leading-relaxed whitespace-pre-wrap font-handwriting text-2xl font-bold"', content)

# Fix loading bubble
load_bubble = r'class="bg-cream border border-ledgerline text-navy/70 p-3 rounded-2xl rounded-tl-sm shadow-sm flex items-center gap-2"'
content = content.replace(load_bubble, 'class="bg-cream border border-ledgerline text-sage p-3 rounded-2xl rounded-tl-sm shadow-sm flex items-center gap-2 font-handwriting text-xl"')

# The chat window initial bot message
initial_bot = r'<div class="bg-cream border border-ledgerline text-navy p-3 rounded-2xl rounded-tl-sm shadow-sm max-w-\[85%\] leading-relaxed">'
content = content.replace(initial_bot, '<div class="bg-cream border border-ledgerline text-sage p-3 rounded-2xl rounded-tl-sm shadow-sm max-w-[85%] leading-relaxed font-handwriting text-2xl font-bold">')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
