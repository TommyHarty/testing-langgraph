# FastAPI POC Starter

A minimal, dockerised FastAPI starter for building small POCs. Intentionally generic — no LLM frameworks, no databases, no logging setup. Add what you need per POC.

## Structure

```
.
├── app/            # FastAPI app
├── core/           # Config
├── scripts/        # Setup, run, and test scripts
├── tests/          # Pytest tests
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── .env.example
```

## Getting started

```bash
cp .env.example .env
./scripts/setup.sh
```

## Running

Docker is the default runtime.

```bash
./scripts/run.sh
```

Or directly with Docker Compose:

```bash
docker compose up
```

## Testing

```bash
./scripts/test.sh
```

## Teardown

Stops containers, removes networks/volumes, and cleans up built images:

```bash
./scripts/down.sh
```

## Health endpoint

```
GET /health
```

Returns:

```json
{
  "status": "ok",
  "app_name": "FastAPI POC Starter",
  "app_env": "local"
}
```

## Config

Environment variables (see `.env.example`):

| Variable        | Default               | Notes                          |
|-----------------|-----------------------|--------------------------------|
| `APP_NAME`      | `FastAPI POC Starter` |                                |
| `APP_ENV`       | `local`               |                                |
| `API_HOST`      | `0.0.0.0`             |                                |
| `API_PORT`      | `8000`                |                                |
| `OPENAI_API_KEY`| _(empty)_             | Not used by the starter itself |

`OPENAI_API_KEY` is included in config because many POCs will need it. The starter does not depend on or call the OpenAI SDK.

## Local fallback

If Docker is unavailable, the scripts fall back to a local `.venv`. Run `scripts/setup.sh` to create it. This path is secondary — Docker is the canonical runtime.
