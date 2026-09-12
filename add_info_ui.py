import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Registration Form
old_create_form = """      <div class="flex gap-4">
        <div class="w-1/3">
          <label class="block text-sm font-semibold text-slate-700 mb-1.5">Age</label>
          <input type="number" id="cr_age" min="18" max="120" placeholder="18" class="w-full px-4 py-3 rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none transition-all">
        </div>
        <div class="w-2/3">
          <label class="block text-sm font-semibold text-slate-700 mb-1.5">Email</label>
          <input type="email" id="cr_email" placeholder="john@example.com" class="w-full px-4 py-3 rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none transition-all">
        </div>
      </div>
      <div>
        <label class="block text-sm font-semibold text-slate-700 mb-1.5">Choose a 4-Digit PIN</label>"""

new_create_form = """      <div class="flex gap-4">
        <div class="w-1/3">
          <label class="block text-sm font-semibold text-slate-700 mb-1.5">Age</label>
          <input type="number" id="cr_age" min="18" max="120" placeholder="18" class="w-full px-4 py-3 rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none transition-all">
        </div>
        <div class="w-2/3">
          <label class="block text-sm font-semibold text-slate-700 mb-1.5">Email</label>
          <input type="email" id="cr_email" placeholder="john@example.com" class="w-full px-4 py-3 rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none transition-all">
        </div>
      </div>
      <div class="flex gap-4">
        <div class="w-1/2">
          <label class="block text-sm font-semibold text-slate-700 mb-1.5">Phone Number</label>
          <input type="tel" id="cr_phone" placeholder="+1 (555) 000-0000" class="w-full px-4 py-3 rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none transition-all">
        </div>
        <div class="w-1/2">
          <label class="block text-sm font-semibold text-slate-700 mb-1.5">Account Type</label>
          <select id="cr_acctype" class="w-full px-4 py-3 rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none transition-all">
            <option value="Savings">Savings</option>
            <option value="Current">Current</option>
          </select>
        </div>
      </div>
      <div>
        <label class="block text-sm font-semibold text-slate-700 mb-1.5">Full Address</label>
        <input type="text" id="cr_address" placeholder="123 Main St, City, Country" class="w-full px-4 py-3 rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none transition-all">
      </div>
      <div>
        <label class="block text-sm font-semibold text-slate-700 mb-1.5">Choose a 4-Digit PIN</label>"""
content = content.replace(old_create_form, new_create_form)

# 2. Update registration submit wiring
old_cr_submit = """      const pin = document.getElementById('cr_pin').value;
      const res = await apiCall('/api/create', { name, age, email, pin });"""
new_cr_submit = """      const pin = document.getElementById('cr_pin').value;
      const phone = document.getElementById('cr_phone').value;
      const address = document.getElementById('cr_address').value;
      const accType = document.getElementById('cr_acctype').value;
      const res = await apiCall('/api/create', { name, age, email, pin, phone, address, accType });"""
content = content.replace(old_cr_submit, new_cr_submit)

# 3. Update Settings Form
old_settings = """              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Update Name</label>
                  <input type="text" id="up_name" value="${esc(user.name)}" class="w-full px-4 py-3 rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none transition-all">
                </div>
                <div>
                  <label class="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Update Email</label>
                  <input type="email" id="up_email" value="${esc(user.email)}" class="w-full px-4 py-3 rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none transition-all">
                </div>
              </div>
              <div>
                <label class="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">New PIN (Optional)</label>"""

new_settings = """              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Update Name</label>
                  <input type="text" id="up_name" value="${esc(user.name)}" class="w-full px-4 py-3 rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none transition-all">
                </div>
                <div>
                  <label class="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Update Email</label>
                  <input type="email" id="up_email" value="${esc(user.email)}" class="w-full px-4 py-3 rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none transition-all">
                </div>
                <div>
                  <label class="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Update Phone</label>
                  <input type="tel" id="up_phone" value="${esc(user.phone || '')}" class="w-full px-4 py-3 rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none transition-all">
                </div>
                <div>
                  <label class="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Update Address</label>
                  <input type="text" id="up_address" value="${esc(user.address || '')}" class="w-full px-4 py-3 rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none transition-all">
                </div>
              </div>
              <div>
                <label class="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">New PIN (Optional)</label>"""
content = content.replace(old_settings, new_settings)

# 4. Update Settings submit wiring
old_up_submit = """    const name = document.getElementById('up_name').value;
    const email = document.getElementById('up_email').value;
    const newPin = document.getElementById('up_pin').value;
    const res = await apiCall('/api/update', { accountNo: accNo, pin: state.sessionPin, name, email, newPin });"""
new_up_submit = """    const name = document.getElementById('up_name').value;
    const email = document.getElementById('up_email').value;
    const phone = document.getElementById('up_phone').value;
    const address = document.getElementById('up_address').value;
    const newPin = document.getElementById('up_pin').value;
    const res = await apiCall('/api/update', { accountNo: accNo, pin: state.sessionPin, name, email, phone, address, newPin });"""
content = content.replace(old_up_submit, new_up_submit)


# 5. Update Overview Tab Profile Information
old_overview = """                  <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center font-bold">
                      ${initial}
                    </div>
                    <div>
                      <h3 class="font-bold text-slate-800">${esc(user.name)}</h3>
                      <p class="text-xs text-slate-500">${esc(user.email)} &bull; Age: ${user.age}</p>
                    </div>
                  </div>"""

