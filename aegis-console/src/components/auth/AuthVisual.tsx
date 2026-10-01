import { Logo } from "@/components/common/Logo";

/**
 * Purely decorative — no interactivity, no backend calls.
 */
export function AuthVisual() {
  return (
    <div className="absolute inset-0" aria-hidden="true">
      <div className="absolute inset-0 bg-gradient-to-br from-aegis-bg via-aegis-bg2 to-[#0d1526]" />
      <div className="absolute left-1/2 top-1/2 h-[420px] w-[420px] -translate-x-1/2 -translate-y-1/2 animate-driftSlow rounded-full bg-aegis-cyan/10 blur-[100px]" />
      <div className="absolute left-1/3 top-2/3 h-[280px] w-[280px] animate-driftSlow rounded-full bg-aegis-violet/10 blur-[90px] [animation-delay:-4s]" />
      <div className="absolute inset-0 flex items-center justify-center">
        <div className="relative flex h-56 w-56 items-center justify-center rounded-3xl border border-aegis-border/60 bg-white/[0.02] backdrop-blur-sm">
          <div className="absolute inset-3 rounded-2xl border border-dashed border-aegis-cyan/20" />
          <Logo size={72} />
        </div>
      </div>
    </div>
  );
}
