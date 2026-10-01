import { Link } from "react-router-dom";
import { Logo } from "@/components/common/Logo";
import { ForgotPasswordForm } from "@/features/auth/ForgotPasswordForm";

export default function ForgotPasswordPage() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-aegis-bg px-4">
      <div className="w-full max-w-sm">
        <div className="mb-8 flex justify-center">
          <Link to="/">
            <Logo size={32} withWordmark />
          </Link>
        </div>
        <div className="rounded-2xl border border-aegis-border bg-aegis-surface/60 p-6 shadow-elevated">
          <h1 className="text-lg font-semibold text-aegis-text">Reset your password</h1>
          <p className="mt-1 text-sm text-aegis-textMuted">
            Enter the email associated with your account.
          </p>
          <div className="mt-6">
            <ForgotPasswordForm />
          </div>
        </div>
      </div>
    </div>
  );
}
