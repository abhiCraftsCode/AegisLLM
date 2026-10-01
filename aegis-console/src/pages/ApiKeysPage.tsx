import { useCallback, useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { Plus } from "lucide-react";
import { PageHeader } from "@/components/common/PageHeader";
import { EmptyState } from "@/components/common/EmptyState";
import { ErrorState } from "@/components/common/ErrorState";
import { Pagination } from "@/components/common/Pagination";
import { Skeleton } from "@/components/ui/Skeleton";
import { Button } from "@/components/ui/Button";
import { ApiKeyList } from "@/features/api-keys/ApiKeyList";
import { CreateKeyDialog } from "@/features/api-keys/CreateKeyDialog";
import { KeyCreatedDialog } from "@/features/api-keys/KeyCreatedDialog";
import { ApiKeyDetailDialog } from "@/features/api-keys/ApiKeyDetailDialog";
import { EditKeyDialog } from "@/features/api-keys/EditKeyDialog";
import { RevokeKeyDialog } from "@/features/api-keys/RevokeKeyDialog";
import { apiKeysApi } from "@/features/api-keys/api";
import { ApiError } from "@/lib/api";
import { DEFAULT_PAGE_SIZE } from "@/lib/constants";
import type { GenerateResponse, KeySchema, PageResponse } from "@/types/api";

export default function ApiKeysPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const page = Math.max(1, Number(searchParams.get("page") ?? "1"));

  const [data, setData] = useState<PageResponse<KeySchema> | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [createOpen, setCreateOpen] = useState(false);
  const [createdResult, setCreatedResult] = useState<GenerateResponse | null>(null);
  const [selectedKey, setSelectedKey] = useState<KeySchema | null>(null);
  const [editingKey, setEditingKey] = useState<KeySchema | null>(null);
  const [revokingKey, setRevokingKey] = useState<KeySchema | null>(null);

  const load = useCallback(
    async (targetPage: number) => {
      setLoading(true);
      setError(null);
      try {
        const res = await apiKeysApi.list(targetPage, DEFAULT_PAGE_SIZE);
        setData(res);
      } catch (err) {
        setError(err instanceof ApiError ? err.message : "Couldn't load API keys.");
      } finally {
        setLoading(false);
      }
    },
    []
  );

  useEffect(() => {
    load(page);
  }, [page, load]);

  function goToPage(p: number) {
    setSearchParams((prev) => {
      const next = new URLSearchParams(prev);
      next.set("page", String(p));
      return next;
    });
  }

  async function refetchAfterRevoke() {
    setRevokingKey(null);
    setSelectedKey(null);
    // If this was the last item on the last page, step back a page.
    if (data && data.items.length === 1 && data.page > 1) {
      goToPage(data.page - 1);
    } else {
      load(page);
    }
  }

  return (
    <div>
      <PageHeader
        title="API Keys"
        description="Manage the keys used to access your AegisLLM gateway."
        actions={
          <Button size="sm" onClick={() => setCreateOpen(true)}>
            <Plus size={15} /> Create API Key
          </Button>
        }
      />

      {loading && (
        <div className="space-y-2">
          {Array.from({ length: 4 }).map((_, i) => (
            <Skeleton key={i} className="h-[72px]" />
          ))}
        </div>
      )}

      {!loading && error && <ErrorState message={error} onRetry={() => load(page)} />}

      {!loading && !error && data && data.items.length === 0 && (
        <EmptyState
          title="No API keys yet"
          description="Create your first gateway key to connect an application."
          action={<Button size="sm" onClick={() => setCreateOpen(true)}>Create API Key</Button>}
        />
      )}

      {!loading && !error && data && data.items.length > 0 && (
        <div className="flex flex-col gap-4">
          <ApiKeyList keys={data.items} onSelect={setSelectedKey} />
          <Pagination page={data.page} pages={data.pages} total={data.total} onPageChange={goToPage} />
        </div>
      )}

      <CreateKeyDialog
        open={createOpen}
        onClose={() => setCreateOpen(false)}
        onCreated={(result) => {
          setCreateOpen(false);
          setCreatedResult(result);
        }}
      />

      {createdResult && (
        <KeyCreatedDialog
          result={createdResult}
          onDone={() => {
            setCreatedResult(null);
            load(page);
          }}
        />
      )}

      {selectedKey && !editingKey && !revokingKey && (
        <ApiKeyDetailDialog
          keyRecord={selectedKey}
          onClose={() => setSelectedKey(null)}
          onEdit={() => setEditingKey(selectedKey)}
          onRevoke={() => setRevokingKey(selectedKey)}
        />
      )}

      {editingKey && (
        <EditKeyDialog
          keyRecord={editingKey}
          onClose={() => setEditingKey(null)}
          onUpdated={() => {
            setEditingKey(null);
            setSelectedKey(null);
            load(page);
          }}
        />
      )}

      {revokingKey && (
        <RevokeKeyDialog keyRecord={revokingKey} onClose={() => setRevokingKey(null)} onRevoked={refetchAfterRevoke} />
      )}
    </div>
  );
}
