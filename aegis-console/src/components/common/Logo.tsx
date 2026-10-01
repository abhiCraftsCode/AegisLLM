import { cn } from "@/lib/utils";

interface LogoProps {
  size?: number;
  className?: string;
  withWordmark?: boolean;
}

/**
 * Abstract Aegis mark: three interlocking angular strata that suggest a
 * shield without drawing a literal shield outline. Consistent across
 * landing, auth, sidebar and topbar per spec section 6.
 */
export function Logo({ size = 28, className, withWordmark = false }: LogoProps) {
  return (
    <span className={cn("inline-flex items-center gap-2.5", className)}>
      <svg
        width={size}
        height={size}
        viewBox="0 0 40 40"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        aria-hidden="true"
      >
        <defs>
          <linearGradient id="aegisGradA" x1="4" y1="2" x2="36" y2="38" gradientUnits="userSpaceOnUse">
            <stop offset="0" stopColor="#4fd8e0" />
            <stop offset="1" stopColor="#8b7cf6" />
          </linearGradient>
        </defs>
        <path
          d="M20 2 L36 9 V19 C36 28.5 29.5 34.8 20 38 C10.5 34.8 4 28.5 4 19 V9 Z"
          fill="url(#aegisGradA)"
          fillOpacity="0.14"
          stroke="url(#aegisGradA)"
          strokeWidth="1.4"
        />
        <path d="M20 8 L29.5 12.2 V19.3 C29.5 25.3 25.5 29.5 20 32" stroke="#4fd8e0" strokeWidth="1.8" strokeLinecap="round" fill="none" />
        <path d="M20 8 L10.5 12.2 V19.3 C10.5 25.3 14.5 29.5 20 32" stroke="#8b7cf6" strokeWidth="1.8" strokeLinecap="round" fill="none" opacity="0.85" />
        <circle cx="20" cy="19" r="3.4" fill="#4fd8e0" />
      </svg>
      {withWordmark && <span className="text-base font-semibold tracking-tight text-aegis-text">AegisLLM</span>}
    </span>
  );
}
