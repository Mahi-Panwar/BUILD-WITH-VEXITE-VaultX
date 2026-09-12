import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Cards Tab UI
old_cards_ui = """            <div class="relative z-10">
              <div class="font-mono text-2xl tracking-[0.2em] mb-2 shadow-sm">4532 9912 **** ${String(accNo).substring(0,4).padEnd(4,'8')}</div>
              <div class="flex justify-between text-xs font-medium uppercase tracking-widest text-slate-300">
                <span>${esc(user.name)}</span>
                <span>12/29</span>
              </div>
            </div>"""

new_cards_ui = """            <div class="relative z-10">
              <div class="font-mono text-2xl tracking-[0.2em] mb-2 shadow-sm">${user.card_number ? user.card_number.match(/.{1,4}/g).join(' ') : '4532 9912 **** ' + String(accNo).substring(0,4).padEnd(4,'8')}</div>
              <div class="flex justify-between text-xs font-medium uppercase tracking-widest text-slate-300">
                <span>${esc(user.name)}</span>
                <span class="flex items-center gap-4">
                  <span>CVV: ***</span>
                  <span>EXP: ${user.expiry || '12/29'}</span>
                </span>
              </div>
            </div>"""

content = content.replace(old_cards_ui, new_cards_ui)

# 2. Update Loans Tab UI
old_loans_ui = """          <div class="bg-indigo-50 border border-indigo-100 p-6 rounded-3xl">
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
          </div>"""

new_loans_ui = """          <div class="bg-indigo-50 border border-indigo-100 p-6 rounded-3xl">
            <h3 class="font-bold text-indigo-900 mb-1">Personal Loan</h3>
            <div class="text-indigo-600 text-2xl font-bold mb-4">Up to ₹5,00,000</div>
            <p class="text-sm text-indigo-700/80 mb-6">Rates starting at 10.5% p.a. Minimal documentation required.</p>
            <button onclick="applyLoan('Personal', 500000)" class="w-full bg-indigo-600 text-white py-2 rounded-xl text-sm font-bold shadow-md hover:bg-indigo-700 transition-colors">Instant Approval ₹5L</button>
          </div>
          <div class="bg-emerald-50 border border-emerald-100 p-6 rounded-3xl">
            <h3 class="font-bold text-emerald-900 mb-1">Home Loan</h3>
            <div class="text-emerald-600 text-2xl font-bold mb-4">Up to ₹2 Crores</div>
            <p class="text-sm text-emerald-700/80 mb-6">Rates starting at 8.3% p.a. Flexible repayment tenure up to 30 years.</p>
            <button onclick="applyLoan('Home', 20000000)" class="w-full bg-emerald-600 text-white py-2 rounded-xl text-sm font-bold shadow-md hover:bg-emerald-700 transition-colors">Apply For ₹2Cr</button>
          </div>
          
          <div class="bg-white border border-slate-200 p-6 rounded-3xl shadow-sm flex flex-col items-center text-center overflow-y-auto max-h-64">
            ${(!user.loans || user.loans.length === 0) ? `
              <div class="flex-1 flex flex-col items-center justify-center">
                <div class="w-16 h-16 bg-slate-100 text-slate-400 rounded-full flex items-center justify-center text-2xl mb-4"><i class="fas fa-file-invoice-dollar"></i></div>
                <h3 class="font-bold text-slate-800">No Active Loans</h3>
                <p class="text-sm text-slate-500 mt-2">You currently do not have any active loans.</p>
              </div>
            ` : `
              <div class="w-full text-left">
                <h3 class="font-bold text-slate-800 mb-4 sticky top-0 bg-white z-10 pb-2 border-b">Active Loans</h3>
                <div class="space-y-3">
                  ${user.loans.map(l => `
                    <div class="p-3 bg-slate-50 rounded-xl border border-slate-100 flex justify-between items-center">
                      <div>
                        <div class="font-bold text-slate-700 text-sm">${l.type} Loan</div>
                        <div class="text-xs text-slate-500">ID: ${l.id}</div>
                      </div>
                      <div class="text-right">
                        <div class="font-bold text-emerald-600 text-sm">₹${l.amount.toLocaleString()}</div>
                        <div class="text-[10px] font-bold uppercase tracking-wider text-emerald-500 bg-emerald-100 px-2 py-0.5 rounded">${l.status}</div>
                      </div>
                    </div>
                  `).join('')}
                </div>
              </div>
            `}
          </div>"""

content = content.replace(old_loans_ui, new_loans_ui)

# 3. Add applyLoan function to scripts
apply_loan_js = """
  window.applyLoan = async function(loanType, amount) {
    if (!confirm(`Are you sure you want to apply for a ${loanType} loan of ₹${amount.toLocaleString()}?`)) return;
    
    showToast(`Applying for ${loanType} loan...`, true);
    try {
      const res = await apiCall('/api/loan', {
        accountNo: user.accountNo || user['accountNo.'],
        pin: state.sessionPin,
        loanType: loanType,
        amount: amount
      });
      
      if (res.ok) {
        showToast(res.msg, true);
        await refreshUser();
        render();
      } else {
        showToast(res.msg, false);
      }
    } catch (e) {
      showToast("Network Error", false);
    }
  };
"""

content = content.replace("async function render() {", apply_loan_js + "\n  async function render() {")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
