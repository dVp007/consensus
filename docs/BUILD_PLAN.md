# Build plan

Six weeks at roughly 8-10 hours a week. Each week ends with something you can demo.
Commit small and often; a steady commit history looks great on GitHub.

---

## Week 1 — Get it running and learn the codebase

Already working: create plan, invite link, join, live member list, WebSocket room.

- [ ] Run backend and frontend (README). Open http://localhost:8000/docs and try every endpoint.
- [ ] Create a plan, join from an incognito window, watch the member list update live.
- [ ] Read `models.py`, `auth.py`, `routers/plans.py`. Make sure you can explain why
      `schemas.MemberPublic` exists separately from `models.Member`.
- [ ] Get an OpenRouter key, pick a tool-calling model, and make one test call to
      `agents/llm.complete()` from a Python shell.
- [ ] Push to GitHub. Add a GitHub Actions workflow that runs `pytest` and `npm run build`.

**Demo:** two browsers, one plan, live member list.

## Week 2 — The interviewer agent (the core agent loop)

- [ ] `interviewer.execute_tool()`: handle `save_constraint` and `finish_interview`.
- [ ] `interviewer.run_turn()`: the tool loop described in the file's docstring.
      Respect `agent_max_steps`. Handle bad JSON arguments by returning an error to the model.
- [ ] `POST /plans/{id}/chat`: save messages, call `run_turn`, broadcast `interview_done`.
- [ ] `ChatPanel.tsx`: input box, `useMutation`, optimistic message, typing indicator, autoscroll.
- [ ] Tests: mock `llm.complete` to return a fake tool call and check a Constraint row is saved.
      (Never hit the real API in tests.)

**Demo:** chat with the agent; it asks good questions, and constraints appear in the DB.

## Week 3 — The planner agent and live progress

- [ ] `services/scoring.score_proposal()`: start with budget, then dates. Make `test_scoring.py` pass.
- [ ] `planner.run_planner()`: anonymize → LLM JSON → validate → score → save. Broadcast
      `agent_step` events between stages.
- [ ] `POST /plans/{id}/propose` with `BackgroundTasks`.
- [ ] Organizer-only "Generate options" button; agent progress list already renders in PlanRoom.
- [ ] WebSocket reconnect with backoff in `usePlanSocket`.

**Demo:** 3 people finish interviews, organizer clicks generate, everyone sees progress, then options.

## Week 4 — Privacy guard and voting

- [ ] `privacy.find_leaks()`: make `test_privacy.py` pass. Run it inside the planner and
      regenerate (once) or redact if something leaks.
- [ ] Voting endpoint + tally with a GROUP BY. Status → `decided` when everyone has voted.
- [ ] `ProposalsPanel.tsx`: vote buttons, live tally bars, winner banner.
- [ ] "What I understood about you" panel in chat, with delete for wrong constraints.

**Demo:** full loop from invite to decision.

## Week 5 — Make it production-quality

- [ ] Alembic migrations instead of `create_all`.
- [ ] Switch to Postgres (`docker compose up -d db`).
- [ ] `agent_runs` table: model, tokens, latency, cost per call. Simple trace viewer page.
- [ ] **Eval suite** (`backend/evals/`): 15-20 scripted groups (e.g. "4 friends, one vegan,
      budgets $100-$600, two date windows that barely overlap"). Measure: % of proposals
      satisfying all hard constraints, privacy leaks, cost and latency per plan.
      Put the numbers in the README.
- [ ] Rate limiting on chat endpoint; max members per plan.

## Week 6 — Ship it

- [ ] Deploy: backend on Render/Railway/Fly.io, frontend on Vercel/Netlify, managed Postgres.
      (In production, set `FRONTEND_ORIGIN` and point the frontend at the backend URL.)
- [ ] README: screenshots, 30-60s demo GIF, architecture diagram, eval results table.
- [ ] Record a 2-minute walkthrough video.
- [ ] Optional stretch: planner tools with real data (places search, weather), streaming
      chat over SSE, Redis pub/sub so WebSockets work across multiple server instances,
      a "re-plan" round using vote feedback.

---

## Resume bullet (fill in your real numbers)

> Built **Consensus**, a multiplayer AI planning app (React, TypeScript, FastAPI, PostgreSQL,
> WebSockets) where per-user interviewer agents gather private constraints via tool calling
> and a planner agent proposes group options; added deterministic fit scoring and an
> automated privacy guard, reaching **X%** hard-constraint satisfaction with **0** leaks
> across a **N**-scenario eval suite at **$Y** per plan.
