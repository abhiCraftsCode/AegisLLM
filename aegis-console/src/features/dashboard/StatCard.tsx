import type { ReactNode } from "react";
import { cn } from "@/lib/utils";

export function StatCard({
  label,
  value,
  sub,
  icon,
  tone = "default",
}: {
  label: string;
  value: ReactNode;
  sub?: ReactNode;
  icon?: ReactNode;
  tone?: "default" | "danger" | "accent";
}) {
  return (
    <div className="rounded-2xl border border-aegis-border bg-aegis-surface/60 p-5">
      <div className="flex items-center justify-between">
        <p className="text-sm font-medium text-aegis-textMuted">{label}</p>
        {icon && (
          <span
            className={cn(
              "flex h-8 w-8 items-center justify-center rounded-lg",
              tone === "danger" && "bg-aegis-coral/10 text-aegis-coral",
              tone === "accent" && "bg-aegis-cyanSoft text-aegis-cyan",
              tone === "default" && "bg-white/5 text-aegis-textMuted"
            )}
          >
            {icon}
          </span>
        )}
      </div>
      <p className="mt-3 text-2xl font-semibold tracking-tight text-aegis-text">{value}</p>
      {sub && <p className="mt-1 text-xs text-aegis-textFaint">{sub}</p>}
    </div>
  );
}
