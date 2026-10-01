import { useState } from "react";
import { Link } from "react-router-dom";
import { User, KeyRound, ArrowRight } from "lucide-react";
import { PageHeader } from "@/components/common/PageHeader";
import { Button } from "@/components/ui/Button";
import { PasswordForm } from "@/features/settings/PasswordForm";

export default function SettingsPage() {
  const [passwordOpen, setPasswordOpen] = useState(false);

  return (
    <div className="max-w-2xl">
      <PageHeader title="Settings" description="Manage your account and application preferences." />

      <div className="flex flex-col gap-4">
        <div className="flex items-center justify-between rounded-2xl border border-aegis-border bg-aegis-surface/60 p-5">
          <div className="flex items-center gap-3">
            <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-aegis-cyanSoft text-aegis-cyan">
              <User size={18} />
            </span>
            <div>
              <p className="text-sm font-semibold text-aegis-text">Profile</p>
              <p className="text-xs text-aegis-textMuted">Update your name, email and phone number.</p>
            </div>
          </div>
          <Link to="/app/profile">
            <Button variant="secondary" size="sm">
              Manage Profile <ArrowRight size={14} />
            </Button>
          </Link>
        </div>

        <div className="rounded-2xl border border-aegis-border bg-aegis-surface/60 p-5">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-aegis-violet/10 text-aegis-violet">
                <KeyRound size={18} />
              </span>
              <div>
                <p className="text-sm font-semibold text-aegis-text">Password</p>
                <p className="text-xs text-aegis-textMuted">Change your account password.</p>
              </div>
            </div>
            <Button variant="secondary" size="sm" onClick={() => setPasswordOpen(true)}>
              Change Password
            </Button>
          </div>
          <div className="mt-4 flex items-center justify-between border-t border-aegis-border pt-4">
            <div>
              <p className="text-sm text-aegis-text">Forgot your password?</p>
              <p className="text-xs text-aegis-textMuted">Request a password reset through email.</p>
            </div>
            <Link to="/forgot-password">
              <Button variant="ghost" size="sm">
                Reset Password
              </Button>
            </Link>
          </div>
        </div>
      </div>

      <PasswordForm open={passwordOpen} onClose={() => setPasswordOpen(false)} />
    </div>
  );
}
