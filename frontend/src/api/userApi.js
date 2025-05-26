const BASE_URL = '/api/users';
const AUTH_URL = '/api/auth';

// ✅ CREATE - dodaj użytkownika
export async function createUser(user) {
  const res = await fetch(BASE_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(user),
  });

  if (!res.ok) {
    throw new Error('Błąd dodawania użytkownika');
  }

  return await res.json();
}

// ✅ READ - pobierz użytkowników
export async function getUsers() {
  const res = await fetch(BASE_URL);

  if (!res.ok) {
    throw new Error('Błąd pobierania użytkowników');
  }

  return await res.json();
}

// ✅ UPDATE - aktualizuj użytkownika
export async function updateUser(id, updatedUser) {
  const res = await fetch(`${BASE_URL}/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(updatedUser),
  });

  if (!res.ok) {
    throw new Error('Błąd aktualizacji użytkownika');
  }

  return await res.json();
}

// ✅ DELETE - usuń użytkownika
export async function deleteUser(id) {
  const res = await fetch(`${BASE_URL}/${id}`, {
    method: 'DELETE',
  });

  if (!res.ok) {
    throw new Error('Błąd usuwania użytkownika');
  }

  return await res.json();
}

//logowanie
export async function loginUser(email, password) {
  const res = await fetch(`${AUTH_URL}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: email, password }),
  });

  if (!res.ok) {
    throw new Error('Błąd logowania');
  }

  return await res.json();
}

// token refresh
export async function refreshToken(refreshToken) {
  const res = await fetch(`${AUTH_URL}/refresh`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh_token: refreshToken }),
  });

  if (!res.ok) {
    throw new Error('Błąd odświeżania tokena');
  }

  return await res.json();
}

// wylogowywanie
export async function logoutUser(token) {
  const res = await fetch(`${AUTH_URL}/logout`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
  });

  if (!res.ok) {
    throw new Error('Błąd wylogowania');
  }

  return await res.json();
}

//liczba kilometrów
export async function getTotalKilometers(token) {
  const res = await fetch('/api/rides/total', {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!res.ok) {
    throw new Error('Błąd pobierania kilometrów');
  }

  return await res.json();
}

//start trasy
export async function startRide(token) {
  const res = await fetch('/api/start_trip', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });

  if (!res.ok) {
    throw new Error('Błąd rozpoczęcia trasy');
  }

  return await res.json();
}