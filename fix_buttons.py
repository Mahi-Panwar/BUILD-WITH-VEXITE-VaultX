import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update "Request New Card" button
old_req_card = """<button class="px-4 py-2 bg-slate-900 text-white rounded-lg text-sm font-bold hover:bg-slate-800 transition-colors">
            <i class="fas fa-plus"></i> Request New Card
          </button>"""
new_req_card = """<button onclick="requestNewCard()" class="px-4 py-2 bg-slate-900 text-white rounded-lg text-sm font-bold hover:bg-slate-800 transition-colors shadow-lg active:scale-95">
            <i class="fas fa-plus"></i> Request New Card
          </button>"""
content = content.replace(old_req_card, new_req_card)

# 2. Update Loan buttons back to exact text user wants and wire up Calculate EMI
old_loan_personal = """<button onclick="applyLoan('Personal', 500000)" class="w-full bg-indigo-600 text-white py-2 rounded-xl text-sm font-bold shadow-md hover:bg-indigo-700 transition-colors">Instant Approval ₹5L</button>"""
new_loan_personal = """<button onclick="applyLoan('Personal', 500000)" class="w-full bg-indigo-600 text-white py-2 rounded-xl text-sm font-bold shadow-md hover:bg-indigo-700 transition-colors active:scale-95">Apply Now</button>"""
content = content.replace(old_loan_personal, new_loan_personal)

old_loan_home = """<button onclick="applyLoan('Home', 20000000)" class="w-full bg-emerald-600 text-white py-2 rounded-xl text-sm font-bold shadow-md hover:bg-emerald-700 transition-colors">Apply For ₹2Cr</button>"""
new_loan_home = """<button onclick="calculateEMI(20000000, 8.3, 30)" class="w-full bg-emerald-600 text-white py-2 rounded-xl text-sm font-bold shadow-md hover:bg-emerald-700 transition-colors active:scale-95">Calculate EMI</button>"""
content = content.replace(old_loan_home, new_loan_home)

# 3. Add Javascript for requestNewCard and calculateEMI
new_js = """
  window.requestNewCard = async function() {
    if (!confirm("Are you sure you want to request a new virtual card? Your old card number will be deactivated.")) return;
    
    // In a real app, this hits an API. Here we simulate the update and refresh.
    showToast("Generating new secure virtual card...", true);
    
    // Hit a new custom update_card endpoint we will create
    const res = await apiCall('/api/new_card', { accountNo: user.accountNo || user['accountNo.'], pin: state.sessionPin });
    if (res.ok) {
        showToast("New card generated successfully!", true);
        await refreshUser();
        render();
    } else {
        showToast("Failed to generate card.", false);
    }
  };

  window.calculateEMI = function(principal, rate, years) {
    // EMI = [P x R x (1+R)^N]/[(1+R)^N-1]
    const r = (rate / 100) / 12;
    const n = years * 12;
    const emi = (principal * r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1);
    
    alert(`Home Loan EMI Calculator:\\n\\nLoan Amount: ₹${principal.toLocaleString()}\\nInterest Rate: ${rate}% p.a.\\nTenure: ${years} Years\\n\\nEstimated Monthly EMI: ₹${Math.round(emi).toLocaleString()}`);
  };
"""

content = content.replace("window.applyLoan = async function(loanType, amount) {", new_js + "\n  window.applyLoan = async function(loanType, amount) {")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
