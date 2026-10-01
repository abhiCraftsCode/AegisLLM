import type { WeekSchema } from "@/types/api";
import { formatShortDate } from "@/lib/utils";

export function ActivityChart({ week }: { week: WeekSchema }) {
  const max = Math.max(1, ...week.days.map((d) => d.total_requests));

  return (
    <div>
      <div className="flex h-52 items-end gap-2 sm:gap-3">
        {week.days.map((day) => {
          const totalHeight = (day.total_requests / max) * 100;
          const blockedHeight = (day.blocked_requests / max) * 100;
          return (
            <div key={day.date} className="flex flex-1 flex-col items-center gap-2">
              <div className="relative flex h-40 w-full max-w-[36px] items-end justify-center rounded-md bg-white/[0.03]">
                <div
                  className="w-full rounded-md bg-aegis-cyan/25 transition-all"
                  style={{ height: `${totalHeight}%` }}
                  title={`${day.total_requests} requests`}
                />
                <div
                  className="absolute bottom-0 w-full rounded-md bg-aegis-coral/70 transition-all"
                  style={{ height: `${blockedHeight}%` }}
                  title={`${day.blocked_requests} blocked`}
                />
              </div>
              <span className="text-[10px] text-aegis-textFaint">{formatShortDate(day.date)}</span>
            </div>
          );
        })}
      </div>
      <div className="mt-4 flex items-center gap-4 text-xs text-aegis-textMuted">
        <span className="flex items-center gap-1.5">
          <span className="h-2 w-2 rounded-sm bg-aegis-cyan/50" /> Total requests
        </span>
        <span className="flex items-center gap-1.5">
          <span className="h-2 w-2 rounded-sm bg-aegis-coral/70" /> Blocked requests
        </span>
      </div>
    </div>
  );
}
