import { useState } from "react";
import { PageHeader } from "@/components/common/PageHeader";
import { CodeBlock } from "@/components/common/CodeBlock";
import { cn } from "@/lib/utils";
import {
  integrationMethods,
  type ContentBlock,
  type IntegrationMethodId,
} from "@/features/integrations/content";

export default function IntegrationsPage() {
  const [selected, setSelected] = useState<IntegrationMethodId>("rest");
  const method =
    integrationMethods.find((m) => m.id === selected) ?? integrationMethods[0];

  return (
    <div>
      <PageHeader
        title="Integrate AegisLLM"
        description="Connect AegisLLM to your application using the method that fits your stack."
      />

      <div
        role="radiogroup"
        aria-label="Integration method"
        className="mb-6 flex flex-wrap gap-2 rounded-xl border border-aegis-border bg-aegis-surface/50 p-1.5"
      >
        {integrationMethods.map((m) => (
          <button
            key={m.id}
            role="radio"
            aria-checked={selected === m.id}
            onClick={() => setSelected(m.id)}
            className={cn(
              "min-w-[140px] flex-1 rounded-lg px-3 py-2 text-xs font-medium transition-colors sm:text-sm",
              selected === m.id
                ? "bg-aegis-cyanSoft text-aegis-cyan"
                : "text-aegis-textMuted hover:bg-white/5 hover:text-aegis-text",
            )}
          >
            {m.label}
          </button>
        ))}
      </div>

      <div className="rounded-2xl border border-aegis-border bg-aegis-surface/60 p-5 sm:p-6">
        <h2 className="text-lg font-semibold text-aegis-text">
          {method.label}
        </h2>
        <p className="mt-1.5 text-sm text-aegis-textMuted">{method.overview}</p>

        <div className="mt-6 flex flex-col divide-y divide-aegis-border">
          {method.sections.map((section) => (
            <section
              key={section.heading}
              className="flex flex-col gap-3 py-6 first:pt-0 last:pb-0"
            >
              <h3 className="text-sm font-semibold text-aegis-text">
                {section.heading}
              </h3>
              {section.blocks.map((block, i) => (
                <IntegrationBlock key={i} block={block} />
              ))}
            </section>
          ))}
        </div>
      </div>
    </div>
  );
}

function IntegrationBlock({ block }: { block: ContentBlock }) {
  switch (block.type) {
    case "paragraph":
      return (
        <p className="text-sm leading-relaxed text-aegis-textMuted">
          {block.text}
        </p>
      );
    case "code":
      return (
        <CodeBlock
          code={block.code}
          language={block.language}
          label={block.title}
        />
      );
    case "note":
      return (
        <div className="rounded-lg border border-aegis-amber/25 bg-aegis-amber/10 px-3.5 py-2.5 text-sm text-aegis-amber">
          {block.text}
        </div>
      );
  }
}
