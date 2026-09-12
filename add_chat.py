import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

chat_widget_html = """
<!-- Chatbot Widget -->
<div id="chat-widget" class="fixed bottom-6 right-6 z-[100] flex flex-col items-end">
  
  <!-- Chat Window -->
  <div id="chat-window" class="hidden w-80 sm:w-96 bg-white rounded-2xl shadow-2xl border border-slate-200 mb-4 overflow-hidden flex-col h-[500px] max-h-[80vh] fade-in">
    <!-- Header -->
    <div class="bg-slate-900 text-white p-4 flex justify-between items-center shrink-0">
      <div class="flex items-center gap-2">
        <div class="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center">
          <i class="fas fa-robot text-sm"></i>
        </div>
        <div>
          <h4 class="font-bold text-sm">VaultX Assistant</h4>
          <p class="text-[10px] text-slate-300">Powered by Gemini AI</p>
        </div>
      </div>
      <button onclick="toggleChat()" class="text-slate-400 hover:text-white transition-colors">
        <i class="fas fa-times"></i>
      </button>
    </div>
    
    <!-- Messages Area -->
    <div id="chat-messages" class="flex-1 p-4 overflow-y-auto bg-slate-50 flex flex-col gap-3 text-sm">
      <div class="flex justify-start">
        <div class="bg-white border border-slate-200 text-slate-800 p-3 rounded-2xl rounded-tl-sm shadow-sm max-w-[85%] leading-relaxed">
          Hello! I am your VaultX AI Assistant. How can I help you today?
        </div>
      </div>
    </div>
    
    <!-- Input Area -->
    <div class="p-3 bg-white border-t border-slate-100 shrink-0">
      <form id="chat-form" class="relative flex items-center">
        <input type="text" id="chat-input" autocomplete="off" placeholder="Ask something..." required class="w-full pl-4 pr-12 py-3 rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all">
        <button type="submit" class="absolute right-2 w-8 h-8 bg-blue-600 text-white rounded-lg flex items-center justify-center hover:bg-blue-700 transition-colors shadow-sm">
          <i class="fas fa-paper-plane text-xs"></i>
        </button>
      </form>
    </div>
  </div>
  
  <!-- Floating Toggle Button -->
  <button id="chat-toggle" onclick="toggleChat()" class="w-14 h-14 bg-slate-900 hover:bg-slate-800 text-white rounded-full flex items-center justify-center shadow-2xl transition-transform hover:scale-110 active:scale-95 group">
    <i class="fas fa-comment-dots text-2xl group-hover:hidden"></i>
    <i class="fas fa-robot text-2xl hidden group-hover:block"></i>
  </button>
</div>

<script>
  function toggleChat() {
    const window = document.getElementById('chat-window');
    if (window.classList.contains('hidden')) {
      window.classList.remove('hidden');
      window.classList.add('flex');
    } else {
      window.classList.add('hidden');
      window.classList.remove('flex');
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    // We bind the chat form on next tick to ensure elements exist
    setTimeout(() => {
      const chatForm = document.getElementById('chat-form');
      if (chatForm) {
        chatForm.onsubmit = async (e) => {
          e.preventDefault();
          const input = document.getElementById('chat-input');
          const msg = input.value.trim();
          if (!msg) return;
          
          input.value = '';
          const messagesArea = document.getElementById('chat-messages');
          
          // Add User Message
          messagesArea.innerHTML += `
            <div class="flex justify-end">
              <div class="bg-blue-600 text-white p-3 rounded-2xl rounded-tr-sm shadow-sm max-w-[85%] leading-relaxed">
                ${msg.replace(/</g, "&lt;").replace(/>/g, "&gt;")}
              </div>
            </div>
          `;
          messagesArea.scrollTop = messagesArea.scrollHeight;
          
          // Add Loading Indicator
          const loadId = 'loading-' + Date.now();
          messagesArea.innerHTML += `
            <div id="${loadId}" class="flex justify-start">
              <div class="bg-white border border-slate-200 text-slate-500 p-3 rounded-2xl rounded-tl-sm shadow-sm flex items-center gap-2">
                <i class="fas fa-circle-notch fa-spin"></i> Thinking...
              </div>
            </div>
          `;
          messagesArea.scrollTop = messagesArea.scrollHeight;
          
          try {
            const url = 'http://127.0.0.1:8000/api/chat';
            const res = await fetch(url, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ message: msg })
            });
            const data = await res.json();
            
            document.getElementById(loadId).remove();
            
            // Add Bot Message
            messagesArea.innerHTML += `
              <div class="flex justify-start">
                <div class="bg-white border border-slate-200 text-slate-800 p-3 rounded-2xl rounded-tl-sm shadow-sm max-w-[85%] leading-relaxed whitespace-pre-wrap">
                  ${data.reply ? data.reply.replace(/</g, "&lt;").replace(/>/g, "&gt;") : "Error connecting to AI."}
                </div>
              </div>
            `;
          } catch(err) {
            document.getElementById(loadId).remove();
            messagesArea.innerHTML += `
              <div class="flex justify-start">
                <div class="bg-rose-50 border border-rose-200 text-rose-700 p-3 rounded-2xl rounded-tl-sm shadow-sm max-w-[85%] leading-relaxed">
                  Network error.
                </div>
              </div>
            `;
          }
          messagesArea.scrollTop = messagesArea.scrollHeight;
        };
      }
    }, 100);
  });
</script>
"""

content = content.replace("</body>", chat_widget_html + "\n</body>")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
