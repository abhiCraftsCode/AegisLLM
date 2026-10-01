import type { ReactNode } from "react";
import { cn } from "@/lib/utils";

type Tone = "success" | "danger" | "neutral" | "warning";

export function StatusBadge({ tone, children }: { tone: Tone; children: ReactNode }) {
  const toneClasses: Record<Tone, string> = {
    success: "bg-aegis-mint/10 text-aegis-mint border-aegis-mint/25",
    danger: "bg-aegis-coral/10 text-aegis-coral border-aegis-coral/25",
    neutral: "bg-white/5 text-aegis-textMuted border-aegis-border",
    warning: "bg-aegis-amber/10 text-aegis-amber border-aegis-amber/25",
  };
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-xs font-medium",
        toneClasses[tone]
      )}
    >
      <span className="h-1.5 w-1.5 rounded-full bg-current" />
      {children}
    </span>
  );
}
