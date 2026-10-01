import { useState } from "react";
import { Outlet } from "react-router-dom";
import { Sidebar } from "./Sidebar";
import { Topbar } from "./Topbar";
import { cn } from "@/lib/utils";

export function DashboardLayout() {
  const [collapsed, setCollapsed] = useState(false);
  const [mobileNavOpen, setMobileNavOpen] = useState(false);

  return (
    <div className="relative flex min-h-screen bg-aegis-bg">
      <div className="pointer-events-none fixed inset-0 overflow-hidden">
        <div className="absolute -left-32 -top-32 h-[420px] w-[420px] animate-driftSlow rounded-full bg-aegis-cyan/[0.05] blur-[110px]" />
        <div className="absolute right-[-10%] top-1/3 h-[360px] w-[360px] animate-driftSlow rounded-full bg-aegis-violet/[0.05] blur-[100px] [animation-delay:-6s]" />
      </div>

      <aside
        className={cn(
          "sticky top-0 z-30 hidden h-screen shrink-0 border-r border-aegis-border transition-all duration-300 lg:block",
          collapsed ? "w-[76px]" : "w-64"
        )}
      >
        <Sidebar collapsed={collapsed} onToggleCollapse={() => setCollapsed((c) => !c)} />
      </aside>

      {mobileNavOpen && (
        <div className="fixed inset-0 z-50 lg:hidden">
          <div
            className="absolute inset-0 animate-fadeIn bg-black/60 backdrop-blur-sm"
            onClick={() => setMobileNavOpen(false)}
          />
          <div className="relative z-10 h-full w-72 animate-[scaleIn_0.25s_ease-out] border-r border-aegis-border">
            <Sidebar collapsed={false} onNavigate={() => setMobileNavOpen(false)} />
          </div>
        </div>
      )}

      <div className="relative z-10 flex min-h-screen flex-1 flex-col">
        <Topbar onOpenMobileNav={() => setMobileNavOpen(true)} />
        <main className="flex-1 px-4 py-6 sm:px-6 lg:px-8">
          <Outlet />
        </main>
        <footer className="border-t border-aegis-border px-6 py-4 text-center text-xs text-aegis-textFaint">
          AegisLLM • LLM Security Gateway · v1.0.0 · {new Date().getFullYear()}
        </footer>
      </div>
    </div>
  );
}
