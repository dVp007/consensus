import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../lib/api";
import { saveToken } from "../lib/session";

export default function HomePage() {
  const navigate = useNavigate();
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [name, setName] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      const session = await api.createPlan(title, description, name);
      saveToken(session.plan.id, session.member_token);
      navigate(`/plans/${session.plan.id}`);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="mx-auto max-w-lg px-4 py-16">
      <h1 className="text-3xl font-semibold tracking-tight">Consensus</h1>
      <p className="mt-2 text-stone-600">
        Plan anything with a group. Everyone tells the agent what they want, privately. It finds the options that work
        for all of you.
      </p>

      <form onSubmit={onSubmit} className="mt-8 space-y-4 rounded-xl border border-stone-200 bg-white p-6">
        <label className="block">
          <span className="text-sm font-medium">What are you planning?</span>
          <input
            required
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Weekend trip for 6 in November"
            className="mt-1 w-full rounded-lg border border-stone-300 px-3 py-2"
          />
        </label>
        <label className="block">
          <span className="text-sm font-medium">Details (optional)</span>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={3}
            className="mt-1 w-full rounded-lg border border-stone-300 px-3 py-2"
          />
        </label>
        <label className="block">
          <span className="text-sm font-medium">Your name</span>
          <input
            required
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="mt-1 w-full rounded-lg border border-stone-300 px-3 py-2"
          />
        </label>
        {error && <p className="text-sm text-red-600">{error}</p>}
        <button
          disabled={busy}
          className="w-full rounded-lg bg-stone-900 px-4 py-2 font-medium text-white disabled:opacity-50"
        >
          {busy ? "Creating…" : "Create plan"}
        </button>
      </form>
    </main>
  );
}
