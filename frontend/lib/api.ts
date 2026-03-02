import type { University } from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000/api/v1";

export async function fetchRegions(): Promise<string[]> {
  const response = await fetch(`${API_BASE}/regions`, { next: { revalidate: 3600 } });
  const data = await response.json();
  return data.items;
}

export async function fetchUniversitiesByCountry(
  region: string,
  country: string
): Promise<University[]> {
  const response = await fetch(
    `${API_BASE}/regions/${encodeURIComponent(region)}/countries/${encodeURIComponent(country)}/universities`,
    { next: { revalidate: 3600 } }
  );
  const data = await response.json();
  return data.items;
}
