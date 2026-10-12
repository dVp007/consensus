# Consensus

**A multiplayer AI agent that plans things for groups.**

Most AI assistants serve one person. Consensus serves a group. An organizer creates a plan
("weekend trip for 6", "team offsite", "where should we eat Friday?") and shares a link.
The agent then talks to each member **privately** to learn their budget, dates and
dealbreakers, proposes options that balance everyone's constraints, explains the
trade-offs without revealing who wanted what, and runs a group vote.

> Status: early development. See [docs/BUILD_PLAN.md](docs/BUILD_PLAN.md) for the roadmap.

## Why it's interesting

- **Private input, shared output.** People share a tight budget or a dietary need with the
  agent that they'd never post in the group chat. The planner only sees anonymized
  constraints, and a privacy guard checks every proposal for leaks.
- **Two cooperating agents.** An *interviewer* (tool-calling chat loop, one per member)
  turns conversation into structured constraints; a *planner* turns everyone's constraints
  into options.
- **Deterministic where it matters.** The LLM proposes; plain Python scores how well each
  option fits everyone's hard constraints.
- **Real-time multiplayer.** WebSockets push joins, readiness, agent progress and votes.

## Stack

| Layer | Tech |
|---|---|
| Frontend | React 18, TypeScript, Vite, Tailwind CSS v4, TanStack Query, React Router |
| Backend | Python, FastAPI, SQLAlchemy 2, Pydantic v2, WebSockets |
| Database | SQLite (dev) / PostgreSQL |
| LLM | [OpenRouter](https://openrouter.ai) via the OpenAI SDK (any tool-calling model) |
| Tests | pytest |

## Getting started

### 1. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                 # then add your OpenRouter key and model
uvicorn app.main:app --reload        # http://localhost:8000/docs
```

Run tests with `pytest`. Tests for features you haven't built yet show as `xfail`.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev                          # http://localhost:5173
```

The Vite dev server proxies `/api` and `/ws` to the backend.

### 3. Try it

Create a plan, copy the invite link, open it in a private/incognito window and join as a
second person. The member list updates live in both windows.

### Choosing a model

Get a key at [openrouter.ai/keys](https://openrouter.ai/keys). On
[openrouter.ai/models](https://openrouter.ai/models), filter by **Tools** support and copy
the model id into `LLM_MODEL`. Free variants (ending in `:free`) are fine for development
but rate limited, and some handle tool calls poorly, so test a few.

## Project structure

```
backend/
  app/
    main.py            FastAPI app, CORS, routers
    config.py          settings from env
    db.py, models.py   SQLAlchemy schema (plans, members, messages, constraints, proposals, votes)
    schemas.py         API shapes (never expose private fields)
    auth.py            per-plan member tokens
    realtime.py        WebSocket rooms per plan
    routers/           plans (done), chat, proposals, ws
    agents/
      llm.py           OpenRouter client (done)
      prompts.py       system prompts
      tools.py         tool schemas for the interviewer
      interviewer.py   private chat agent loop      <- you build
      planner.py       group proposal agent         <- you build
      privacy.py       leak detection               <- you build
    services/scoring.py  deterministic fit score    <- you build
  tests/
frontend/src/
  pages/               Home (create), Join, PlanRoom
  components/          ChatPanel, ProposalsPanel    <- you finish
  hooks/usePlanSocket.ts
  lib/                 api client, types, session
docs/
  ARCHITECTURE.md
  BUILD_PLAN.md
```

## License

MIT
