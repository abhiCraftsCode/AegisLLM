import { useEffect, useRef, useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { AlertTriangle } from "lucide-react";
import { Logo } from "@/components/common/Logo";
import { Button } from "@/components/ui/Button";
import { useAuth } from "@/hooks/useAuth";
import { ApiError } from "@/lib/api";
import type { OAuthProvider } from "@/types/api";

export default function OAuthCallbackPage() {
  const [params] = useSearchParams();
  const { loginWithOAuth } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);
  const ran = useRef(false);

  useEffect(() => {
    if (ran.current) return;
    ran.current = true;

    const code = params.get("code");
    const provider = params.get("state") as OAuthProvider | null;
    const oauthError = params.get("error");

    if (oauthError) {
      setError("The provider declined the sign-in request.");
      return;
    }
    if (!code || (provider !== "google" && provider !== "github")) {
      setError("Missing authorization code or provider.");
      return;
    }

    loginWithOAuth(provider, code)
      .then(() => navigate("/app/dashboard", { replace: true }))
      .catch((err) => {
        setError(err instanceof ApiError ? err.message : "OAuth sign-in failed. Please try again.");
      });
  }, [params, loginWithOAuth, navigate]);

  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-4 bg-aegis-bg px-4 text-center">
      {!error ? (
        <>
          <div className="animate-pulse">
            <Logo size={36} />
          </div>
          <p className="text-sm text-aegis-textMuted">Completing sign-in…</p>
        </>
      ) : (
        <>
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-aegis-coral/10 text-aegis-coral">
            <AlertTriangle size={20} />
          </div>
          <p className="max-w-sm text-sm text-aegis-textMuted">{error}</p>
          <Link to="/login">
            <Button size="sm">Back to Sign In</Button>
          </Link>
        </>
      )}
    </div>
  );
}
