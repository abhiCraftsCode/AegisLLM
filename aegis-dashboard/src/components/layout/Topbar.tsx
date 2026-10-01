import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import { Menu, ChevronDown, User, Settings, LogOut } from "lucide-react";
import { useAuth } from "@/hooks/useAuth";
import { ThemeToggle } from "@/components/common/ThemeToggle";
import { getInitials } from "@/lib/utils";

export function Topbar({ onOpenMobileNav }: { onOpenMobileNav: () => void }) {
  const { user, logout } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function onClick(e: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) setMenuOpen(false);
    }
    document.addEventListener("mousedown", onClick);
    return () => document.removeEventListener("mousedown", onClick);
  }, []);

  return (
    <header className="flex h-16 items-center justify-between border-b border-aegis-border bg-aegis-bg/80 px-4 backdrop-blur-md sm:px-6">
      <button
        onClick={onOpenMobileNav}
        aria-label="Open navigation"
        className="rounded-lg p-2 text-aegis-textMuted hover:bg-white/5 hover:text-aegis-text lg:hidden"
      >
        <Menu size={20} />
      </button>

      <div className="flex-1" />

      <div className="flex items-center gap-3">
        <ThemeToggle />
        <div className="relative" ref={menuRef}>
          <button
            onClick={() => setMenuOpen((v) => !v)}
            className="flex items-center gap-2 rounded-lg border border-aegis-border py-1.5 pl-1.5 pr-2.5 hover:bg-white/5"
            aria-haspopup="menu"
            aria-expanded={menuOpen}
          >
            <span className="flex h-7 w-7 items-center justify-center rounded-full bg-aegis-cyanSoft text-xs font-semibold text-aegis-cyan">
              {user ? getInitials(user.name) : "?"}
            </span>
            <span className="hidden max-w-[120px] truncate text-sm font-medium text-aegis-text sm:inline">
              {user?.name ?? "Account"}
            </span>
            <ChevronDown size={14} className="text-aegis-textMuted" />
          </button>

          {menuOpen && (
            <div
              role="menu"
              className="absolute right-0 top-full z-40 mt-2 w-48 animate-scaleIn overflow-hidden rounded-xl border border-aegis-border bg-aegis-elevated shadow-elevated"
            >
              <Link
                to="/app/profile"
                role="menuitem"
                onClick={() => setMenuOpen(false)}
                className="flex items-center gap-2.5 px-3.5 py-2.5 text-sm text-aegis-text hover:bg-white/5"
              >
                <User size={15} /> Profile
              </Link>
              <Link
                to="/app/settings"
                role="menuitem"
                onClick={() => setMenuOpen(false)}
                className="flex items-center gap-2.5 px-3.5 py-2.5 text-sm text-aegis-text hover:bg-white/5"
              >
                <Settings size={15} /> Settings
              </Link>
              <button
                role="menuitem"
                onClick={logout}
                className="flex w-full items-center gap-2.5 border-t border-aegis-border px-3.5 py-2.5 text-sm text-aegis-coral hover:bg-aegis-coral/10"
              >
                <LogOut size={15} /> Logout
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
