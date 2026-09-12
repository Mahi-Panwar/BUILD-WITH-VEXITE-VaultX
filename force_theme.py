import re
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's just unconditionally force the style in the script block
content = content.replace("bg-cream border border-ledgerline text-navy p-3 rounded-2xl rounded-tl-sm", "bg-cream border border-ledgerline text-sage p-3 rounded-2xl rounded-tl-sm font-handwriting text-2xl font-bold")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
