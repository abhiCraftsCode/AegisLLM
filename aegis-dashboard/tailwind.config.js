/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["'Inter'", "system-ui", "sans-serif"],
        mono: ["'JetBrains Mono'", "ui-monospace", "monospace"],
      },
      colors: {
        aegis: {
          bg: "#0b0f1a",
          bg2: "#0f1420",
          surface: "#141b2b",
          surface2: "#1a2336",
          elevated: "#1e2740",
          border: "rgba(148, 163, 184, 0.12)",
          borderStrong: "rgba(148, 163, 184, 0.22)",
          cyan: "#4fd8e0",
          cyanSoft: "rgba(79, 216, 224, 0.14)",
          violet: "#8b7cf6",
          mint: "#34d399",
          amber: "#f5b350",
          coral: "#f4694f",
          text: "#e6ebf5",
          textMuted: "#9aa6bd",
          textFaint: "#5c6780",
        },
      },
      boxShadow: {
        elevated: "0 8px 30px -10px rgba(0,0,0,0.45)",
        glow: "0 0 40px -10px rgba(79, 216, 224, 0.35)",
      },
      keyframes: {
        shimmer: {
          "0%": { backgroundPosition: "-400px 0" },
          "100%": { backgroundPosition: "400px 0" },
        },
        fadeIn: {
          "0%": { opacity: 0 },
          "100%": { opacity: 1 },
        },
        scaleIn: {
          "0%": { opacity: 0, transform: "scale(0.97)" },
          "100%": { opacity: 1, transform: "scale(1)" },
        },
        driftSlow: {
          "0%, 100%": { transform: "translate(0,0)" },
          "50%": { transform: "translate(12px,-10px)" },
        },
      },
      animation: {
        shimmer: "shimmer 1.6s ease-in-out infinite",
        fadeIn: "fadeIn 0.35s ease-out",
        scaleIn: "scaleIn 0.28s cubic-bezier(0.16,1,0.3,1)",
        driftSlow: "driftSlow 12s ease-in-out infinite",
      },
    },
  },
  plugins: [],
};
