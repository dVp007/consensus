import { useState } from "react";
import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { api } from "../lib/api";
import { getToken } from "../lib/session";
import { usePlanSocket } from "../hooks/usePlanSocket";
import ChatPanel from "../components/ChatPanel";
import ProposalsPanel from "../components/ProposalsPanel";

export default function PlanRoomPage() {
  const { planId = "" } = useParams();
  const [agentSteps, setAgentSteps] = useState<string[]>([]);
  const plan = useQuery({ queryKey: ["plan", planId], queryFn: () => api.getPlan(planId), enabled: !!getToken(planId) });

  // Live updates: anything that changes the plan just triggers a refetch.
  usePlanSocket(planId, (event) => {
    if (event.type === "agent_step") setAgentSteps((s) => [...s, event.step]);
    else plan.refetch();
  });

  if (!getToken(planId)) return <p className="p-8">You're not a member of this plan. Ask for an invite link.</p>;
  if (plan.isLoading) return <p className="p-8">Loading…</p>;
  if (plan.isError) return <p className="p-8 text-red-600">{(plan.error as Error).message}</p>;

  const p = plan.data!;
  const inviteUrl = `${location.origin}/join/${p.invite_code}`;
  const done = p.members.filter((m) => m.interview_done).length;

  return (
    <main className="mx-auto grid max-w-6xl gap-6 px-4 py-8 lg:grid-cols-[280px_1fr]">
      <aside className="space-y-6">
        <div>
          <h1 className="text-xl font-semibold">{p.title}</h1>
          <span className="mt-1 inline-block rounded-full bg-stone-200 px-2 py-0.5 text-xs">{p.status}</span>
        </div>

        <div className="rounded-xl border border-stone-200 bg-white p-4">
          <p className="text-sm font-medium">Invite link</p>
          <div className="mt-2 flex gap-2">
            <input readOnly value={inviteUrl} className="min-w-0 flex-1 rounded border px-2 py-1 text-xs" />
            <button onClick={() => navigator.clipboard.writeText(inviteUrl)} className="rounded border px-2 text-xs">
              Copy
            </button>
          </div>
        </div>

        <div className="rounded-xl border border-stone-200 bg-white p-4">
          <p className="text-sm font-medium">
            Members · {done}/{p.members.length} ready
          </p>
          <ul className="mt-2 space-y-1">
            {p.members.map((m) => (
              <li key={m.id} className="flex items-center justify-between text-sm">
                <span>
                  {m.display_name}
                  {m.role === "organizer" && <span className="ml-1 text-xs text-stone-500">(organizer)</span>}
                </span>
                <span className={m.interview_done ? "text-green-700" : "text-stone-400"}>
                  {m.interview_done ? "ready" : "chatting"}
                </span>
              </li>
            ))}
          </ul>
          {/* TODO (Week 3): show a "Generate options" button for the organizer that calls
              api.startPlanning(planId). Fetch /plans/{id}/me to know if you're the organizer. */}
        </div>

        {agentSteps.length > 0 && (
          <div className="rounded-xl border border-stone-200 bg-white p-4 text-sm">
            <p className="font-medium">Agent progress</p>
            <ol className="mt-2 list-decimal space-y-1 pl-4 text-stone-600">
              {agentSteps.map((s, i) => (
                <li key={i}>{s}</li>
              ))}
            </ol>
          </div>
        )}
      </aside>

      <section>{p.status === "gathering" ? <ChatPanel planId={planId} /> : <ProposalsPanel planId={planId} />}</section>
    </main>
  );
}
