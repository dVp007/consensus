# Architecture

## Flow

```
Organizer creates plan ──► invite link ──► members join
                                               │
            ┌──────────────────────────────────┘
            ▼
   Each member: private chat with INTERVIEWER agent
      tool calls: save_constraint(...), finish_interview()
            │  writes Constraint rows (private to that member)
            ▼
   Organizer clicks "Generate options"
            ▼
   PLANNER agent (background task)
      1. load constraints, anonymize as P1..Pn (shuffled)
      2. LLM -> 3 proposals as JSON (validated with Pydantic)
      3. scoring.score_proposal()   deterministic fit score
      4. privacy.find_leaks()       block anything revealing who said what
      5. save proposals, status -> voting
            ▼
   Members vote (1-3) ──► tally ──► status -> decided

   WebSocket room per plan pushes: member_joined, interview_done,
   status_changed, agent_step, vote_cast  (never private content)
```

## Data model

| Table | Key fields | Visibility |
|---|---|---|
| plans | title, description, status, invite_code | all members |
| members | display_name, role, token_hash, interview_done | public fields to members; token_hash never |
| messages | member_id, role, content | owner only |
| constraints | member_id, category, summary, value (JSON), is_hard | owner only; planner sees anonymized |
| proposals | round, title, summary, details, tradeoffs, fit_score | all members |
| votes | proposal_id, member_id, score | tallies only |

## Plan status machine

`gathering` → `proposing` → `voting` → `decided`
(`proposing` → `gathering` again if the planner fails.)

## API

| Method | Path | Who | Status |
|---|---|---|---|
| POST | /api/plans | anyone | done |
| GET | /api/invites/{code} | anyone | done |
| POST | /api/invites/{code}/join | anyone | done |
| GET | /api/plans/{id} | member | done |
| GET | /api/plans/{id}/me | member | done |
| GET | /api/plans/{id}/chat | member (own) | done |
| POST | /api/plans/{id}/chat | member | **Week 2** |
| GET | /api/plans/{id}/constraints | member (own) | done |
| POST | /api/plans/{id}/propose | organizer | **Week 3** |
| GET | /api/plans/{id}/proposals | member | done |
| PUT | /api/proposals/{id}/vote | member | **Week 4** |
| GET | /api/plans/{id}/tally | member | **Week 4** |
| WS | /ws/plans/{id}?token= | member | done |

## Design decisions worth explaining in interviews

1. **Token-per-plan auth instead of accounts.** Joining with just a name keeps friction low
   (people won't sign up to pick a restaurant). Tokens are random, returned once, stored hashed.
2. **The LLM never grades itself.** Fit scores come from tested Python.
3. **Privacy is enforced in code, not just the prompt.** Prompts ask the planner to stay
   anonymous; `privacy.py` verifies it.
4. **Agent runs outside the request.** Planning takes a while, so the endpoint returns 202
   and progress streams over the WebSocket.
5. **Step limits on every agent loop** so a confused model can't loop forever or burn money.
