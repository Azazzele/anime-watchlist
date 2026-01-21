const API_URL = "http://localhost:8000/api";

export async function searchAnime(search) {
  const response = await fetch(
    `${API_URL}/anime?search=${encodeURIComponent(search)}`
  );

  if (!response.ok) {
    throw new Error("Ошибка запроса");
  }

  return response.json();
}
