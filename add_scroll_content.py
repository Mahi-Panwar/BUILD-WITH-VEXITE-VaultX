import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

more_sections = """
    <!-- Statistics Section -->
    <section class="py-16 bg-blue-600 text-white px-8">
      <div class="max-w-6xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
        <div>
          <div class="text-4xl font-bold mb-2">2M+</div>
          <div class="text-blue-200 text-sm font-medium uppercase tracking-wider">Active Users</div>
        </div>
        <div>
          <div class="text-4xl font-bold mb-2">$5B+</div>
          <div class="text-blue-200 text-sm font-medium uppercase tracking-wider">Transactions Processed</div>
        </div>
        <div>
          <div class="text-4xl font-bold mb-2">99.9%</div>
          <div class="text-blue-200 text-sm font-medium uppercase tracking-wider">Uptime Reliability</div>
        </div>
        <div>
          <div class="text-4xl font-bold mb-2">24/7</div>
          <div class="text-blue-200 text-sm font-medium uppercase tracking-wider">Customer Support</div>
        </div>
      </div>
    </section>

    <!-- Services Section -->
    <section class="py-24 bg-slate-50 px-8">
      <div class="max-w-6xl mx-auto">
        <div class="text-center mb-16">
          <h2 class="text-3xl font-bold text-slate-900 mb-4">Comprehensive Banking Services</h2>
          <p class="text-slate-500 max-w-2xl mx-auto">From personal checking accounts to complex corporate treasury solutions, VaultX has the tools you need to succeed.</p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <!-- Service 1 -->
          <div class="bg-white p-8 rounded-3xl border border-slate-200 hover:shadow-xl hover:-translate-y-1 transition-all">
            <div class="w-14 h-14 bg-indigo-50 text-indigo-600 rounded-2xl flex items-center justify-center text-2xl mb-6"><i class="fas fa-wallet"></i></div>
            <h3 class="text-xl font-bold text-slate-800 mb-3">Checking & Savings</h3>
            <p class="text-slate-600 text-sm mb-4">High-yield savings and zero-fee checking accounts designed for your daily needs.</p>
            <a href="#" class="text-indigo-600 font-bold text-sm hover:underline flex items-center gap-2">Learn More <i class="fas fa-arrow-right"></i></a>
          </div>
          <!-- Service 2 -->
          <div class="bg-white p-8 rounded-3xl border border-slate-200 hover:shadow-xl hover:-translate-y-1 transition-all">
            <div class="w-14 h-14 bg-emerald-50 text-emerald-600 rounded-2xl flex items-center justify-center text-2xl mb-6"><i class="fas fa-chart-line"></i></div>
            <h3 class="text-xl font-bold text-slate-800 mb-3">Investment Portfolios</h3>
            <p class="text-slate-600 text-sm mb-4">Automated wealth management with AI-driven insights to grow your net worth.</p>
            <a href="#" class="text-emerald-600 font-bold text-sm hover:underline flex items-center gap-2">Learn More <i class="fas fa-arrow-right"></i></a>
          </div>
          <!-- Service 3 -->
          <div class="bg-white p-8 rounded-3xl border border-slate-200 hover:shadow-xl hover:-translate-y-1 transition-all">
            <div class="w-14 h-14 bg-orange-50 text-orange-600 rounded-2xl flex items-center justify-center text-2xl mb-6"><i class="fas fa-credit-card"></i></div>
            <h3 class="text-xl font-bold text-slate-800 mb-3">Credit Cards</h3>
            <p class="text-slate-600 text-sm mb-4">Premium rewards, zero foreign transaction fees, and exclusive lounge access.</p>
            <a href="#" class="text-orange-600 font-bold text-sm hover:underline flex items-center gap-2">Learn More <i class="fas fa-arrow-right"></i></a>
          </div>
        </div>
      </div>
    </section>

    <!-- Testimonials Section -->
    <section class="py-24 bg-white px-8">
      <div class="max-w-6xl mx-auto">
        <h2 class="text-3xl font-bold text-slate-900 mb-12 text-center">Trusted by Thousands</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="bg-slate-50 p-8 rounded-2xl border border-slate-100">
            <div class="flex text-yellow-400 mb-4 gap-1">
              <i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i>
            </div>
            <p class="text-slate-600 italic mb-6">"VaultX completely transformed how I manage my business finances. The AI chat feature is an absolute lifesaver!"</p>
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-full bg-slate-200 bg-[url('https://i.pravatar.cc/100?img=1')] bg-cover"></div>
              <div>
                <h4 class="font-bold text-slate-800 text-sm">Sarah Jenkins</h4>
                <p class="text-xs text-slate-500">Tech Entrepreneur</p>
              </div>
            </div>
          </div>
          <div class="bg-slate-50 p-8 rounded-2xl border border-slate-100">
            <div class="flex text-yellow-400 mb-4 gap-1">
              <i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i>
            </div>
            <p class="text-slate-600 italic mb-6">"The UI is gorgeous and lightning fast. Making transfers has never been easier. I recommend it to all my friends."</p>
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-full bg-slate-200 bg-[url('https://i.pravatar.cc/100?img=12')] bg-cover"></div>
              <div>
                <h4 class="font-bold text-slate-800 text-sm">David Chen</h4>
                <p class="text-xs text-slate-500">Freelance Designer</p>
              </div>
            </div>
          </div>
          <div class="bg-slate-50 p-8 rounded-2xl border border-slate-100">
            <div class="flex text-yellow-400 mb-4 gap-1">
              <i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i>
            </div>
            <p class="text-slate-600 italic mb-6">"Finally, a bank that doesn't feel like it's stuck in 1999. The real-time ledger updates are fantastic."</p>
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-full bg-slate-200 bg-[url('https://i.pravatar.cc/100?img=5')] bg-cover"></div>
              <div>
                <h4 class="font-bold text-slate-800 text-sm">Marcus Johnson</h4>
                <p class="text-xs text-slate-500">Software Engineer</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
"""

content = content.replace("    <!-- Footer -->", more_sections)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
