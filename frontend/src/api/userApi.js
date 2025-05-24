const API_URL = "http://127.0.0.1:8000"; 


export const createUser = async (userData) => {
  try {
    const response = await fetch(`${API_URL}/users`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(userData),
    });

    if (!response.ok) {
      throw new Error("Nie udało się utworzyć użytkownika.");
    }

    return await response.json();
  } catch (error) {
    console.error("Błąd podczas tworzenia użytkownika:", error);
    throw error;
  }
};


export const getUsers = async () => {
  try {
    const response = await fetch(`${API_URL}/users`, {
      method: "GET",
    });

    if (!response.ok) {
      throw new Error("Nie udało się pobrać listy użytkowników.");
    }

    return await response.json();
  } catch (error) {
    console.error("Błąd podczas pobierania użytkowników:", error);
    throw error;
  }
};