import { ChevronLeft, ChevronRight } from "lucide-react";
import { Button } from "@/components/ui/Button";

export function Pagination({
  page,
  pages,
  total,
  onPageChange,
}: {
  page: number;
  pages: number;
  total: number;
  onPageChange: (page: number) => void;
}) {
  if (pages <= 1) return null;

  return (
    <div className="flex flex-col items-center justify-between gap-3 border-t border-aegis-border pt-4 sm:flex-row">
      <p className="text-xs text-aegis-textFaint">
        Page {page} of {pages} · {total} total
      </p>
      <div className="flex items-center gap-2">
        <Button
          variant="secondary"
          size="sm"
          onClick={() => onPageChange(page - 1)}
          disabled={page <= 1}
          aria-label="Previous page"
        >
          <ChevronLeft size={15} />
          Prev
        </Button>
        <Button
          variant="secondary"
          size="sm"
          onClick={() => onPageChange(page + 1)}
          disabled={page >= pages}
          aria-label="Next page"
        >
          Next
          <ChevronRight size={15} />
        </Button>
      </div>
    </div>
  );
}
