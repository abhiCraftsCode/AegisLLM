import { Link } from "react-router-dom";
import { Logo } from "@/components/common/Logo";
import { Button } from "@/components/ui/Button";
import { useAuth } from "@/hooks/useAuth";

export default function NotFoundPage() {
  const { isAuthenticated } = useAuth();
  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-5 bg-aegis-bg px-4 text-center">
      <div className="animate-fadeIn">
        <Logo size={40} />
      </div>
      <div>
        <p className="text-5xl font-semibold tracking-tight text-aegis-text">404</p>
        <p className="mt-2 text-sm text-aegis-textMuted">This route doesn&apos;t exist.</p>
      </div>
      <Link to={isAuthenticated ? "/app/dashboard" : "/"}>
        <Button size="sm">{isAuthenticated ? "Return to Dashboard" : "Return home"}</Button>
      </Link>
    </div>
  );
}
