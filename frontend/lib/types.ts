export type RegionSlug = "north-america" | "europe" | "asia-pacific";

export type University = {
  id: number;
  official_name: string;
  english_name?: string | null;
  region: string;
  country: string;
  website: string;
};
