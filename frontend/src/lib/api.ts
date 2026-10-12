import { getToken } from "./session";
import type { Message, Plan, Proposal, SessionOut } from "./types";

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}

async function request<T>(path: string, init: RequestInit = {}, planId?: string): Promise<T> {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  const token = planId ? getToken(planId) : null;
  if (token) headers.Authorization = `Bearer ${token}`;

  const res = await fetch(`/api${path}`, { ...init, headers: { ...headers, ...init.headers } });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new ApiError(res.status, body.detail ?? res.statusText);
  }
  return res.status === 204 ? (undefined as T) : res.json();
}

export const api = {
  createPlan: (title: string, description: string, organizer_name: string) =>
    request<SessionOut>("/plans", { method: "POST", body: JSON.stringify({ title, description, organizer_name }) }),

  previewInvite: (code: string) => request<Plan>(`/invites/${code}`),

  joinPlan: (code: string, display_name: string) =>
    request<SessionOut>(`/invites/${code}/join`, { method: "POST", body: JSON.stringify({ display_name }) }),

  getPlan: (planId: string) => request<Plan>(`/plans/${planId}`, {}, planId),

  getChat: (planId: string) => request<Message[]>(`/plans/${planId}/chat`, {}, planId),

  sendChat: (planId: string, content: string) =>
    request<Message>(`/plans/${planId}/chat`, { method: "POST", body: JSON.stringify({ content }) }, planId),

  startPlanning: (planId: string) => request(`/plans/${planId}/propose`, { method: "POST" }, planId),

  getProposals: (planId: string) => request<Proposal[]>(`/plans/${planId}/proposals`, {}, planId),

  vote: (planId: string, proposalId: string, score: 1 | 2 | 3) =>
    request<void>(`/proposals/${proposalId}/vote`, { method: "PUT", body: JSON.stringify({ score }) }, planId),
};
