import { forwardRef, useState, type InputHTMLAttributes } from "react";
import { Eye, EyeOff } from "lucide-react";
import { cn } from "@/lib/utils";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  hint?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className, label, error, hint, id, ...props }, ref) => {
    const inputId = id ?? props.name;
    return (
      <div className="flex flex-col gap-1.5">
        {label && (
          <label htmlFor={inputId} className="text-sm font-medium text-aegis-text">
            {label}
          </label>
        )}
        <input
          ref={ref}
          id={inputId}
          className={cn(
            "h-10 w-full rounded-lg border bg-aegis-surface2/60 px-3 text-sm text-aegis-text placeholder:text-aegis-textFaint",
            "outline-none transition-colors focus:border-aegis-cyan/60 focus:bg-aegis-surface2",
            error ? "border-aegis-coral/60" : "border-aegis-border",
            className
          )}
          aria-invalid={!!error}
          aria-describedby={error ? `${inputId}-error` : hint ? `${inputId}-hint` : undefined}
          {...props}
        />
        {error && (
          <p id={`${inputId}-error`} className="text-xs text-aegis-coral">
            {error}
          </p>
        )}
        {!error && hint && (
          <p id={`${inputId}-hint`} className="text-xs text-aegis-textFaint">
            {hint}
          </p>
        )}
      </div>
    );
  }
);
Input.displayName = "Input";

interface PasswordInputProps extends InputProps {}

export const PasswordInput = forwardRef<HTMLInputElement, PasswordInputProps>((props, ref) => {
  const [visible, setVisible] = useState(false);
  const { className, label, error, hint, id, ...rest } = props;
  const inputId = id ?? rest.name;

  return (
    <div className="flex flex-col gap-1.5">
      {label && (
        <label htmlFor={inputId} className="text-sm font-medium text-aegis-text">
          {label}
        </label>
      )}
      <div className="relative">
        <input
          ref={ref}
          id={inputId}
          type={visible ? "text" : "password"}
          className={cn(
            "h-10 w-full rounded-lg border bg-aegis-surface2/60 px-3 pr-10 text-sm text-aegis-text placeholder:text-aegis-textFaint",
            "outline-none transition-colors focus:border-aegis-cyan/60 focus:bg-aegis-surface2",
            error ? "border-aegis-coral/60" : "border-aegis-border",
            className
          )}
          aria-invalid={!!error}
          aria-describedby={error ? `${inputId}-error` : hint ? `${inputId}-hint` : undefined}
          {...rest}
        />
        <button
          type="button"
          onClick={() => setVisible((v) => !v)}
          aria-label={visible ? "Hide password" : "Show password"}
          className="absolute right-0 top-0 flex h-10 w-10 items-center justify-center text-aegis-textMuted hover:text-aegis-text"
        >
          {visible ? <EyeOff size={16} /> : <Eye size={16} />}
        </button>
      </div>
      {error && (
        <p id={`${inputId}-error`} className="text-xs text-aegis-coral">
          {error}
        </p>
      )}
      {!error && hint && (
        <p id={`${inputId}-hint`} className="text-xs text-aegis-textFaint">
          {hint}
        </p>
      )}
    </div>
  );
});
PasswordInput.displayName = "PasswordInput";
