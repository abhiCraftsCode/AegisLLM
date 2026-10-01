import { GOOGLE_CLIENT_ID, GITHUB_CLIENT_ID, OAUTH_REDIRECT_URI } from "@/lib/constants";

function startGoogleOAuth() {
  const params = new URLSearchParams({
    client_id: GOOGLE_CLIENT_ID,
    redirect_uri: OAUTH_REDIRECT_URI,
    response_type: "code",
    scope: "openid email profile",
    state: "google",
    prompt: "select_account",
  });
  window.location.href = `https://accounts.google.com/o/oauth2/v2/auth?${params.toString()}`;
}

function startGithubOAuth() {
  const params = new URLSearchParams({
    client_id: GITHUB_CLIENT_ID,
    redirect_uri: OAUTH_REDIRECT_URI,
    scope: "read:user user:email",
    state: "github",
  });
  window.location.href = `https://github.com/login/oauth/authorize?${params.toString()}`;
}

/**
 * The backend supports google + github via POST /auth/oauth { provider, code }
 * (authorization-code exchange). Buttons are disabled if the corresponding
 * client ID hasn't been configured for this deployment, so we never fake a
 * successful login.
 */
export function OAuthButtons() {
  const googleReady = !!GOOGLE_CLIENT_ID;
  const githubReady = !!GITHUB_CLIENT_ID;

  return (
    <div className="flex flex-col gap-2">
      <div className="relative flex items-center py-1">
        <div className="h-px flex-1 bg-aegis-border" />
        <span className="px-3 text-xs text-aegis-textFaint">or continue with</span>
        <div className="h-px flex-1 bg-aegis-border" />
      </div>
      <div className="grid grid-cols-2 gap-2">
        <button
          type="button"
          onClick={startGoogleOAuth}
          disabled={!googleReady}
          title={googleReady ? undefined : "Google OAuth is not configured for this deployment"}
          className="flex h-10 items-center justify-center gap-2 rounded-lg border border-aegis-borderStrong bg-aegis-elevated text-sm font-medium text-aegis-text transition-colors hover:bg-aegis-surface2 disabled:cursor-not-allowed disabled:opacity-40"
        >
          <GoogleMark /> Google
        </button>
        <button
          type="button"
          onClick={startGithubOAuth}
          disabled={!githubReady}
          title={githubReady ? undefined : "GitHub OAuth is not configured for this deployment"}
          className="flex h-10 items-center justify-center gap-2 rounded-lg border border-aegis-borderStrong bg-aegis-elevated text-sm font-medium text-aegis-text transition-colors hover:bg-aegis-surface2 disabled:cursor-not-allowed disabled:opacity-40"
        >
          <GithubMark /> GitHub
        </button>
      </div>
    </div>
  );
}

function GoogleMark() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" aria-hidden="true">
      <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 01-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" />
      <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.99.66-2.25 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.85A11 11 0 0012 23z" />
      <path fill="#FBBC05" d="M5.84 14.1a6.6 6.6 0 010-4.2V7.05H2.18a11 11 0 000 9.9l3.66-2.85z" />
      <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1a11 11 0 00-9.82 6.05l3.66 2.85C6.71 7.3 9.14 5.38 12 5.38z" />
    </svg>
  );
}

function GithubMark() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
      <path d="M12 .5A11.5 11.5 0 000 12.25c0 5.14 3.29 9.5 7.86 11.04.58.11.79-.26.79-.57v-2c-3.2.71-3.87-1.4-3.87-1.4-.53-1.36-1.29-1.73-1.29-1.73-1.05-.73.08-.71.08-.71 1.17.08 1.78 1.22 1.78 1.22 1.03 1.79 2.7 1.27 3.36.97.1-.76.4-1.27.73-1.56-2.55-.29-5.24-1.29-5.24-5.76 0-1.27.45-2.31 1.19-3.13-.12-.3-.52-1.5.11-3.12 0 0 .97-.31 3.18 1.2a10.9 10.9 0 015.79 0c2.2-1.51 3.17-1.2 3.17-1.2.64 1.62.24 2.82.12 3.12.74.82 1.19 1.86 1.19 3.13 0 4.48-2.7 5.46-5.26 5.75.41.36.78 1.08.78 2.17v3.22c0 .31.21.69.8.57A11.75 11.75 0 0024 12.25 11.5 11.5 0 0012 .5z" />
    </svg>
  );
}
