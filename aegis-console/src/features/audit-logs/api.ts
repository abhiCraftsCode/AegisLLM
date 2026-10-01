import { apiClient } from "@/lib/api";
import type { LogSchema, PageResponse } from "@/types/api";

export const auditLogsApi = {
  list: (page: number, size: number) =>
    apiClient.get<PageResponse<LogSchema>>("/audit-logs/all", { page, size }),
  get: (logId: number) => apiClient.get<LogSchema>(`/audit-logs/${logId}`),
};
