import { AlertTriangle } from "lucide-react";
import { Button } from "@/components/ui/Button";

export function ErrorState({
  message = "We couldn't load this data.",
  onRetry,
}: {
  message?: string;
  onRetry?: () => void;
}) {
  return (
    <div className="flex flex-col items-center justify-center rounded-2xl border border-aegis-border bg-aegis-surface/40 px-6 py-14 text-center">
      <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-aegis-coral/10 text-aegis-coral">
        <AlertTriangle size={20} />
      </div>
      <h3 className="text-sm font-semibold text-aegis-text">Something went wrong</h3>
      <p className="mt-1.5 max-w-xs text-sm text-aegis-textMuted">{message}</p>
      {onRetry && (
        <Button variant="secondary" size="sm" className="mt-5" onClick={onRetry}>
          Retry
        </Button>
      )}
    </div>
  );
}
