import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Add Transfer and History to desktop nav
old_nav = '''            <button data-dtab="settings" class="w-full flex items-center gap-4 px-4 py-3 rounded-xl transition-all font-medium ${state.dashTab==='settings'?'bg-blue-600 text-white shadow-lg shadow-blue-600/20':'text-slate-400 hover:text-white hover:bg-slate-800'}">
              <i class="fas fa-cog w-5 text-center"></i> Settings
            </button>'''
new_nav = '''            <button data-dtab="transfer" class="w-full flex items-center gap-4 px-4 py-3 rounded-xl transition-all font-medium ${state.dashTab==='transfer'?'bg-blue-600 text-white shadow-lg shadow-blue-600/20':'text-slate-400 hover:text-white hover:bg-slate-800'}">
              <i class="fas fa-exchange-alt w-5 text-center"></i> Transfer
            </button>
            <button data-dtab="history" class="w-full flex items-center gap-4 px-4 py-3 rounded-xl transition-all font-medium ${state.dashTab==='history'?'bg-blue-600 text-white shadow-lg shadow-blue-600/20':'text-slate-400 hover:text-white hover:bg-slate-800'}">
              <i class="fas fa-history w-5 text-center"></i> History
            </button>
            <button data-dtab="settings" class="w-full flex items-center gap-4 px-4 py-3 rounded-xl transition-all font-medium ${state.dashTab==='settings'?'bg-blue-600 text-white shadow-lg shadow-blue-600/20':'text-slate-400 hover:text-white hover:bg-slate-800'}">
              <i class="fas fa-cog w-5 text-center"></i> Settings
            </button>'''
content = content.replace(old_nav, new_nav)

# Add to mobile nav
old_mobile = '''           <button data-dtab="settings" class="px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap ${state.dashTab==='settings'?'bg-blue-50 text-blue-600 border border-blue-100':'text-slate-600'}">Settings</button>'''
new_mobile = '''           <button data-dtab="transfer" class="px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap ${state.dashTab==='transfer'?'bg-blue-50 text-blue-600 border border-blue-100':'text-slate-600'}">Transfer</button>
           <button data-dtab="history" class="px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap ${state.dashTab==='history'?'bg-blue-50 text-blue-600 border border-blue-100':'text-slate-600'}">History</button>
           <button data-dtab="settings" class="px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap ${state.dashTab==='settings'?'bg-blue-50 text-blue-600 border border-blue-100':'text-slate-600'}">Settings</button>'''
content = content.replace(old_mobile, new_mobile)

# Add to dashboard quick actions
old_actions = '''            <!-- Quick Action Cards -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">'''
new_actions = '''            <!-- Quick Action Cards -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <button data-dtab="transfer" class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition-all text-left group flex flex-col justify-between items-start gap-4">
                <div class="w-12 h-12 bg-indigo-50 text-indigo-600 rounded-xl flex items-center justify-center text-xl group-hover:scale-110 transition-transform">
                  <i class="fas fa-exchange-alt"></i>
                </div>
                <div>
                  <h3 class="font-bold text-slate-800">Transfer</h3>
                  <p class="text-xs text-slate-500 mt-1">Send money</p>
                </div>
              </button>'''
# Actually wait, my dashboard quick actions used flex-row. Let's just rewrite the whole Quick Action block.
content = re.sub(
r'<!-- Quick Action Cards -->.*?</div>\s+</div>\s+</div>', 
r'''<!-- Quick Action Cards -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <button data-dtab="deposit" class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition-all text-left group">
                <div class="w-12 h-12 bg-emerald-50 text-emerald-600 rounded-xl flex items-center justify-center text-xl group-hover:scale-110 transition-transform mb-3">
                  <i class="fas fa-arrow-down"></i>
                </div>
                <h3 class="font-bold text-slate-800">Deposit</h3>
                <p class="text-xs text-slate-500 mt-1">Add funds</p>
              </button>
              <button data-dtab="withdraw" class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition-all text-left group">
                <div class="w-12 h-12 bg-rose-50 text-rose-600 rounded-xl flex items-center justify-center text-xl group-hover:scale-110 transition-transform mb-3">
                  <i class="fas fa-arrow-up"></i>
                </div>
                <h3 class="font-bold text-slate-800">Withdraw</h3>
                <p class="text-xs text-slate-500 mt-1">Remove funds</p>
              </button>
              <button data-dtab="transfer" class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition-all text-left group">
                <div class="w-12 h-12 bg-indigo-50 text-indigo-600 rounded-xl flex items-center justify-center text-xl group-hover:scale-110 transition-transform mb-3">
                  <i class="fas fa-exchange-alt"></i>
                </div>
                <h3 class="font-bold text-slate-800">Transfer</h3>
                <p class="text-xs text-slate-500 mt-1">Send to account</p>
              </button>
            </div>
          </div>''', content, flags=re.DOTALL)

