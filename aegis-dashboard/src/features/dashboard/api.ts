import { apiClient } from "@/lib/api";
import type { StatSchema, DashboardPeriod } from "@/types/api";

export interface StatsQuery {
  period: DashboardPeriod;
  month?: number;
  year?: number;
  from_date?: string;
  to_date?: string;
}

export const dashboardApi = {
  getStats: (query: StatsQuery) =>
    apiClient.get<StatSchema>("/dashboard/stats", {
      period: query.period,
      month: query.month,
      year: query.year,
      from_date: query.from_date,
      to_date: query.to_date,
    }),
};
