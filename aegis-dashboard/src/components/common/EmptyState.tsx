import type { ReactNode } from "react";
import { Logo } from "./Logo";

export function EmptyState({
  title,
  description,
  action,
}: {
  title: string;
  description?: string;
  action?: ReactNode;
}) {
  return (
    <div className="flex flex-col items-center justify-center rounded-2xl border border-dashed border-aegis-border bg-aegis-surface/40 px-6 py-14 text-center">
      <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-aegis-cyanSoft">
        <Logo size={22} />
      </div>
      <h3 className="text-sm font-semibold text-aegis-text">{title}</h3>
      {description && <p className="mt-1.5 max-w-xs text-sm text-aegis-textMuted">{description}</p>}
      {action && <div className="mt-5">{action}</div>}
    </div>
  );
}