# Add the new tabs rendering to renderDashPanel
new_tabs = '''
  if (state.dashTab === 'transfer') {
    return `
      <div class="fade-in max-w-2xl mx-auto">
        <div class="bg-white rounded-3xl shadow-xl border border-slate-100 overflow-hidden">
          <div class="bg-indigo-50 p-8 border-b border-indigo-100 flex items-center justify-between">
            <div>
              <h2 class="text-2xl font-bold text-indigo-800 mb-1">Transfer Funds</h2>
              <p class="text-indigo-600 text-sm">Instantly send money to another account.</p>
            </div>
            <div class="w-16 h-16 bg-white rounded-full flex items-center justify-center shadow-sm text-3xl text-indigo-500">
              <i class="fas fa-exchange-alt"></i>
            </div>
          </div>
          <div class="p-8">
            <form id="transferForm" class="space-y-6">
              <div>
                <label class="block text-sm font-bold text-slate-700 mb-2 uppercase tracking-wide">Target Account No / Email</label>
                <input type="text" id="tr_target" placeholder="Recipient's info" required class="w-full px-5 py-4 rounded-xl border-2 border-slate-200 bg-slate-50 focus:bg-white focus:ring-0 focus:border-indigo-500 outline-none text-lg font-medium text-slate-800 transition-all">
              </div>
              <div>
                <label class="block text-sm font-bold text-slate-700 mb-2 uppercase tracking-wide">Amount to Transfer</label>
                <div class="relative flex items-center">
                  <span class="absolute left-6 text-2xl text-slate-400 font-light">₹</span>
                  <input type="number" id="tr_amt" min="1" max="${balance}" placeholder="1000" required class="w-full pl-12 pr-6 py-5 rounded-2xl border-2 border-slate-200 bg-slate-50 focus:bg-white focus:ring-0 focus:border-indigo-500 outline-none text-3xl font-bold text-slate-800 transition-all font-mono">
                </div>
              </div>
              <button type="submit" class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-lg py-5 rounded-2xl transition-all shadow-lg shadow-indigo-600/30 flex justify-center items-center gap-3 mt-4">
                Confirm Transfer <i class="fas fa-paper-plane"></i>
              </button>
            </form>
          </div>
        </div>
      </div>
    `;
  }
  
  if (state.dashTab === 'history') {
    const txs = user.transactions || [];
    const rows = txs.map(t => `
      <tr class="border-b border-slate-100 hover:bg-slate-50 transition-colors">
        <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-500">${t.date}</td>
        <td class="px-6 py-4 whitespace-nowrap">
          <span class="px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full 
            ${t.type === 'DEPOSIT' || t.type === 'TRANSFER IN' ? 'bg-emerald-100 text-emerald-800' : 
              t.type === 'WITHDRAWAL' || t.type === 'TRANSFER OUT' ? 'bg-rose-100 text-rose-800' : 'bg-blue-100 text-blue-800'}">
            ${t.type}
          </span>
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-700">${t.detail || ''}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm font-mono font-bold text-right ${t.type === 'DEPOSIT' || t.type === 'TRANSFER IN' ? 'text-emerald-600' : t.type==='CREATE'?'text-slate-500':'text-rose-600'}">
          ${t.type === 'DEPOSIT' || t.type === 'TRANSFER IN' ? '+' : t.type==='CREATE'?'':'-'}₹${t.amount.toLocaleString('en-IN')}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm font-mono font-bold text-slate-800 text-right">
          ₹${t.balance.toLocaleString('en-IN')}
        </td>
      </tr>
    `).join('');
    
    return `
      <div class="fade-in max-w-5xl mx-auto">
        <div class="bg-white rounded-3xl shadow-sm border border-slate-200 overflow-hidden">
          <div class="bg-slate-50 p-6 border-b border-slate-200 flex justify-between items-center">
            <h3 class="text-xl font-bold text-slate-800 flex items-center gap-2"><i class="fas fa-history text-slate-500"></i> Transaction History</h3>
            <span class="text-sm font-medium text-slate-500">${txs.length} total records</span>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead class="bg-slate-50 border-b border-slate-200">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Date/Time</th>
                  <th class="px-6 py-3 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Type</th>
                  <th class="px-6 py-3 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Details</th>
                  <th class="px-6 py-3 text-right text-xs font-bold text-slate-500 uppercase tracking-wider">Amount</th>
                  <th class="px-6 py-3 text-right text-xs font-bold text-slate-500 uppercase tracking-wider">Balance</th>
                </tr>
              </thead>
              <tbody class="bg-white">
                ${rows.length ? rows : '<tr><td colspan="5" class="px-6 py-10 text-center text-slate-500">No transactions found.</td></tr>'}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    `;
  }
'''
content = content.replace("  if (state.dashTab === 'settings') {", new_tabs + "\n  if (state.dashTab === 'settings') {")

# Add wiring for transfer
wiring = '''
  const transferForm = document.getElementById('transferForm');
  if (transferForm) transferForm.onsubmit = async e => {
    e.preventDefault();
    const btn = transferForm.querySelector('button');
    const oldHtml = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin text-xl"></i>';

    const target = document.getElementById('tr_target').value;
    const amt = Number(document.getElementById('tr_amt').value);
    const res = await apiCall('/api/transfer', { accountNo: user.accountNo || user['accountNo.'], pin: state.sessionPin, targetAccount: target, amount: amt });
    if (res.ok) {
      showToast(`Successfully transferred ₹${amt.toLocaleString()}`, true);
      await refreshUser();
      state.dashTab = 'dashboard';
    } else {
      showToast(res.msg, false);
      btn.innerHTML = oldHtml;
    }
    render();
  };
'''
content = content.replace("  const updateForm = document.getElementById('updateForm');", wiring + "\n  const updateForm = document.getElementById('updateForm');")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
