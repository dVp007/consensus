import { useQuery } from "@tanstack/react-query";
import { api } from "../lib/api";

/**
 * The member's PRIVATE chat with the interviewer agent.
 *
 * Already done: loading history.
 * TODO (Week 2):
 *   - Input box + send button calling api.sendChat (use useMutation from react-query).
 *   - Optimistic UI: show the user's message immediately, a typing indicator while waiting.
 *   - Auto-scroll to the newest message.
 *   - A "Private" badge in the header so people trust it ("Only the agent sees this").
 * TODO (Week 3, stretch): stream tokens via SSE instead of waiting for the full reply.
 * TODO (Week 4): side panel listing "What I understood about you" (GET /constraints),
 *   with a way to delete a wrong one.
 */
export default function ChatPanel({ planId }: { planId: string }) {
  const chat = useQuery({ queryKey: ["chat", planId], queryFn: () => api.getChat(planId) });

  return (
    <div className="flex h-[70vh] flex-col rounded-xl border border-stone-200 bg-white">
      <header className="border-b border-stone-200 px-4 py-3">
        <p className="font-medium">Your private chat</p>
        <p className="text-xs text-stone-500">Only the planning agent sees this. The group never sees your answers.</p>
      </header>

      <div className="flex-1 space-y-3 overflow-y-auto p-4">
        {chat.data?.length === 0 && (
          <p className="text-sm text-stone-500">Say hi to start. The agent will ask about your budget, dates and must-haves.</p>
        )}
        {chat.data?.map((m) => (
          <div
            key={m.id}
            className={`max-w-[80%] rounded-lg px-3 py-2 text-sm ${
              m.role === "user" ? "ml-auto bg-stone-900 text-white" : "bg-stone-100"
            }`}
          >
            {m.content}
          </div>
        ))}
      </div>

      <footer className="border-t border-stone-200 p-3 text-sm text-stone-400">
        TODO: message input (see comment at the top of ChatPanel.tsx)
      </footer>
    </div>
  );
}
