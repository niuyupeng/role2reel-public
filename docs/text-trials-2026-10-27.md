# Public text trials · 2026-10-27

Four synthetic requests were actually completed by two independent execution agents: one completed A/B against the public baseline, another completed C/D after the routing refactor. The agents received the user requests and public skill, not expected outputs or other trial results. They read only relevant public references. The coordinating agent then reviewed the returned text against the explicit constraints; this review was not a blinded human evaluation.

The outputs linked below are preserved verbatim beneath their input sections. Only the public page wrapper was added. Source paths, local host details and private project records are excluded.

| Case | Input/output | Source | Coordinating review |
|---|---|---|---|
| A | [12-second story, two full segment prompts](examples/camera-segments.md) | Baseline `821a6f5` | Two 8-second footage plans; two 6-second trims; original line and key ownership retained; action precedes reaction; files correctly marked unavailable |
| B | [Postal worker, three possible pasts](examples/life-paths.md) | Baseline `821a6f5` | Three distinct proposed motives; uncertainties visible; author chooses; no biography, ranking or canon lock |
| C | [English three-shot board](examples/compact-board.md) | Refactored entrypoint, hash below | Exactly three rows totaling 9 seconds; both repeated lines preserved with original speakers; no invented asset bindings or new approval process |
| D | [Short revisable character draft](examples/character-draft.md) | Refactored entrypoint, hash below | One paragraph, 150 Unicode characters including punctuation/label, 133 Han characters; text-only draft with revisable additions; no visual asset pack or canon claim |

## Read-time source identity

A/B used commit `821a6f5b443b05912fd175b307f9f79fec68c1ee`. C/D captured the entrypoint SHA-256 immediately before reading it: `ca12e658b103455f4c2c764c011cd3cd5a3f02bbf9fac2e26bb944950dea2f97`. That read-time digest identifies the Windows CRLF bytes. The same entrypoint normalized to LF, as distributed by Git, has SHA-256 `6a1e4ce6429a28f4292a491802f9f572402464630af4afca2ab2a6971a8bf664`. Their relevant storyboard/atomic-shot references already included the compact-contract corrections. Packaging and onboarding work continued separately; the text cases do not certify every later documentation byte.

Model settings were inherited from the executing Codex session and were not independently captured as a reproducible API configuration. These observations therefore are not a comparative model benchmark. Four different inputs and two agents are not four independent repeated trials of one task.

## Review limits and unresolved questions

- A's lens, aperture, distance and blocking choices are proposed production settings. No identity or room photos were supplied; camera-to-scene fit is not verified. No generator was chosen, so multi-shot and 8-second provider support is not established.
- C's 9-second schedule is not a rehearsed performance. The discussion board protects the repeated joke but has not been judged by an audience.
- B/D preserve fictional proposal status, but psychological depth, author preference and originality were not measured. Short draft success is not evidence that the deep-biography pipeline has passed.
- No image, audio, Word rendering or video output was generated in these trials. There is no new evidence for visual realism, lip sync, acting, platform success or production adoption.
- No hard-constraint failures were identified in these four text outputs by the coordinating review. That is a small observed sample, not a success-rate claim. The historical and pending cases in [EVALS](../EVALS.md) retain their own status; these runs do not mark old case IDs passed.

## Output fingerprints

These hashes apply to the original UTF-8 output text with LF line endings, before the public input/page wrapper. They identify recorded text, not its artistic quality.

```json
[
  {
    "case": "A",
    "source_revision": "821a6f5b443b05912fd175b307f9f79fec68c1ee",
    "output_text_sha256_lf": "118ecc8e58fcf196c8d327558acca7cd08aabee252c3f0cc1753da6850fd76ee"
  },
  {
    "case": "B",
    "source_revision": "821a6f5b443b05912fd175b307f9f79fec68c1ee",
    "output_text_sha256_lf": "f2b5b2bf305363ab033b7f9bd420110026b976c4c09775422231588a97a1b762"
  },
  {
    "case": "C",
    "source_revision": "entrypoint SHA-256 ca12e658b103455f4c2c764c011cd3cd5a3f02bbf9fac2e26bb944950dea2f97",
    "output_text_sha256_lf": "49c997ba50b60c7757c5e4517c962296699fc72cb51da048081f8e2e03e9df0b"
  },
  {
    "case": "D",
    "source_revision": "entrypoint SHA-256 ca12e658b103455f4c2c764c011cd3cd5a3f02bbf9fac2e26bb944950dea2f97",
    "output_text_sha256_lf": "2e44e4f0a529cf561ea9b1b3f1013b24622ad018b176a444f7494abcb644d3ca"
  }
]
```
