# Contributing

Thanks for your interest in JobFit Agent.

## Development Setup

```bash
git clone https://github.com/sweetheartbaby/jobfit-agent.git
cd jobfit-agent

python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Run Tests

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

## Add a New Job Connector

1. Create a loader under `src/jobfit_agent/connectors/`.
2. Convert external data into the common `Job` schema.
3. Add detection logic in `src/jobfit_agent/workflow.py`.
4. Add example data under `examples/`.
5. Add tests under `tests/`.

## Safety Rules

- Do not add code that bypasses access controls.
- Do not collect private data without user authorization.
- Do not implement mass job application behavior.
- Resume tailoring must stay evidence-grounded and should not invent experience.
