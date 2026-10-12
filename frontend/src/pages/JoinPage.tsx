import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { api } from "../lib/api";
import { saveToken } from "../lib/session";

export default function JoinPage() {
  const { inviteCode = "" } = useParams();
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [error, setError] = useState<string | null>(null);

  const invite = useQuery({ queryKey: ["invite", inviteCode], queryFn: () => api.previewInvite(inviteCode) });

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    try {
      const session = await api.joinPlan(inviteCode, name);
      saveToken(session.plan.id, session.member_token);
      navigate(`/plans/${session.plan.id}`);
    } catch (err) {
      setError((err as Error).message);
    }
  }

  if (invite.isLoading) return <p className="p-8">Loading…</p>;
  if (invite.isError) return <p className="p-8 text-red-600">This invite link isn't valid.</p>;

  return (
    <main className="mx-auto max-w-lg px-4 py-16">
      <p className="text-sm text-stone-500">You're invited to plan</p>
      <h1 className="text-2xl font-semibold">{invite.data!.title}</h1>
      <form onSubmit={onSubmit} className="mt-6 flex gap-2">
        <input
          required
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Your name"
          className="flex-1 rounded-lg border border-stone-300 px-3 py-2"
        />
        <button className="rounded-lg bg-stone-900 px-4 py-2 font-medium text-white">Join</button>
      </form>
      {error && <p className="mt-2 text-sm text-red-600">{error}</p>}
    </main>
  );
}