new_overview = """                  <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center font-bold">
                      ${initial}
                    </div>
                    <div>
                      <h3 class="font-bold text-slate-800">${esc(user.name)} <span class="ml-2 px-2 py-0.5 rounded text-[10px] bg-indigo-100 text-indigo-700 font-bold uppercase tracking-widest">${esc(user.acc_type || 'Savings')}</span></h3>
                      <p class="text-xs text-slate-500 mt-1"><i class="fas fa-envelope mr-1"></i> ${esc(user.email)} &bull; <i class="fas fa-phone mr-1 ml-1"></i> ${esc(user.phone || 'N/A')}</p>
                      <p class="text-xs text-slate-500 mt-1"><i class="fas fa-map-marker-alt mr-1"></i> ${esc(user.address || 'Address not provided')}</p>
                    </div>
                  </div>"""
content = content.replace(old_overview, new_overview)

# 6. Add Landing Page Content
landing_replace_target = """        <div class="mt-8 pt-8 border-t border-slate-100 flex items-center justify-between">
          <div class="flex items-center gap-2 text-sm font-semibold text-slate-700">
            <i class="fas fa-shield-alt text-emerald-500"></i> Bank-grade Security
          </div>
          <div class="flex gap-1">
            <div class="w-2 h-2 rounded-full bg-slate-300"></div>
            <div class="w-2 h-2 rounded-full bg-blue-600"></div>
            <div class="w-2 h-2 rounded-full bg-slate-300"></div>
          </div>
        </div>
      </div>
    </div>
  `;
}"""

new_landing_content = """        <div class="mt-8 pt-8 border-t border-slate-100 flex items-center justify-between">
          <div class="flex items-center gap-2 text-sm font-semibold text-slate-700">
            <i class="fas fa-shield-alt text-emerald-500"></i> Bank-grade Security
          </div>
          <div class="flex gap-1">
            <div class="w-2 h-2 rounded-full bg-slate-300"></div>
            <div class="w-2 h-2 rounded-full bg-blue-600"></div>
            <div class="w-2 h-2 rounded-full bg-slate-300"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Additional Website Content -->
    <section class="py-24 bg-white px-8">
      <div class="max-w-6xl mx-auto text-center">
        <h2 class="text-3xl font-bold text-slate-900 mb-4">Why Choose VaultX?</h2>
        <p class="text-slate-500 max-w-2xl mx-auto mb-16">Experience the next generation of financial management with tools built for speed, security, and simplicity.</p>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="p-6 rounded-2xl bg-slate-50 border border-slate-100 hover:shadow-lg transition-all text-left">
            <div class="w-12 h-12 bg-blue-100 text-blue-600 rounded-xl flex items-center justify-center text-xl mb-4"><i class="fas fa-bolt"></i></div>
            <h3 class="font-bold text-lg mb-2 text-slate-800">Lightning Fast Transfers</h3>
            <p class="text-sm text-slate-600">Send and receive money instantly across the globe with zero hidden fees.</p>
          </div>
          <div class="p-6 rounded-2xl bg-slate-50 border border-slate-100 hover:shadow-lg transition-all text-left">
            <div class="w-12 h-12 bg-emerald-100 text-emerald-600 rounded-xl flex items-center justify-center text-xl mb-4"><i class="fas fa-lock"></i></div>
            <h3 class="font-bold text-lg mb-2 text-slate-800">Military-Grade Security</h3>
            <p class="text-sm text-slate-600">Your funds are protected by industry-leading encryption and biometric authentication.</p>
          </div>
          <div class="p-6 rounded-2xl bg-slate-50 border border-slate-100 hover:shadow-lg transition-all text-left">
            <div class="w-12 h-12 bg-indigo-100 text-indigo-600 rounded-xl flex items-center justify-center text-xl mb-4"><i class="fas fa-robot"></i></div>
            <h3 class="font-bold text-lg mb-2 text-slate-800">24/7 AI Support</h3>
            <p class="text-sm text-slate-600">Got a question? Our Gemini-powered AI Assistant is always here to help you.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-slate-900 py-12 px-8 text-slate-400">
      <div class="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
        <div class="col-span-2">
          <h2 class="text-xl font-bold text-white flex items-center gap-2 mb-4"><i class="fas fa-university text-blue-500"></i> VaultX Bank</h2>
          <p class="text-sm max-w-sm">The modern financial solution designed to give you complete control over your money, without the complexity of traditional banking.</p>
        </div>
        <div>
          <h4 class="text-white font-bold mb-4">Quick Links</h4>
          <ul class="space-y-2 text-sm">
            <li><a href="#" class="hover:text-blue-400">Personal Banking</a></li>
            <li><a href="#" class="hover:text-blue-400">Business Accounts</a></li>
            <li><a href="#" class="hover:text-blue-400">Investment</a></li>
          </ul>
        </div>
        <div>
          <h4 class="text-white font-bold mb-4">Legal</h4>
          <ul class="space-y-2 text-sm">
            <li><a href="#" class="hover:text-blue-400">Privacy Policy</a></li>
            <li><a href="#" class="hover:text-blue-400">Terms of Service</a></li>
            <li><a href="#" class="hover:text-blue-400">Security</a></li>
          </ul>
        </div>
      </div>
      <div class="max-w-6xl mx-auto pt-8 border-t border-slate-800 text-sm text-center">
        &copy; 2026 VaultX Bank Manager. All rights reserved.
      </div>
    </footer>
  `;
}"""
content = content.replace(landing_replace_target, new_landing_content)


with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
