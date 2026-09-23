# Limitations

JobFit Agent is an MVP and has known limitations.

## Current Limitations

- Rule-based matching can miss semantic matches that use very different wording.
- Optional LLM parsing depends on user-provided API configuration.
- HTML snapshot parsing is generic and may include noisy page text.
- The default scoring weights are heuristic and should be calibrated with real user feedback.
- The tool does not verify whether resume claims are objectively true; it only checks whether suggestions are grounded in the provided resume text.

## Non-goals

- No auto-apply or mass application behavior.
- No bypassing access controls or anti-bot systems.
- No guarantee that a high score means the user will pass screening or interviews.
