import { useQuery } from "@tanstack/react-query";
import { api } from "../lib/api";

/**
 * Shows the planner's options once status is "proposing" / "voting" / "decided".
 *
 * Already done: listing proposals.
 * TODO (Week 4):
 *   - Three vote buttons per card (No / OK / Love it) calling api.vote; highlight your choice.
 *   - Live tally bars (GET /plans/{id}/tally), refreshed on "vote_cast" socket events.
 *   - A "decided" banner with the winner when status === "decided".
 *   - While status === "proposing", show a skeleton/loading state instead of an empty list.
 */
export default function ProposalsPanel({ planId }: { planId: string }) {
  const proposals = useQuery({ queryKey: ["proposals", planId], queryFn: () => api.getProposals(planId) });

  if (proposals.data?.length === 0) {
    return <p className="text-stone-500">The agent is putting options together…</p>;
  }

  return (
    <div className="grid gap-4 md:grid-cols-2">
      {proposals.data?.map((p) => (
        <article key={p.id} className="rounded-xl border border-stone-200 bg-white p-4">
          <div className="flex items-start justify-between gap-2">
            <h3 className="font-semibold">{p.title}</h3>
            <span className="rounded-full bg-green-100 px-2 py-0.5 text-xs text-green-800">{p.fit_score}% fit</span>
          </div>
          <p className="mt-2 text-sm text-stone-700">{p.summary}</p>
          {p.tradeoffs.length > 0 && (
            <ul className="mt-3 list-disc space-y-1 pl-4 text-xs text-stone-500">
              {p.tradeoffs.map((t, i) => (
                <li key={i}>{t}</li>
              ))}
            </ul>
          )}
        </article>
      ))}
    </div>
  );
}
