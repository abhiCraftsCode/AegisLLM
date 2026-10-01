import { Link } from "react-router-dom";
import { ShieldCheck, ScanSearch, Gauge, ScrollText, ArrowRight } from "lucide-react";
import { Logo } from "@/components/common/Logo";
import { ThemeToggle } from "@/components/common/ThemeToggle";
import { Button } from "@/components/ui/Button";

const capabilities = [
  {
    icon: ScanSearch,
    title: "Prompt Inspection",
    description: "Every prompt is analyzed before it ever reaches your language model.",
  },
  {
    icon: ShieldCheck,
    title: "Threat Detection",
    description: "A security engine scores each request and flags what looks unsafe.",
  },
  {
    icon: Gauge,
    title: "Gateway Protection",
    description: "AegisLLM sits in front of your LLM, so nothing gets through unchecked.",
  },
  {
    icon: ScrollText,
    title: "Audit Logging",
    description: "Every inspection is recorded, so you can review activity later.",
  },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-aegis-bg">
      {/* Navbar */}
      <header className="sticky top-0 z-30 border-b border-aegis-border bg-aegis-bg/80 backdrop-blur-md">
        <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4 sm:px-6">
          <Link to="/" className="flex items-center gap-2.5">
            <Logo size={26} withWordmark />
          </Link>
          <div className="flex items-center gap-2 sm:gap-3">
            <ThemeToggle />
            <Link to="/login">
              <Button variant="ghost" size="sm">
                Login
              </Button>
            </Link>
            <Link to="/register">
              <Button size="sm">Get Started</Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="relative overflow-hidden px-4 pb-20 pt-16 sm:px-6 sm:pt-24">
        <div className="pointer-events-none absolute inset-0" aria-hidden="true">
          <div className="absolute left-1/2 top-0 h-[500px] w-[700px] -translate-x-1/2 animate-driftSlow rounded-full bg-aegis-cyan/[0.06] blur-[120px]" />
        </div>

        <div className="relative mx-auto max-w-3xl text-center">
          <span className="inline-flex items-center rounded-full border border-aegis-border bg-aegis-surface/60 px-3 py-1 text-xs font-medium text-aegis-textMuted">
            LLM SECURITY GATEWAY
          </span>
          <h1 className="mt-6 text-4xl font-semibold tracking-tight text-aegis-text sm:text-5xl">
            Secure every prompt.
            <br />
            Trust every response.
          </h1>
          <p className="mx-auto mt-5 max-w-xl text-base text-aegis-textMuted">
            AegisLLM inspects requests before they reach your language model, scoring threats and
            recording every decision so you can see exactly what your gateway is protecting against.
          </p>
          <div className="mt-8 flex flex-col items-center justify-center gap-3 sm:flex-row">
            <Link to="/register">
              <Button size="lg">
                Get Started <ArrowRight size={16} />
              </Button>
            </Link>
            <Link to="/login">
              <Button variant="secondary" size="lg">
                Sign In
              </Button>
            </Link>
          </div>
        </div>

        {/* Pipeline visual - decorative only, not interactive */}
        <div className="relative mx-auto mt-16 max-w-3xl" aria-hidden="true">
          <div className="flex flex-col items-stretch gap-3 rounded-2xl border border-aegis-border bg-aegis-surface/50 p-6 sm:flex-row sm:items-center sm:justify-between">
            {[
              { label: "Application" },
              { label: "AegisLLM" },
              { label: "Security Engine" },
              { label: "Allowed / Blocked" },
              { label: "LLM" },
            ].map((step, idx, arr) => (
              <div key={step.label} className="flex items-center gap-3">
                <div className="flex flex-1 items-center justify-center rounded-xl border border-aegis-border bg-white/[0.02] px-4 py-3 text-center text-xs font-medium text-aegis-text sm:min-w-[110px]">
                  {step.label}
                </div>
                {idx < arr.length - 1 && (
                  <ArrowRight size={16} className="hidden shrink-0 text-aegis-cyan/50 sm:block" />
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Capabilities */}
      <section className="border-t border-aegis-border px-4 py-16 sm:px-6">
        <div className="mx-auto max-w-6xl">
          <h2 className="text-center text-2xl font-semibold text-aegis-text">What AegisLLM does</h2>
          <div className="mt-10 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {capabilities.map((cap) => (
              <div key={cap.title} className="rounded-2xl border border-aegis-border bg-aegis-surface/50 p-5">
                <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-aegis-cyanSoft text-aegis-cyan">
                  <cap.icon size={18} />
                </span>
                <h3 className="mt-4 text-sm font-semibold text-aegis-text">{cap.title}</h3>
                <p className="mt-1.5 text-sm text-aegis-textMuted">{cap.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="border-t border-aegis-border px-4 py-16 sm:px-6">
        <div className="mx-auto max-w-3xl text-center">
          <h2 className="text-2xl font-semibold text-aegis-text">How AegisLLM works</h2>
          <p className="mx-auto mt-3 max-w-xl text-sm text-aegis-textMuted">
            Your application sends prompts to AegisLLM instead of directly to your model. The
            security engine inspects each one, then the request is allowed through or blocked
            before it reaches your LLM.
          </p>
          <div className="mt-10 flex flex-col items-center gap-3" aria-hidden="true">
            {["Your Application", "AegisLLM", "Security Engine", "LLM"].map((step, idx, arr) => (
              <div key={step} className="flex flex-col items-center">
                <div className="w-56 rounded-xl border border-aegis-border bg-aegis-surface/50 px-4 py-3 text-sm font-medium text-aegis-text">
                  {step}
                </div>
                {idx < arr.length - 1 && <div className="my-1 h-6 w-px bg-aegis-border" />}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="border-t border-aegis-border px-4 py-16 sm:px-6">
        <div className="mx-auto max-w-2xl rounded-2xl border border-aegis-border bg-aegis-surface/50 p-10 text-center">
          <h2 className="text-2xl font-semibold text-aegis-text">
            Secure every prompt.
            <br />
            Trust every response.
          </h2>
          <Link to="/register" className="mt-6 inline-block">
            <Button size="lg">
              Get Started <ArrowRight size={16} />
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-aegis-border px-4 py-10 sm:px-6">
        <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-3 sm:flex-row">
          <div className="flex items-center gap-2.5">
            <Logo size={20} />
            <span className="text-sm text-aegis-textMuted">AegisLLM · LLM Security Gateway</span>
          </div>
          <div className="flex items-center gap-4 text-sm text-aegis-textMuted">
            <Link to="/login" className="hover:text-aegis-text">
              Login
            </Link>
            <Link to="/register" className="hover:text-aegis-text">
              Get Started
            </Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
