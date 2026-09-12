import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add Tailwind Config
tailwind_config = """<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@500;700&family=Courier+Prime:ital,wght@0,400;0,700;1,400&family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
<script>
  tailwind.config = {
    theme: {
      extend: {
        colors: {
          walnut: '#2B211A',
          mahogany: '#3E2F22',
          cream: '#F3ECDC',
          navy: '#1B2740',
          brass: '#C89B4A',
          sage: '#5C7A63',
          ledgerline: '#E5D6C1'
        },
        fontFamily: {
          serif: ['"Playfair Display"', 'Georgia', 'serif'],
          mono: ['"Courier Prime"', '"Courier New"', 'monospace'],
          sans: ['"Playfair Display"', 'serif'],
          handwriting: ['"Caveat"', 'cursive'],
        }
      }
    }
  }
</script>
<style>
  body { font-family: 'Playfair Display', serif; }
  .ledger-bg { background: repeating-linear-gradient(transparent, transparent 31px, #E5D6C1 31px, #E5D6C1 32px); }
</style>
"""

content = re.sub(r'<script src="https://cdn\.tailwindcss\.com"></script>', tailwind_config, content)

# 2. General Color Replacements
# Backgrounds
content = re.sub(r'bg-slate-900|bg-slate-800', 'bg-walnut', content)
content = re.sub(r'bg-white', 'bg-cream', content)
content = re.sub(r'bg-slate-50|bg-slate-100|bg-blue-50|bg-indigo-50|bg-emerald-50|bg-orange-50', 'bg-cream', content)
content = re.sub(r'bg-slate-200', 'bg-ledgerline', content)

# Text colors
content = re.sub(r'text-slate-800|text-slate-900|text-slate-700', 'text-navy', content)
content = re.sub(r'text-slate-500|text-slate-600|text-slate-400', 'text-navy/70', content)
content = re.sub(r'text-slate-300|text-slate-200', 'text-cream/70', content)

# Accents (Buttons, Icons)
content = re.sub(r'bg-blue-600|bg-indigo-600|bg-emerald-600', 'bg-brass text-walnut', content)
content = re.sub(r'hover:bg-blue-700|hover:bg-indigo-700|hover:bg-emerald-700|hover:bg-slate-800', 'hover:brightness-110', content)
content = re.sub(r'text-blue-600|text-indigo-600|text-emerald-600|text-orange-600|text-blue-500|text-emerald-500', 'text-brass', content)
content = re.sub(r'text-white', 'text-cream', content)
content = re.sub(r'border-blue-600|border-indigo-600|border-emerald-600|border-blue-500|border-indigo-500', 'border-brass', content)
content = re.sub(r'shadow-blue-600/20|shadow-blue-600/30|shadow-indigo-600/30', 'shadow-brass/20', content)

# Borders
content = re.sub(r'border-slate-100|border-slate-200|border-slate-800', 'border-ledgerline', content)
content = re.sub(r'border-slate-800/60', 'border-mahogany', content)

# 3. Chatbot Specific Colors (Sage for bot, Navy for user)
# User message bubble inside chat
# We have `bg-brass text-walnut` (from blue-600 replacement) for user bubble. Let's make it navy.
content = content.replace('bg-brass text-walnut text-cream p-3 rounded-2xl rounded-tr-sm', 'bg-navy text-cream p-3 rounded-2xl rounded-tr-sm')

# Bot message bubble
bot_bubble_old = 'bg-cream border border-ledgerline text-navy p-3 rounded-2xl rounded-tl-sm'
bot_bubble_new = 'bg-cream border border-ledgerline text-sage font-handwriting text-xl p-3 rounded-2xl rounded-tl-sm'
content = content.replace(bot_bubble_old, bot_bubble_new)

# Add ledger-bg class to panels
content = content.replace('class="p-8 bg-cream"', 'class="p-8 bg-cream ledger-bg"')
content = content.replace('bg-cream rounded-3xl shadow-xl', 'bg-cream rounded-3xl shadow-2xl border-4 border-brass ledger-bg')

# Hero gradient replace
content = re.sub(r'bg-gradient-to-br from-cream to-cream', 'bg-gradient-to-br from-walnut to-mahogany', content)
content = re.sub(r'bg-gradient-to-br from-slate-900 to-slate-800', 'bg-gradient-to-br from-walnut to-mahogany', content)

# Some remaining odd classes
content = content.replace('bg-brass text-walnut hover:brightness-110 text-cream', 'bg-brass text-walnut hover:brightness-110')
content = content.replace('text-brass text-2xl font-bold mb-4', 'text-navy text-2xl font-bold mb-4') # Headings shouldn't all be brass

# Ensure the body uses the walnut/mahogany background for the "desk"
content = content.replace('<body class="bg-cream', '<body class="bg-gradient-to-br from-walnut to-mahogany min-h-screen text-cream')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
