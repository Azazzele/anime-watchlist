const API_URL = "http://localhost:8000";

export async function getCurrentSeason(limit = 12) {
  const res = await fetch(`${API_URL}/season/current?limit=${limit}`);

  if (!res.ok) {
    throw new Error("Ошибка загрузки сезона");
  }

  return res.json();
}
