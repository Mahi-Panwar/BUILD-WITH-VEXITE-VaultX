import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add new tabs to Sidebar (Desktop & Mobile)
old_sidebar = '''            <button data-dtab="settings" class="w-full flex items-center gap-4 px-4 py-3 rounded-xl transition-all font-medium ${state.dashTab==='settings'?'bg-blue-600 text-white shadow-lg shadow-blue-600/20':'text-slate-400 hover:text-white hover:bg-slate-800'}">
              <i class="fas fa-cog w-5 text-center"></i> Settings
            </button>'''
new_sidebar = '''            <button data-dtab="cards" class="w-full flex items-center gap-4 px-4 py-3 rounded-xl transition-all font-medium ${state.dashTab==='cards'?'bg-blue-600 text-white shadow-lg shadow-blue-600/20':'text-slate-400 hover:text-white hover:bg-slate-800'}">
              <i class="fas fa-credit-card w-5 text-center"></i> Virtual Cards
            </button>
            <button data-dtab="loans" class="w-full flex items-center gap-4 px-4 py-3 rounded-xl transition-all font-medium ${state.dashTab==='loans'?'bg-blue-600 text-white shadow-lg shadow-blue-600/20':'text-slate-400 hover:text-white hover:bg-slate-800'}">
              <i class="fas fa-hand-holding-usd w-5 text-center"></i> Loans
            </button>
            <button data-dtab="settings" class="w-full flex items-center gap-4 px-4 py-3 rounded-xl transition-all font-medium ${state.dashTab==='settings'?'bg-blue-600 text-white shadow-lg shadow-blue-600/20':'text-slate-400 hover:text-white hover:bg-slate-800'}">
              <i class="fas fa-cog w-5 text-center"></i> Settings / Update Profile
            </button>'''
content = content.replace(old_sidebar, new_sidebar)

# 2. Add Global "Update Account" button to Header
old_header = '''           <div class="flex items-center gap-4">
             <div class="px-4 py-2 bg-slate-100 rounded-full text-sm font-medium text-slate-600 border border-slate-200 shadow-inner">
               Status: <span class="text-emerald-500"><i class="fas fa-shield-check"></i> Secured</span>
             </div>
          </div>'''
new_header = '''           <div class="flex items-center gap-4">
             <button data-dtab="settings" class="px-4 py-2 bg-indigo-50 hover:bg-indigo-100 text-indigo-600 rounded-lg text-sm font-bold transition-colors border border-indigo-200">
               <i class="fas fa-user-edit"></i> Edit Profile
             </button>
             <div class="px-4 py-2 bg-slate-100 rounded-full text-sm font-medium text-slate-600 border border-slate-200 shadow-inner hidden lg:block">
               Status: <span class="text-emerald-500"><i class="fas fa-shield-check"></i> Secured</span>
             </div>
          </div>'''
content = content.replace(old_header, new_header)

