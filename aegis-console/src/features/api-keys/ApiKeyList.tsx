import { StatusBadge } from "@/components/ui/StatusBadge";
import { formatDateTime } from "@/lib/utils";
import type { KeySchema } from "@/types/api";

export function ApiKeyList({ keys, onSelect }: { keys: KeySchema[]; onSelect: (key: KeySchema) => void }) {
  return (
    <div className="flex flex-col gap-2">
      {keys.map((key) => (
        <button
          key={key.id}
          onClick={() => onSelect(key)}
          className="flex flex-col gap-2 rounded-xl border border-aegis-border bg-aegis-surface/50 p-4 text-left transition-colors hover:border-aegis-borderStrong hover:bg-aegis-surface2/60 sm:flex-row sm:items-center sm:justify-between"
        >
          <div className="flex items-center gap-3">
            <div>
              <p className="text-sm font-semibold text-aegis-text">{key.name ?? "Untitled key"}</p>
              <p className="font-mono text-xs text-aegis-textFaint">{key.prefix}</p>
            </div>
          </div>
          <div className="flex flex-wrap items-center gap-4 sm:gap-6">
            <StatusBadge tone={key.is_active ? "success" : "danger"}>{key.is_active ? "Active" : "Revoked"}</StatusBadge>
            <div className="text-xs text-aegis-textMuted">
              <p className="text-aegis-textFaint">Created</p>
              {formatDateTime(key.created_at)}
            </div>
            <div className="text-xs text-aegis-textMuted">
              <p className="text-aegis-textFaint">Last used</p>
              {key.last_used_at ? formatDateTime(key.last_used_at) : "Never"}
            </div>
          </div>
        </button>
      ))}
    </div>
  );
}
