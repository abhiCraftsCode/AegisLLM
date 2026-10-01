export const API_BASE_URL: string =
  (import.meta.env.VITE_API_BASE_URL as string | undefined) ?? "http://localhost:8000";

export const ACCESS_TOKEN_KEY = "aegis_access_token";
export const REFRESH_TOKEN_KEY = "aegis_refresh_token";
export const THEME_KEY = "aegis_theme";

export const DEFAULT_PAGE_SIZE = 10;

export const GOOGLE_CLIENT_ID: string = (import.meta.env.VITE_GOOGLE_CLIENT_ID as string | undefined) ?? "";
export const GITHUB_CLIENT_ID: string = (import.meta.env.VITE_GITHUB_CLIENT_ID as string | undefined) ?? "";
export const OAUTH_REDIRECT_URI: string =
  (import.meta.env.VITE_OAUTH_REDIRECT_URI as string | undefined) ??
  `${window.location.origin}/oauth/callback`;
