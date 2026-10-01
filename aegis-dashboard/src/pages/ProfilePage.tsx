import { useState } from "react";
import { Link } from "react-router-dom";
import { PageHeader } from "@/components/common/PageHeader";
import { Button } from "@/components/ui/Button";
import { useAuth } from "@/hooks/useAuth";
import { ProfileForm } from "@/features/settings/ProfileForm";
import { PasswordForm } from "@/features/settings/PasswordForm";
import { getInitials, formatDate } from "@/lib/utils";

export default function ProfilePage() {
  const { user } = useAuth();
  const [passwordOpen, setPasswordOpen] = useState(false);

  if (!user) return null;

  return (
    <div>
      <PageHeader title="Profile" description="Manage your personal account information." />

      <div className="mb-6 flex items-center gap-4 rounded-2xl border border-aegis-border bg-aegis-surface/60 p-5">
        <span className="flex h-14 w-14 items-center justify-center rounded-full bg-aegis-cyanSoft text-lg font-semibold text-aegis-cyan">
          {getInitials(user.name)}
        </span>
        <div>
          <p className="text-base font-semibold text-aegis-text">{user.name}</p>
          <p className="text-sm text-aegis-textMuted">
            {user.is_active ? "Active" : "Inactive"} · Member since {formatDate(user.created_at)}
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-5 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <div className="rounded-2xl border border-aegis-border bg-aegis-surface/60 p-5">
            <h2 className="mb-4 text-sm font-semibold text-aegis-text">Account details</h2>
            <ProfileForm />
          </div>
        </div>

        <div className="rounded-2xl border border-aegis-border bg-aegis-surface/60 p-5">
          <h2 className="text-sm font-semibold text-aegis-text">Security</h2>
          <p className="mt-1 text-sm text-aegis-textMuted">Password</p>
          <p className="text-xs text-aegis-textFaint">Change your account password.</p>
          <Button size="sm" variant="secondary" className="mt-3 w-full" onClick={() => setPasswordOpen(true)}>
            Change Password
          </Button>
          <Link to="/forgot-password" className="mt-3 block text-center text-xs font-medium text-aegis-cyan hover:underline">
            Forgot your password?
          </Link>
        </div>
      </div>

      <PasswordForm open={passwordOpen} onClose={() => setPasswordOpen(false)} />
    </div>
  );
}
