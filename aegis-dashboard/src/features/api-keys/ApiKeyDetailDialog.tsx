import type { ReactNode } from "react";
import { StatusBadge } from "@/components/ui/StatusBadge";
import { Button } from "@/components/ui/Button";
import { Dialog } from "@/components/ui/Dialog";
import { formatDateTime } from "@/lib/utils";
import type { KeySchema } from "@/types/api";

function Field({ label, value }: { label: string; value: ReactNode }) {
  return (
    <div className="flex items-center justify-between border-b border-aegis-border py-2.5 last:border-0">
      <span className="text-xs text-aegis-textMuted">{label}</span>
      <span className="text-sm font-medium text-aegis-text">{value}</span>
    </div>
  );
}

export function ApiKeyDetailDialog({
  keyRecord,
  onClose,
  onEdit,
  onRevoke,
}: {
  keyRecord: KeySchema;
  onClose: () => void;
  onEdit: () => void;
  onRevoke: () => void;
}) {
  return (
    <Dialog open onClose={onClose} title={keyRecord.name ?? "Untitled key"} description={keyRecord.prefix}>
      <div>
        <Field label="Status" value={<StatusBadge tone={keyRecord.is_active ? "success" : "danger"}>{keyRecord.is_active ? "Active" : "Revoked"}</StatusBadge>} />
        <Field label="Prefix" value={<code className="font-mono text-xs">{keyRecord.prefix}</code>} />
        <Field label="Created" value={formatDateTime(keyRecord.created_at)} />
        <Field label="Last used" value={keyRecord.last_used_at ? formatDateTime(keyRecord.last_used_at) : "Never"} />
        <Field label="LLM name" value={keyRecord.llm_name ?? "—"} />
        <Field label="LLM URL" value={<span className="max-w-[220px] truncate text-right">{keyRecord.llm_url ?? "—"}</span>} />
      </div>
      <div className="mt-6 flex justify-end gap-2">
        {keyRecord.is_active && (
          <Button variant="danger" size="sm" onClick={onRevoke}>
            Revoke Key
          </Button>
        )}
        <Button variant="secondary" size="sm" onClick={onEdit}>
          Edit
        </Button>
      </div>
    </Dialog>
  );
}
