/**
 * nav.js — Injects the shared navbar and AI chat widget into every page.
 * Import this at the bottom of every HTML page's <script type=module> block.
 */
import { Auth, logout } from './api.js';

export function renderNav() {
    const username   = Auth.getUsername();
    const isLoggedIn = Auth.isLoggedIn();

    const authLinks = isLoggedIn
        ? `<span style="color:var(--text-muted); margin-left:1.5rem">👤 ${username}</span>
           <button class="nav-logout-btn" style="background:none;border:none;color:var(--text-muted);cursor:pointer;font-size:1rem;margin-left:1.5rem">Logout</button>`
        : `<a href="/auth/login.html" style="color:var(--accent);margin-left:1.5rem">Login</a>
           <a href="/auth/signup.html" class="btn-primary" style="padding:0.4rem 1rem;margin-left:1.5rem">Sign Up</a>`;

    document.body.insertAdjacentHTML('afterbegin', `
    <nav class="navbar">
      <div class="nav-container">
        <div class="logo-group">
          <a href="/index.html" class="logo">FinPlatform.</a>
          <span class="dev-badge">(in development)</span>
        </div>
        <div class="nav-links">
          <a href="/charts.html">Charts</a>
          <a href="/calendar.html">Calendar</a>
          <a href="/forum/list.html">Forum</a>
          ${authLinks}
        </div>
      </div>
    </nav>`);

    document.querySelector('.nav-logout-btn')?.addEventListener('click', async () => {
        try { await logout({ refresh: Auth.getRefresh() }); } catch (_) {}
        Auth.clear();
        window.location.href = '/index.html';
    });
}

export function renderAIChat() {
    document.body.insertAdjacentHTML('beforeend', `
    <button id="ai-toggle-btn" class="ai-float-btn">🤖 Ask AI</button>
    <div id="ai-chat-modal" class="chat-modal hidden">
      <div class="chat-header">
        <h4>Market AI Assistant</h4>
        <button id="close-chat">✕</button>
      </div>
      <div class="chat-body" id="chat-body">
        <div class="message bot">Hello! I can explain recent market movements based on live news data. What asset are you looking at? (Note: I do not predict prices).</div>
      </div>
      <div class="chat-footer">
        <input type="text" id="chat-input" placeholder="Why did market prices move this week?" />
        <button id="send-btn">Send</button>
      </div>
    </div>
    <script src="/js/chat.js"></script>`);
}
