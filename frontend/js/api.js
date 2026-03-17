const API_BASE = '/api';

async function apiFetch(path, options = {}) {
  const defaults = {
    headers: { 'Content-Type': 'application/json' },
  };
  const opts = { ...defaults, ...options };
  if (opts.body && typeof opts.body === 'object') {
    opts.body = JSON.stringify(opts.body);
  }
  
  const res = await fetch(`${API_BASE}${path}`, opts);
  
  // Verifica se a resposta é JSON antes de tentar parsear
  const contentType = res.headers.get("content-type");
  let data;
  
  if (contentType && contentType.indexOf("application/json") !== -1) {
    data = await res.json();
  } else {
    // Se não for JSON, lê como texto para debug
    const text = await res.text();
    console.error('Resposta não-JSON recebida:', text);
    throw new Error(`Erro no servidor (${res.status}). A resposta não é um JSON válido.`);
  }

  if (!res.ok) {
    throw new Error(data.erro || `Erro ${res.status}`);
  }
  return data;
}

const API = {
  // Propostas
  listarPropostas:    ()         => apiFetch('/propostas'),
  buscarProposta:     (id)       => apiFetch(`/propostas/${id}`),
  criarProposta:      (body)     => apiFetch('/propostas', { method: 'POST', body }),
  editarProposta:     (id, body) => apiFetch(`/propostas/${id}`, { method: 'PUT', body }),
  duplicarProposta:   (id)       => apiFetch(`/propostas/${id}/duplicar`, { method: 'POST' }),

  // Serviços
  listarServicos:     ()         => apiFetch('/servicos'),
  criarServico:       (body)     => apiFetch('/servicos', { method: 'POST', body }),
  editarServico:      (id, body) => apiFetch(`/servicos/${id}`, { method: 'PUT', body }),
  excluirServico:     (id)       => apiFetch(`/servicos/${id}`, { method: 'DELETE' }),

  // Clientes
  listarClientes:     ()         => apiFetch('/clientes'),
  criarCliente:       (body)     => apiFetch('/clientes', { method: 'POST', body }),
  editarCliente:      (id, body) => apiFetch(`/clientes/${id}`, { method: 'PUT', body }),

  // Configurações
  buscarConfig:       ()         => apiFetch('/configuracoes'),
  salvarConfig:       (body)     => apiFetch('/configuracoes', { method: 'PUT', body }),
};