# 3. Add Cards and Loans tabs logic
cards_tab = '''
  if (state.dashTab === 'cards') {
    return `
      <div class="fade-in max-w-4xl mx-auto space-y-6">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-2xl font-bold text-slate-800">Your Virtual Cards</h2>
            <p class="text-slate-500 text-sm">Manage your debit and credit cards securely.</p>
          </div>
          <button class="px-4 py-2 bg-slate-900 text-white rounded-lg text-sm font-bold hover:bg-slate-800 transition-colors">
            <i class="fas fa-plus"></i> Request New Card
          </button>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <!-- Card 1 -->
          <div class="relative w-full h-56 bg-gradient-to-br from-slate-900 to-slate-800 rounded-3xl p-6 text-white shadow-2xl overflow-hidden flex flex-col justify-between group">
            <div class="absolute top-0 right-0 w-64 h-64 bg-white opacity-5 rounded-full -mr-20 -mt-20 group-hover:scale-110 transition-transform duration-700"></div>
            <div class="flex justify-between items-start relative z-10">
              <div class="text-lg font-bold tracking-widest text-slate-300">VaultX <span class="text-white">PLATINUM</span></div>
              <i class="fas fa-wifi text-xl opacity-80"></i>
            </div>
            <div class="relative z-10">
              <div class="font-mono text-2xl tracking-[0.2em] mb-2 shadow-sm">4532 9912 **** ${String(accNo).substring(0,4).padEnd(4,'8')}</div>
              <div class="flex justify-between text-xs font-medium uppercase tracking-widest text-slate-300">
                <span>${esc(user.name)}</span>
                <span>12/29</span>
              </div>
            </div>
          </div>
          
          <!-- Card Controls -->
          <div class="bg-white p-6 rounded-3xl shadow-sm border border-slate-200">
            <h3 class="font-bold text-slate-800 mb-4">Card Settings</h3>
            <div class="space-y-4">
              <div class="flex items-center justify-between p-4 bg-slate-50 rounded-xl border border-slate-100">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center"><i class="fas fa-snowflake"></i></div>
                  <div>
                    <div class="font-bold text-slate-800 text-sm">Freeze Card</div>
                    <div class="text-xs text-slate-500">Temporarily lock all transactions</div>
                  </div>
                </div>
                <div class="w-12 h-6 bg-slate-300 rounded-full relative cursor-pointer hover:bg-slate-400 transition-colors">
                  <div class="w-5 h-5 bg-white rounded-full absolute top-0.5 left-0.5 shadow-sm"></div>
                </div>
              </div>
              <div class="flex items-center justify-between p-4 bg-slate-50 rounded-xl border border-slate-100">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center"><i class="fas fa-plane"></i></div>
                  <div>
                    <div class="font-bold text-slate-800 text-sm">International Usage</div>
                    <div class="text-xs text-slate-500">Enable foreign transactions</div>
                  </div>
                </div>
                <div class="w-12 h-6 bg-blue-500 rounded-full relative cursor-pointer hover:bg-blue-600 transition-colors">
                  <div class="w-5 h-5 bg-white rounded-full absolute top-0.5 right-0.5 shadow-sm"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;
  }
  
  if (state.dashTab === 'loans') {
    return `
      <div class="fade-in max-w-4xl mx-auto space-y-6">
        <div>
          <h2 class="text-2xl font-bold text-slate-800">Loan Center</h2>
          <p class="text-slate-500 text-sm">Instant pre-approved loans with competitive interest rates.</p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="bg-indigo-50 border border-indigo-100 p-6 rounded-3xl">
            <h3 class="font-bold text-indigo-900 mb-1">Personal Loan</h3>
            <div class="text-indigo-600 text-2xl font-bold mb-4">Up to ₹5,00,000</div>
            <p class="text-sm text-indigo-700/80 mb-6">Rates starting at 10.5% p.a. Minimal documentation required.</p>
            <button class="w-full bg-indigo-600 text-white py-2 rounded-xl text-sm font-bold shadow-md hover:bg-indigo-700 transition-colors">Apply Now</button>
          </div>
          <div class="bg-emerald-50 border border-emerald-100 p-6 rounded-3xl">
            <h3 class="font-bold text-emerald-900 mb-1">Home Loan</h3>
            <div class="text-emerald-600 text-2xl font-bold mb-4">Up to ₹2 Crores</div>
            <p class="text-sm text-emerald-700/80 mb-6">Rates starting at 8.3% p.a. Flexible repayment tenure up to 30 years.</p>
            <button class="w-full bg-emerald-600 text-white py-2 rounded-xl text-sm font-bold shadow-md hover:bg-emerald-700 transition-colors">Calculate EMI</button>
          </div>
          <div class="bg-white border border-slate-200 p-6 rounded-3xl shadow-sm flex flex-col justify-center items-center text-center">
            <div class="w-16 h-16 bg-slate-100 text-slate-400 rounded-full flex items-center justify-center text-2xl mb-4"><i class="fas fa-file-invoice-dollar"></i></div>
            <h3 class="font-bold text-slate-800">No Active Loans</h3>
            <p class="text-sm text-slate-500 mt-2">You currently do not have any active loans linked to this account.</p>
          </div>
        </div>
      </div>
    `;
  }
'''
content = content.replace("  if (state.dashTab === 'settings') {", cards_tab + "\n  if (state.dashTab === 'settings') {")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
