import { useEffect, useRef } from "react";
import type { PlanEvent } from "../lib/types";
import { getToken } from "../lib/session";

/**
 * Subscribes to live events for a plan. Usage:
 *   usePlanSocket(planId, (event) => { if (event.type === "member_joined") refetch(); });
 *
 * TODO (Week 3): reconnect with exponential backoff when the socket drops
 * (close code !== 4401), and show a small "reconnecting..." badge in the UI.
 */
export function usePlanSocket(planId: string | undefined, onEvent: (e: PlanEvent) => void) {
  const handler = useRef(onEvent);
  handler.current = onEvent;

  useEffect(() => {
    if (!planId) return;
    const token = getToken(planId);
    if (!token) return;

    const proto = location.protocol === "https:" ? "wss" : "ws";
    const ws = new WebSocket(`${proto}://${location.host}/ws/plans/${planId}?token=${encodeURIComponent(token)}`);
    ws.onmessage = (msg) => handler.current(JSON.parse(msg.data) as PlanEvent);
    return () => ws.close();
  }, [planId]);
}
