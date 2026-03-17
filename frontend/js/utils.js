function formatBRL(value) {
  return Number(value || 0).toLocaleString('pt-BR', {
    style: 'currency', currency: 'BRL'
  });
}

function formatDate(str) {
  if (!str) return '—';
  const d = new Date(str.replace(' ', 'T'));
  return d.toLocaleDateString('pt-BR', {
    day: '2-digit', month: '2-digit', year: 'numeric'
  });
}

function getParams() {
  return Object.fromEntries(new URLSearchParams(window.location.search).entries());
}

function toast(msg, type = 'success') {
  const container = document.getElementById('toast');
  if (!container) return;
  const el = document.createElement('div');
  el.className = `toast-msg ${type}`;
  el.textContent = msg;
  container.appendChild(el);
  setTimeout(() => el.remove(), 3500);
}

function setActiveNav(page) {
  document.querySelectorAll('.nav-link').forEach(a => {
    a.classList.toggle('active', a.dataset.page === page);
  });
}

function badgeHtml(status) {
  const map = {
    rascunho: 'badge-rascunho',
    enviada:  'badge-enviada',
    aprovada: 'badge-aprovada',
    recusada: 'badge-recusada',
  };
  const labels = {
    rascunho: 'Rascunho',
    enviada:  'Enviada',
    aprovada: 'Aprovada',
    recusada: 'Recusada',
  };
  return `<span class="badge ${map[status] || ''}">${labels[status] || status}</span>`;
}

function statusOptions(selected) {
  const opts = ['rascunho','enviada','aprovada','recusada'];
  return opts.map(s =>
    `<option value="${s}" ${s === selected ? 'selected' : ''}>${s.charAt(0).toUpperCase()+s.slice(1)}</option>`
  ).join('');
}

function confirmDialog(msg) {
  return window.confirm(msg);
}
