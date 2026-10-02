import type { ComponentType } from "react";
import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  ShieldCheck,
  KeyRound,
  ScrollText,
  User,
  Settings,
  LogOut,
  ChevronsLeft,
  ChevronsRight,
  Plug,
} from "lucide-react";
import { Logo } from "@/components/common/Logo";
import { useAuth } from "@/hooks/useAuth";
import { cn } from "@/lib/utils";

interface NavItem {
  to: string;
  label: string;
  icon: ComponentType<{ size?: number }>;
}

interface NavGroup {
  label: string;
  items: NavItem[];
}

const groups: NavGroup[] = [
  {
    label: "Overview",
    items: [
      { to: "/app/dashboard", label: "Dashboard", icon: LayoutDashboard },
    ],
  },
  {
    label: "Security",
    items: [
      { to: "/app/inspector", label: "Inspector", icon: ShieldCheck },
      { to: "/app/audit-logs", label: "Audit Logs", icon: ScrollText },
    ],
  },
  {
    label: "Developer",
    items: [
      { to: "/app/api-keys", label: "API Keys", icon: KeyRound },
      { to: "/app/integrations", label: "Integrations", icon: Plug },
    ],
  },
  {
    label: "Account",
    items: [
      { to: "/app/profile", label: "Profile", icon: User },
      { to: "/app/settings", label: "Settings", icon: Settings },
    ],
  },
];

export function Sidebar({
  collapsed,
  onToggleCollapse,
  onNavigate,
}: {
  collapsed: boolean;
  onToggleCollapse?: () => void;
  onNavigate?: () => void;
}) {
  const { logout } = useAuth();

  return (
    <div className="flex h-full flex-col bg-aegis-surface/60">
      <div
        className={cn(
          "flex h-16 items-center border-b border-aegis-border px-4",
          collapsed && "justify-center px-0",
        )}
      >
        <NavLink
          to="/app/dashboard"
          className="flex items-center gap-2.5"
          onClick={onNavigate}
        >
          <Logo size={26} />
          {!collapsed && (
            <span className="text-sm font-semibold tracking-tight text-aegis-text">
              AegisLLM
            </span>
          )}
        </NavLink>
      </div>

      <nav className="flex-1 overflow-y-auto px-3 py-4">
        {groups.map((group) => (
          <div key={group.label} className="mb-5">
            {!collapsed && (
              <p className="mb-2 px-2 text-[11px] font-semibold uppercase tracking-wider text-aegis-textFaint">
                {group.label}
              </p>
            )}
            <div className="flex flex-col gap-1">
              {group.items.map((item) => (
                <NavLink
                  key={item.to}
                  to={item.to}
                  onClick={onNavigate}
                  title={collapsed ? item.label : undefined}
                  className={({ isActive }) =>
                    cn(
                      "group flex items-center gap-3 rounded-lg px-2.5 py-2 text-sm font-medium transition-colors",
                      collapsed && "justify-center",
                      isActive
                        ? "bg-aegis-cyanSoft text-aegis-cyan"
                        : "text-aegis-textMuted hover:bg-white/5 hover:text-aegis-text",
                    )
                  }
                >
                  <item.icon size={17} />
                  {!collapsed && <span>{item.label}</span>}
                </NavLink>
              ))}
            </div>
          </div>
        ))}
      </nav>

      <div className="border-t border-aegis-border p-3">
        <button
          onClick={logout}
          title={collapsed ? "Logout" : undefined}
          className={cn(
            "flex w-full items-center gap-3 rounded-lg px-2.5 py-2 text-sm font-medium text-aegis-textMuted transition-colors hover:bg-aegis-coral/10 hover:text-aegis-coral",
            collapsed && "justify-center",
          )}
        >
          <LogOut size={17} />
          {!collapsed && <span>Logout</span>}
        </button>
        {onToggleCollapse && (
          <button
            onClick={onToggleCollapse}
            className={cn(
              "mt-1 hidden w-full items-center gap-3 rounded-lg px-2.5 py-2 text-sm text-aegis-textFaint transition-colors hover:bg-white/5 hover:text-aegis-text lg:flex",
              collapsed && "justify-center",
            )}
            aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
          >
            {collapsed ? (
              <ChevronsRight size={17} />
            ) : (
              <ChevronsLeft size={17} />
            )}
            {!collapsed && <span>Collapse</span>}
          </button>
        )}
      </div>
    </div>
  );
}
