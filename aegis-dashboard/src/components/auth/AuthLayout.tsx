import type { ReactNode } from "react";
import { Link } from "react-router-dom";
import { Logo } from "@/components/common/Logo";
import { ThemeToggle } from "@/components/common/ThemeToggle";
import { AuthVisual } from "./AuthVisual";

export function AuthLayout({
  title,
  subtitle,
  children,
}: {
  title: string;
  subtitle: string;
  children: ReactNode;
}) {
  return (
    <div className="flex min-h-screen bg-aegis-bg">
      <div className="relative hidden w-1/2 overflow-hidden border-r border-aegis-border lg:flex lg:flex-col lg:justify-between">
        <AuthVisual />
        <div className="relative z-10 p-10">
          <Link to="/" className="inline-flex">
            <Logo size={32} withWordmark />
          </Link>
        </div>
        <div className="relative z-10 p-10">
          <p className="max-w-sm text-lg font-medium leading-snug text-aegis-text">
            Secure every prompt. Trust every response.
          </p>
          <p className="mt-2 max-w-sm text-sm text-aegis-textMuted">
            AegisLLM inspects every request before it reaches your language model.
          </p>
        </div>
      </div>

      <div className="flex w-full flex-col lg:w-1/2">
        <div className="flex items-center justify-between p-6">
          <Link to="/" className="inline-flex lg:hidden">
            <Logo size={26} withWordmark />
          </Link>
          <div className="ml-auto">
            <ThemeToggle />
          </div>
        </div>
        <div className="flex flex-1 items-center justify-center px-6 pb-12">
          <div className="w-full max-w-sm">
            <h1 className="text-xl font-semibold text-aegis-text">{title}</h1>
            <p className="mt-1.5 text-sm text-aegis-textMuted">{subtitle}</p>
            <div className="mt-8">{children}</div>
          </div>
        </div>
      </div>
    </div>
  );
}
