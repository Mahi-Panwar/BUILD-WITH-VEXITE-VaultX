import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Fix the sidebar inactive buttons. 
# They currently look like: "text-navy/70 hover:text-cream hover:brightness-110" on a dark background.
# They should be: "text-cream/70 hover:text-cream"
content = content.replace("text-navy/70 hover:text-cream hover:brightness-110", "text-cream/70 hover:text-cream hover:brightness-110")
content = content.replace("text-navy/70 hover:text-cream hover:bg-slate-800", "text-cream/70 hover:text-cream hover:bg-black/20")

# Fix footer text (currently text-navy/70 on bg-walnut)
# The footer uses class="bg-walnut py-12 px-8 text-navy/70"
content = content.replace('class="bg-walnut py-12 px-8 text-navy/70"', 'class="bg-walnut py-12 px-8 text-cream/70"')

# Fix mobile topbar text
# The topbar uses class="md:hidden w-full bg-walnut text-cream h-16...
# and the logout button uses class="text-xs bg-rose-500/20 text-brass px-3 py-1.5... wait
content = content.replace('class="md:hidden flex overflow-x-auto bg-cream border-b border-ledgerline shrink-0 px-2 py-2 gap-2"', 'class="md:hidden flex overflow-x-auto bg-cream border-b border-ledgerline shrink-0 px-2 py-2 gap-2 shadow-sm"')

# Also, there's a problem with the Chat header:
# bg-walnut text-cream p-4 ... It's probably fine, but text-slate-300 was replaced with text-cream/70 which is fine.

# What about the Hero text on the dark background?
# "text-navy text-2xl font-bold mb-4" on the landing page might be wrong.
# Let's fix the landing page text colors in the dark sections.
landing_hero = r'<div class="relative max-w-6xl mx-auto px-8 py-24 z-10 flex flex-col md:flex-row items-center gap-12">'
# If there's dark text on the dark hero background, make it cream.
content = content.replace('text-navy text-5xl', 'text-cream text-5xl')
content = content.replace('text-navy/70 text-lg', 'text-cream/80 text-lg')
content = content.replace('text-navy/70 max-w-2xl', 'text-cream/80 max-w-2xl')

# Let's make sure brass buttons with text-walnut are readable. 
# Brass is #C89B4A. Walnut is #2B211A. This contrast is excellent.
# What about "text-navy" on "bg-cream"? That is #1B2740 on #F3ECDC. Very high contrast.

# In the statistics section (which was originally bg-blue-600, now bg-brass text-walnut):
content = content.replace('bg-brass text-walnut text-cream px-8', 'bg-brass text-walnut px-8')
content = content.replace('text-cream text-sm font-medium', 'text-walnut/80 text-sm font-medium')
content = content.replace('text-cream/70 text-sm font-medium uppercase', 'text-walnut/80 text-sm font-medium uppercase')

# Let's globally check any text-navy/70 that are inside bg-walnut and fix them.
# The sidebar bottom profile section:
# class="p-6 border-t border-mahogany shrink-0 bg-walnut/50"
# text-xs text-navy/70 font-mono truncate -> text-cream/70
content = content.replace('text-xs text-navy/70 font-mono truncate', 'text-xs text-cream/70 font-mono truncate')

# Quick Links in Footer
# text-brass -> should be text-cream for footer links maybe? Or text-brass is fine.
content = content.replace('hover:text-brass', 'hover:text-cream transition-colors')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
