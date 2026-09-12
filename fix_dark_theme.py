import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Fix chat bubbles for dark theme
content = content.replace("bg-white border border-slate-200 text-slate-800", "bg-white/10 border border-white/10 text-white backdrop-blur-md")
content = content.replace("bg-white border-slate-200 text-slate-500", "bg-white/10 border border-white/10 text-slate-300 backdrop-blur-md")
content = content.replace("bg-blue-600 text-white", "bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-[0_0_15px_rgba(8,112,184,0.4)]")

# Fix quick action cards (Deposit, Withdraw, Transfer) from old light theme
content = content.replace('class="bg-white p-5', 'class="bg-white/5 backdrop-blur-xl border border-white/10 p-5')
content = content.replace('bg-emerald-50 text-emerald-600', 'bg-emerald-500/20 text-emerald-400')
content = content.replace('bg-rose-50 text-rose-600', 'bg-rose-500/20 text-rose-400')
content = content.replace('bg-indigo-50 text-indigo-600', 'bg-cyan-500/20 text-cyan-400')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
