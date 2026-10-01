import { Link } from "react-router-dom";
import { Logo } from "@/components/common/Logo";
import { ResetPasswordForm } from "@/features/auth/ResetPasswordForm";

export default function ResetPasswordPage() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-aegis-bg px-4">
      <div className="w-full max-w-sm">
        <div className="mb-8 flex justify-center">
          <Link to="/">
            <Logo size={32} withWordmark />
          </Link>
        </div>
        <div className="rounded-2xl border border-aegis-border bg-aegis-surface/60 p-6 shadow-elevated">
          <h1 className="text-lg font-semibold text-aegis-text">Set a new password</h1>
          <p className="mt-1 text-sm text-aegis-textMuted">Choose a new password for your account.</p>
          <div className="mt-6">
            <ResetPasswordForm />
          </div>
        </div>
      </div>
    </div>
  );
}
