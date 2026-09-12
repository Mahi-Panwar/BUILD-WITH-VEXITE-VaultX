import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Make the body a beautiful dark animated gradient
old_body = 'class="bg-slate-50 text-slate-800 h-screen overflow-hidden font-sans selection:bg-blue-200"'
new_body = 'class="bg-[#0f172a] text-slate-100 h-screen overflow-hidden font-sans selection:bg-cyan-500/30 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-slate-900 via-[#0a0a0a] to-slate-900"'
content = content.replace(old_body, new_body)

# Update the overall container (from white bg to glass)
content = content.replace('class="bg-white rounded-[2rem] shadow-2xl border border-slate-200', 'class="bg-white/5 backdrop-blur-2xl rounded-[2rem] shadow-[0_0_50px_rgba(8,112,184,0.15)] border border-white/10')
# The landing page left panel
content = content.replace('class="w-full lg:w-1/2 p-12 lg:p-20 flex flex-col justify-center relative"', 'class="w-full lg:w-1/2 p-12 lg:p-20 flex flex-col justify-center relative z-10"')

# Update Sidebar Background
content = content.replace('class="w-64 bg-slate-900 text-white flex flex-col shrink-0 hidden md:flex relative z-20 shadow-2xl"', 'class="w-64 bg-black/40 backdrop-blur-xl border-r border-white/10 text-white flex flex-col shrink-0 hidden md:flex relative z-20 shadow-2xl"')
content = content.replace('class="p-8 border-b border-slate-800/60 shrink-0"', 'class="p-8 border-b border-white/10 shrink-0"')
content = content.replace('class="p-6 border-t border-slate-800/60 shrink-0 bg-slate-900/50"', 'class="p-6 border-t border-white/10 shrink-0 bg-black/20"')

# Update header background
content = content.replace('class="h-20 bg-white/80 backdrop-blur-md border-b border-slate-200', 'class="h-20 bg-white/5 backdrop-blur-xl border-b border-white/10')
content = content.replace('text-slate-800 capitalize', 'text-white capitalize tracking-wide')

# Update general panels inside Dashboard
# Overview / Cards / Loans containers
content = content.replace('bg-white p-6 rounded-3xl shadow-sm border border-slate-200', 'bg-white/5 backdrop-blur-xl p-6 rounded-3xl shadow-lg border border-white/10')
content = content.replace('bg-white p-8 rounded-3xl shadow-sm border border-slate-200', 'bg-white/5 backdrop-blur-xl p-8 rounded-3xl shadow-lg border border-white/10')
content = content.replace('bg-white rounded-3xl shadow-sm border border-slate-200', 'bg-white/5 backdrop-blur-xl rounded-3xl shadow-lg border border-white/10')
content = content.replace('bg-slate-50 p-6 border-b border-slate-200', 'bg-white/5 p-6 border-b border-white/10')
content = content.replace('bg-white rounded-3xl shadow-xl border border-slate-100', 'bg-white/5 backdrop-blur-xl rounded-3xl shadow-[0_0_30px_rgba(0,0,0,0.3)] border border-white/10')
content = content.replace('bg-indigo-50 p-8 border-b border-indigo-100', 'bg-gradient-to-r from-cyan-500/20 to-blue-500/20 p-8 border-b border-white/10')

# Update Text colors universally in panels
content = content.replace('text-slate-900', 'text-white')
content = content.replace('text-slate-800', 'text-slate-100')
content = content.replace('text-slate-700', 'text-slate-200')
content = content.replace('text-slate-600', 'text-slate-300')

# Input fields glass effect
content = content.replace('bg-slate-50 focus:bg-white', 'bg-black/20 focus:bg-black/40 text-white placeholder-slate-400')
content = content.replace('border-slate-200', 'border-white/10')
content = content.replace('border-slate-100', 'border-white/5')

# Buttons gradient replacements
content = content.replace('bg-blue-600', 'bg-gradient-to-r from-cyan-500 to-blue-600')
content = content.replace('hover:bg-blue-700', 'hover:from-cyan-400 hover:to-blue-500')
content = content.replace('bg-indigo-600', 'bg-gradient-to-r from-purple-500 to-pink-600')
content = content.replace('hover:bg-indigo-700', 'hover:from-purple-400 hover:to-pink-500')

# Fix tables
content = content.replace('class="bg-white"', 'class="bg-transparent"')
content = content.replace('bg-slate-50 border-b border-slate-200', 'bg-white/5 border-b border-white/10')
content = content.replace('hover:bg-slate-50', 'hover:bg-white/10')

# Chat Widget glass styling
content = content.replace('class="hidden w-80 sm:w-96 bg-white', 'class="hidden w-80 sm:w-96 bg-[#0f172a]/90 backdrop-blur-2xl border-white/10')
content = content.replace('bg-slate-900 text-white', 'bg-gradient-to-r from-cyan-500 to-blue-600 text-white')
content = content.replace('id="chat-messages" class="flex-1 p-4 overflow-y-auto bg-slate-50', 'id="chat-messages" class="flex-1 p-4 overflow-y-auto bg-transparent')
content = content.replace('class="p-3 bg-white border-t border-slate-100', 'class="p-3 bg-transparent border-t border-white/10')

# Landing page specific fixes
content = content.replace('bg-slate-50 px-8', 'bg-black/20 backdrop-blur-xl px-8')
content = content.replace('bg-white px-8', 'bg-transparent px-8')
content = content.replace('bg-indigo-50 border border-indigo-100', 'bg-white/5 border border-white/10')
content = content.replace('bg-emerald-50 border border-emerald-100', 'bg-white/5 border border-white/10')
content = content.replace('text-indigo-900', 'text-cyan-300')
content = content.replace('text-emerald-900', 'text-emerald-300')
content = content.replace('text-indigo-600', 'text-cyan-400')
content = content.replace('text-emerald-600', 'text-emerald-400')
content = content.replace('text-indigo-700/80', 'text-cyan-200/80')
content = content.replace('text-emerald-700/80', 'text-emerald-200/80')
content = content.replace('bg-slate-100 text-slate-400', 'bg-white/10 text-slate-300')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
