/**
 * Types below mirror the backend Pydantic schemas exactly (allschemas.txt).
 * Do not add fields the backend does not return; do not remove fields it does.
 */

export interface ProfileSchema {
  id: number;
  name: string;
  email: string | null;
  phone: string | null;
  oauth_provider: string | null;
  is_active: boolean;
  created_at: string;
}

export interface TokenSchema {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface AuthResponse {
  user: ProfileSchema;
  tokens: TokenSchema;
}

export interface LoginSchema {
  identifier: string;
  password: string;
}

export interface RegisterSchema {
  name: string;
  email?: string | null;
  phone?: string | null;
  password: string;
}

export interface ForgotSchema {
  email: string;
}

export type OAuthProvider = "google" | "github";

export interface OauthLoginSchema {
  provider: OAuthProvider;
  code: string;
}

export interface ResetSchema {
  new_password: string;
  token: string;
}

export interface UpdateSchema {
  name?: string | null;
  email?: string | null;
  phone?: string | null;
}

export interface PasswordSchema {
  new_password: string;
  curr_password?: string | null;
}

// ---- Dashboard ----

export interface DaySchema {
  date: string;
  total_requests: number;
  blocked_requests: number;
}

export interface WeekSchema {
  week: number;
  start_date: string;
  end_date: string;
  days: DaySchema[];
}

export interface StatSchema {
  total_requests: number;
  allowed_requests: number;
  blocked_requests: number;
  block_rate: number;
  avg_latency_ms: number;
  avg_threat_score: number;
  highest_threat_score: number;
  total_keys: number;
  active_keys: number;
  activity: WeekSchema[];
}

export type DashboardPeriod = "lifetime" | "monthly" | "range";

// ---- Gateway / Inspector ----

export interface InspectRequest {
  prompt: string;
}

export interface InspectResponse {
  request_id: string;
  is_blocked: boolean;
  threat_score: number;
  reason: string;
  latency_ms: number;
}

// ---- API Keys ----

export interface KeySchema {
  id: number;
  user_id: number;
  name: string | null;
  prefix: string;
  is_active: boolean;
  last_used_at: string | null;
  created_at: string;
  llm_name: string | null;
  llm_url: string | null;
}

export interface GenerateSchema {
  name?: string | null;
  llm_name?: string | null;
  llm_auth?: string | null;
  llm_url?: string | null;
}

export interface UpstreamConfig {
  llm_name?: string | null;
  llm_url?: string | null;
  llm_auth?: string | null;
}

export interface GenerateResponse {
  key: KeySchema;
  secret: string;
}

export interface PageResponse<T> {
  items: T[];
  page: number;
  size: number;
  total: number;
  pages: number;
}

// ---- Audit Logs ----

export interface LogSchema {
  id: number;
  request_id: string;
  key_id: number | null;
  threat_score: number;
  is_blocked: boolean;
  reason: string | null;
  latency_ms: number;
  created_at: string;
  llm_name: string | null;
  llm_url: string | null;
}
