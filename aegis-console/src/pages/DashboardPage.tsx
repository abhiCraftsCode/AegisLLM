import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  Activity,
  ShieldOff,
  Percent,
  KeyRound,
  Gauge,
  TrendingUp,
  AlertOctagon,
  ShieldCheck,
} from "lucide-react";
import { PageHeader } from "@/components/common/PageHeader";
import { EmptyState } from "@/components/common/EmptyState";
import { ErrorState } from "@/components/common/ErrorState";
import { Skeleton } from "@/components/ui/Skeleton";
import { Button } from "@/components/ui/Button";
import { StatCard } from "@/features/dashboard/StatCard";
import { ActivityChart } from "@/features/dashboard/ActivityChart";
import { dashboardApi } from "@/features/dashboard/api";
import type { DashboardPeriod, StatSchema } from "@/types/api";
import { ApiError } from "@/lib/api";
import { cn, formatDate } from "@/lib/utils";

const filterOptions: { value: DashboardPeriod; label: string }[] = [
  { value: "lifetime", label: "Lifetime" },
  { value: "monthly", label: "Month" },
  { value: "range", label: "Range" },
];

export default function DashboardPage() {
  const [period, setPeriod] = useState<DashboardPeriod>("lifetime");
  const [month, setMonth] = useState(new Date().getMonth() + 1);
  const [year, setYear] = useState(new Date().getFullYear());
  const [fromDate, setFromDate] = useState("");
  const [toDate, setToDate] = useState("");

  const [stats, setStats] = useState<StatSchema | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedWeekIdx, setSelectedWeekIdx] = useState(0);

  async function load() {
    setLoading(true);
    setError(null);
    try {
      const data = await dashboardApi.getStats({
        period,
        month: period === "monthly" ? month : undefined,
        year: period === "monthly" ? year : undefined,
        from_date: period === "range" && fromDate ? fromDate : undefined,
        to_date: period === "range" && toDate ? toDate : undefined,
      });
      setStats(data);
      setSelectedWeekIdx(Math.max(0, data.activity.length - 1));
    } catch (err) {
      setError(
        err instanceof ApiError
          ? err.message
          : "Couldn't load dashboard statistics.",
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [period]);

  function applyRangeOrMonth() {
    load();
  }

  const selectedWeek = stats?.activity[selectedWeekIdx];

  return (
    <div>
      <PageHeader
        title="Dashboard"
        description="Monitor your LLM security activity."
        actions={
          <div className="flex items-center gap-1 rounded-lg border border-aegis-border bg-aegis-surface/60 p-1">
            {filterOptions.map((opt) => (
              <button
                key={opt.value}
                onClick={() => setPeriod(opt.value)}
                className={cn(
                  "rounded-md px-3 py-1.5 text-xs font-medium transition-colors",
                  period === opt.value
                    ? "bg-aegis-cyanSoft text-aegis-cyan"
                    : "text-aegis-textMuted hover:text-aegis-text",
                )}
              >
                {opt.label}
              </button>
            ))}
          </div>
        }
      />

      {period === "monthly" && (
        <div className="mb-6 flex flex-wrap items-end gap-3 rounded-xl border border-aegis-border bg-aegis-surface/40 p-4">
          <div className="flex flex-col gap-1">
            <label className="text-xs font-medium text-aegis-textMuted">
              Month
            </label>
            <select
              value={month}
              onChange={(e) => setMonth(Number(e.target.value))}
              className="h-9 rounded-lg border border-aegis-border bg-aegis-surface2/60 px-2 text-sm text-aegis-text"
            >
              {Array.from({ length: 12 }, (_, i) => i + 1).map((m) => (
                <option key={m} value={m}>
                  {new Date(2000, m - 1, 1).toLocaleString(undefined, {
                    month: "long",
                  })}
                </option>
              ))}
            </select>
          </div>
          <div className="flex flex-col gap-1">
            <label className="text-xs font-medium text-aegis-textMuted">
              Year
            </label>
            <input
              type="number"
              value={year}
              onChange={(e) => setYear(Number(e.target.value))}
              className="h-9 w-24 rounded-lg border border-aegis-border bg-aegis-surface2/60 px-2 text-sm text-aegis-text"
            />
          </div>
          <Button size="sm" onClick={applyRangeOrMonth}>
            Apply
          </Button>
        </div>
      )}

      {period === "range" && (
        <div className="mb-6 flex flex-wrap items-end gap-3 rounded-xl border border-aegis-border bg-aegis-surface/40 p-4">
          <div className="flex flex-col gap-1">
            <label className="text-xs font-medium text-aegis-textMuted">
              From
            </label>
            <input
              type="date"
              value={fromDate}
              onChange={(e) => setFromDate(e.target.value)}
              className="h-9 rounded-lg border border-aegis-border bg-aegis-surface2/60 px-2 text-sm text-aegis-text"
            />
          </div>
          <div className="flex flex-col gap-1">
            <label className="text-xs font-medium text-aegis-textMuted">
              To
            </label>
            <input
              type="date"
              value={toDate}
              onChange={(e) => setToDate(e.target.value)}
              className="h-9 rounded-lg border border-aegis-border bg-aegis-surface2/60 px-2 text-sm text-aegis-text"
            />
          </div>
          <Button
            size="sm"
            onClick={applyRangeOrMonth}
            disabled={!fromDate || !toDate}
          >
            Apply
          </Button>
        </div>
      )}

      {loading && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {Array.from({ length: 4 }).map((_, i) => (
              <Skeleton key={i} className="h-28" />
            ))}
          </div>
          <Skeleton className="h-40" />
          <Skeleton className="h-72" />
        </div>
      )}

      {!loading && error && <ErrorState message={error} onRetry={load} />}

      {!loading && !error && stats && stats.total_requests === 0 && (
        <EmptyState
          title="No activity yet"
          description="Send a prompt through AegisLLM to start building your security activity history."
          action={
            <Link to="/app/inspector">
              <Button size="sm">Open Inspector</Button>
            </Link>
          }
        />
      )}

      {!loading && !error && stats && stats.total_requests > 0 && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-5">
            <StatCard
              label="Total Requests"
              value={stats.total_requests.toLocaleString()}
              icon={<Activity size={16} />}
              tone="default"
            />
            <StatCard
              label="Allowed Requests"
              value={stats.allowed_requests.toLocaleString()}
              icon={<ShieldCheck size={16} />}
              tone="accent"
            />
            <StatCard
              label="Blocked Requests"
              value={stats.blocked_requests.toLocaleString()}
              icon={<ShieldOff size={16} />}
              tone="danger"
            />
            <StatCard
              label="Block Rate"
              value={`${stats.block_rate.toFixed(1)}%`}
              icon={<Percent size={16} />}
            />
            <StatCard
              label="API Keys"
              value={`${stats.active_keys} / ${stats.total_keys}`}
              sub="active / total"
              icon={<KeyRound size={16} />}
            />
          </div>

          <div className="rounded-2xl border border-aegis-border bg-aegis-surface/60 p-5">
            <h3 className="mb-4 text-sm font-semibold text-aegis-text">
              Performance & Threat
            </h3>
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
              <div className="flex items-center gap-3 rounded-xl bg-white/[0.02] p-4">
                <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-aegis-cyanSoft text-aegis-cyan">
                  <Gauge size={16} />
                </span>
                <div>
                  <p className="text-xs text-aegis-textMuted">
                    Average Latency
                  </p>
                  <p className="text-lg font-semibold text-aegis-text">
                    {stats.avg_latency_ms.toFixed(1)} ms
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-3 rounded-xl bg-white/[0.02] p-4">
                <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-aegis-violet/10 text-aegis-violet">
                  <TrendingUp size={16} />
                </span>
                <div>
                  <p className="text-xs text-aegis-textMuted">
                    Average Threat Score
                  </p>
                  <p className="text-lg font-semibold text-aegis-text">
                    {stats.avg_threat_score.toFixed(2)}
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-3 rounded-xl bg-white/[0.02] p-4">
                <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-aegis-coral/10 text-aegis-coral">
                  <AlertOctagon size={16} />
                </span>
                <div>
                  <p className="text-xs text-aegis-textMuted">
                    Highest Threat Score
                  </p>
                  <p className="text-lg font-semibold text-aegis-text">
                    {stats.highest_threat_score.toFixed(2)}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div className="rounded-2xl border border-aegis-border bg-aegis-surface/60 p-5">
            <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
              <h3 className="text-sm font-semibold text-aegis-text">
                Security Activity
              </h3>
              {stats.activity.length > 0 && (
                <select
                  value={selectedWeekIdx}
                  onChange={(e) => setSelectedWeekIdx(Number(e.target.value))}
                  className="h-8 rounded-lg border border-aegis-border bg-aegis-surface2/60 px-2 text-xs text-aegis-text"
                >
                  {stats.activity.map((w, idx) => (
                    <option key={w.week} value={idx}>
                      {formatDate(w.start_date)} – {formatDate(w.end_date)}
                    </option>
                  ))}
                </select>
              )}
            </div>
            {selectedWeek ? (
              <ActivityChart week={selectedWeek} />
            ) : (
              <p className="text-sm text-aegis-textMuted">
                No weekly activity recorded yet.
              </p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
