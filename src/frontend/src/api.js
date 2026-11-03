const BASE_URL = '';

async function request(path, options = {}) {
  const response = await fetch(`${BASE_URL}${path}`, {
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  });

  if (!response.ok) {
    let errorDetail = `Request failed with status ${response.status}`;
    try {
      const data = await response.json();
      if (data && data.detail) {
        errorDetail = data.detail;
      }
    } catch {
      // Non-JSON response
    }
    const error = new Error(errorDetail);
    error.status = response.status;
    throw error;
  }

  return response.json();
}

export async function fetchAvailableNames() {
  return request('/api/session/names');
}

export async function fetchSession() {
  return request('/api/session');
}

export async function login(name) {
  return request('/api/session', {
    method: 'POST',
    body: JSON.stringify({ name }),
  });
}

export async function logout() {
  return request('/api/session', {
    method: 'DELETE',
  });
}

export async function fetchGroups() {
  return request('/api/groups');
}

export async function fetchGroup(id) {
  return request(`/api/groups/${id}`);
}

export async function fetchGroupBalances(id) {
  return request(`/api/groups/${id}/balances`);
}

export async function sendChatMessage({ groupId, conversationId, message }) {
  return request('/api/chat', {
    method: 'POST',
    body: JSON.stringify({
      groupId,
      conversationId,
      message,
    }),
  });
}

export async function fetchConversation(conversationId) {
  return request(`/api/conversations/${conversationId}`);
}

export async function confirmExpense(conversationId) {
  return request(`/api/conversations/${conversationId}/confirm`, {
    method: 'POST',
  });
}


export async function fetchGroupExpenses(id) {
  return request(`/api/groups/${id}/expenses`);
}

// amount is sent as the typed string so the server parses exact cents.
export async function createManualExpense(groupId, { description, amount, paidBy, splitBetween }) {
  return request(`/api/groups/${groupId}/expenses/manual`, {
    method: 'POST',
    body: JSON.stringify({ description, amount, paidBy, splitBetween }),
  });
}
