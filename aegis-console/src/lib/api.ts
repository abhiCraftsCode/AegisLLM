import { API_BASE_URL, ACCESS_TOKEN_KEY } from "./constants";

export class ApiError extends Error {
  status: number;
  detail: unknown;

  constructor(status: number, message: string, detail?: unknown) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.detail = detail;
  }
}

/**
 * Dispatched whenever the API client receives a 401 Unauthorized response.
 * AuthContext listens for this to clear session state without creating a
 * circular import between lib/api.ts and features/auth.
 */
export const UNAUTHORIZED_EVENT = "aegis:unauthorized";

function getToken(): string | null {
  return localStorage.getItem(ACCESS_TOKEN_KEY);
}

function extractMessage(body: unknown, fallback: string): string {
  if (body && typeof body === "object") {
    const anyBody = body as Record<string, unknown>;
    if (typeof anyBody.detail === "string") return anyBody.detail;
    if (Array.isArray(anyBody.detail) && anyBody.detail.length > 0) {
      const first = anyBody.detail[0];
      if (first && typeof first === "object" && "msg" in first) {
        return String((first as Record<string, unknown>).msg);
      }
    }
  }
  return fallback;
}

interface RequestOptions {
  method?: "GET" | "POST" | "PATCH" | "PUT" | "DELETE";
  body?: unknown;
  query?: Record<string, string | number | boolean | undefined | null>;
  auth?: boolean;
  /** Use a raw bearer token instead of the stored session token (e.g. an API key secret). */
  bearerOverride?: string;
}

function buildUrl(path: string, query?: RequestOptions["query"]): string {
  const url = new URL(path.replace(/^\//, ""), API_BASE_URL + "/");
  if (query) {
    Object.entries(query).forEach(([k, v]) => {
      if (v !== undefined && v !== null) url.searchParams.set(k, String(v));
    });
  }
  return url.toString();
}

async function request<T>(
  path: string,
  options: RequestOptions = {},
): Promise<T> {
  const { method = "GET", body, query, auth = true, bearerOverride } = options;

  const headers: Record<string, string> = {};
  if (body !== undefined) headers["Content-Type"] = "application/json";

  if (bearerOverride) {
    headers["Authorization"] = `Bearer ${bearerOverride}`;
  } else if (auth) {
    const token = getToken();
    if (token) headers["Authorization"] = `Bearer ${token}`;
  }

  let response: Response;
  try {
    response = await fetch(buildUrl(path, query), {
      method,
      headers,
      body: body !== undefined ? JSON.stringify(body) : undefined,
    });
  } catch {
    throw new ApiError(
      0,
      "Network error. Check your connection and try again.",
    );
  }

  if (response.status === 204) {
    return undefined as T;
  }

  let parsed: unknown = null;
  const text = await response.text();
  if (text) {
    try {
      parsed = JSON.parse(text);
    } catch {
      parsed = null;
    }
  }

  if (!response.ok) {
    if (response.status === 401) {
      window.dispatchEvent(new CustomEvent(UNAUTHORIZED_EVENT));
    }
    const message = extractMessage(
      parsed,
      `Request failed (${response.status})`,
    );
    throw new ApiError(response.status, message, parsed);
  }

  return parsed as T;
}

export const apiClient = {
  get: <T>(
    path: string,
    query?: RequestOptions["query"],
    options?: Omit<RequestOptions, "method" | "query">,
  ) => request<T>(path, { ...options, method: "GET", query }),
  post: <T>(
    path: string,
    body?: unknown,
    options?: Omit<RequestOptions, "method" | "body">,
  ) => request<T>(path, { ...options, method: "POST", body }),
  patch: <T>(
    path: string,
    body?: unknown,
    options?: Omit<RequestOptions, "method" | "body">,
  ) => request<T>(path, { ...options, method: "PATCH", body }),
  put: <T>(
    path: string,
    body?: unknown,
    options?: Omit<RequestOptions, "method" | "body">,
  ) => request<T>(path, { ...options, method: "PUT", body }),
  delete: <T>(path: string, options?: Omit<RequestOptions, "method">) =>
    request<T>(path, { ...options, method: "DELETE" }),
};
