// Mirrors backend/app/schemas.py. Stretch: generate these from FastAPI's OpenAPI schema
// with `openapi-typescript` so they can never drift.

export type PlanStatus = "gathering" | "proposing" | "voting" | "decided";

export interface Member {
  id: string;
  display_name: string;
  role: "organizer" | "member";
  interview_done: boolean;
}

export interface Plan {
  id: string;
  title: string;
  description: string;
  status: PlanStatus;
  invite_code: string;
  created_at: string;
  members: Member[];
}

export interface SessionOut {
  plan: Plan;
  member: Member;
  member_token: string;
}

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  created_at: string;
}

export interface Proposal {
  id: string;
  round: number;
  title: string;
  summary: string;
  details: Record<string, unknown>;
  tradeoffs: string[];
  fit_score: number;
}

export type PlanEvent =
  | { type: "member_joined"; member: Member }
  | { type: "interview_done"; member_id: string }
  | { type: "status_changed"; status: PlanStatus }
  | { type: "agent_step"; step: string }
  | { type: "planner_failed" }
  | { type: "vote_cast"; proposal_id: string };
