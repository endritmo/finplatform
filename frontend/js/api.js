/**
 * api.js — Centralised fetch wrapper for the FinPlatform REST API.
 * All frontend pages import functions from here; no page hard-codes /api/ URLs.
 */

const API_BASE = '';   // Nginx proxies /api/ and /ai/ to the backend — no port needed.

// ── Token helpers ──────────────────────────────────────────────────────────────
export const Auth = {
    getAccess:  ()    => localStorage.getItem('access_token'),
    getRefresh: ()    => localStorage.getItem('refresh_token'),
    getUsername:()    => localStorage.getItem('username'),
    isLoggedIn: ()    => !!localStorage.getItem('access_token'),
    save: (data)      => {
        localStorage.setItem('access_token',  data.access);
        localStorage.setItem('refresh_token', data.refresh);
        localStorage.setItem('username',      data.username);
    },
    clear: ()         => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('username');
    },
};

// ── Core fetch ─────────────────────────────────────────────────────────────────
async function apiFetch(path, options = {}) {
    const headers = { 'Content-Type': 'application/json', ...options.headers };
    if (Auth.isLoggedIn()) {
        headers['Authorization'] = `Bearer ${Auth.getAccess()}`;
    }
    const resp = await fetch(API_BASE + path, { ...options, headers });
    if (!resp.ok) {
        const err = await resp.json().catch(() => ({ error: resp.statusText }));
        throw new Error(err.error || err.detail || `HTTP ${resp.status}`);
    }
    return resp.json();
}

// ── Auth API ───────────────────────────────────────────────────────────────────
export const signup  = (d) => apiFetch('/api/signup/',  { method: 'POST', body: JSON.stringify(d) });
export const login   = (d) => apiFetch('/api/login/',   { method: 'POST', body: JSON.stringify(d) });
export const logout  = (d) => apiFetch('/api/logout/',  { method: 'POST', body: JSON.stringify(d) });
export const getMe   = ()  => apiFetch('/api/me/');

// ── Data API ───────────────────────────────────────────────────────────────────
export const getSymbols       = ()   => apiFetch('/api/symbols/');
export const getCalendarEvents= ()   => apiFetch('/api/calendar/');

// ── Forum API ──────────────────────────────────────────────────────────────────
export const getThreads     = (q='') => apiFetch(`/api/forum/threads/${q}`);
export const createThread   = (d)    => apiFetch('/api/forum/threads/create/', { method: 'POST', body: JSON.stringify(d) });
export const getThread      = (pk)   => apiFetch(`/api/forum/threads/${pk}/`);
export const editThread     = (pk,d) => apiFetch(`/api/forum/threads/${pk}/edit/`, { method: 'PUT', body: JSON.stringify(d) });
export const createReply    = (tpk,d)=> apiFetch(`/api/forum/threads/${tpk}/replies/`, { method: 'POST', body: JSON.stringify(d) });
export const editReply      = (pk,d) => apiFetch(`/api/forum/replies/${pk}/edit/`, { method: 'PUT', body: JSON.stringify(d) });
export const deleteReply    = (pk)   => apiFetch(`/api/forum/replies/${pk}/delete/`, { method: 'DELETE' });

// ── AI API ─────────────────────────────────────────────────────────────────────
export const askAI = (message) => apiFetch('/ai/ask/', { method: 'POST', body: JSON.stringify({ message }) });
