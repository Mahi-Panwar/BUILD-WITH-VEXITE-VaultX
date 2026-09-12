import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Fix Initial Bot Message
content = re.sub(
    r'<div class="bg-cream border border-white/10 text-slate-100 p-3 rounded-2xl rounded-tl-sm shadow-sm max-w-\[85%\] leading-relaxed">\s*Hello! I am your VaultX AI Assistant\. How can I help you today\?\s*</div>',
    '<div class="bg-cream border border-ledgerline text-sage font-handwriting text-2xl font-bold p-3 rounded-2xl rounded-tl-sm shadow-sm max-w-[85%] leading-relaxed">Hello! I am your VaultX AI Assistant. How can I help you today?</div>',
    content
)

# Fix injected JS Bot Message
content = re.sub(
    r'<div class="bg-cream border border-ledgerline text-navy p-3 rounded-2xl rounded-tl-sm shadow-sm max-w-\[85%\] leading-relaxed whitespace-pre-wrap">',
    '<div class="bg-cream border border-ledgerline text-sage font-handwriting text-2xl font-bold p-3 rounded-2xl rounded-tl-sm shadow-sm max-w-[85%] leading-relaxed whitespace-pre-wrap">',
    content
)
# Wait, let's just use string replace on the known JS string block inside index.html for chat bot
content = content.replace(
    'class="bg-cream border border-white/10 text-slate-100 p-3 rounded-2xl rounded-tl-sm shadow-sm max-w-[85%] leading-relaxed whitespace-pre-wrap"',
    'class="bg-cream border border-ledgerline text-sage font-handwriting text-2xl font-bold p-3 rounded-2xl rounded-tl-sm shadow-sm max-w-[85%] leading-relaxed whitespace-pre-wrap"'
)

# Fix loading indicator
content = content.replace(
    'class="bg-cream border border-white/10 text-slate-100 p-3 rounded-2xl rounded-tl-sm shadow-sm flex items-center gap-2"',
    'class="bg-cream border border-ledgerline text-sage font-handwriting text-xl font-bold p-3 rounded-2xl rounded-tl-sm shadow-sm flex items-center gap-2"'
)

# Fix user message in JS
content = content.replace(
    'class="bg-navy text-cream p-3 rounded-2xl rounded-tr-sm shadow-sm max-w-[85%] leading-relaxed"',
    'class="bg-navy text-cream p-3 rounded-2xl rounded-tr-sm shadow-sm max-w-[85%] leading-relaxed font-sans"'
)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
