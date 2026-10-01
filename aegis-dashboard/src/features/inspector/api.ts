import { apiClient } from "@/lib/api";
import type { InspectRequest, InspectResponse } from "@/types/api";

/**
 * IMPORTANT: /chat/inspections authenticates via get_current_api_key (an
 * API key secret, hashed and compared server-side) — not the dashboard
 * session JWT used by every other endpoint in this app. The caller must
 * supply a raw API key secret as the bearer token.
 */
export const inspectorApi = {
  inspect: (data: InspectRequest, keySecret: string) =>
    apiClient.post<InspectResponse>("/chat/inspect", data, {
      auth: false,
      bearerOverride: keySecret,
    }),
};
