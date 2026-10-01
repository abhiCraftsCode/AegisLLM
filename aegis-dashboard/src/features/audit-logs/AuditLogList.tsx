import { StatusBadge } from "@/components/ui/StatusBadge";
import { formatDateTime, shortenId } from "@/lib/utils";
import type { LogSchema } from "@/types/api";

export function AuditLogList({ logs, onSelect }: { logs: LogSchema[]; onSelect: (log: LogSchema) => void }) {
  return (
    <div className="flex flex-col gap-2">
      {logs.map((log) => (
        <button
          key={log.id}
          onClick={() => onSelect(log)}
          className="flex flex-col gap-2 rounded-xl border border-aegis-border bg-aegis-surface/50 p-4 text-left transition-colors hover:border-aegis-borderStrong hover:bg-aegis-surface2/60 sm:flex-row sm:items-center sm:justify-between"
        >
          <div className="flex items-center gap-3">
            <StatusBadge tone={log.is_blocked ? "danger" : "success"}>{log.is_blocked ? "Blocked" : "Allowed"}</StatusBadge>
            <div>
              <p className="max-w-[280px] truncate text-sm text-aegis-text">{log.reason ?? "No reason provided"}</p>
              <p className="font-mono text-xs text-aegis-textFaint">{shortenId(log.request_id)}</p>
            </div>
          </div>
          <div className="flex flex-wrap items-center gap-4 sm:gap-6">
            <div className="text-xs text-aegis-textMuted">
              <p className="text-aegis-textFaint">Threat score</p>
              {log.threat_score.toFixed(2)}
            </div>
            <div className="text-xs text-aegis-textMuted">
              <p className="text-aegis-textFaint">Latency</p>
              {log.latency_ms.toFixed(1)} ms
            </div>
            <div className="text-xs text-aegis-textMuted">
              <p className="text-aegis-textFaint">Created</p>
              {formatDateTime(log.created_at)}
            </div>
          </div>
        </button>
      ))}
    </div>
  );
}
