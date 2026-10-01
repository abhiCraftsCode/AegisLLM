import { apiClient } from "@/lib/api";
import type { GenerateSchema, GenerateResponse, KeySchema, PageResponse, UpstreamConfig } from "@/types/api";

export const apiKeysApi = {
  list: (page: number, size: number) =>
    apiClient.get<PageResponse<KeySchema>>("/api-keys/all", { page, size }),

  get: (keyId: number) => apiClient.get<KeySchema>(`/api-keys/${keyId}`),

  generate: (data: GenerateSchema) => apiClient.post<GenerateResponse>("/api-keys/generate", data),

  update: (keyId: number, data: UpstreamConfig) =>
    apiClient.patch<KeySchema>(`/api-keys/${keyId}/update`, data),

  deactivate: (keyId: number) => apiClient.delete<void>(`/api-keys/${keyId}/deactivate`),
};
