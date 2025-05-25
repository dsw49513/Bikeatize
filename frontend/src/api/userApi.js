const BASE_URL = '/api/users';

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
