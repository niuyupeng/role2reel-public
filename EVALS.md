# Role2Reel evaluation status

## Production-readiness revision — 2026-10-27, version 2026.10.27.4

[Three rounds of complex text trials](docs/complex-trials-2026-10-27.md) retain nine complete responses to seven synthetic requests, including fresh repeats of the multi-person handoff and locked APS-C enrichment. The coordinator and a separate model reviewer found no hard constraint failure in these nine outputs. One deliberately infeasible request is correctly left unfinished with its exact conflict explained; it is not counted as a successfully generated two-second clip. The record includes complete inputs/outputs, source commit, read-reference hashes, assumptions and review limits. Model identifiers/settings were not exposed and remain unknown. This is not a cross-model benchmark, blinded human review or evidence of media quality.

English installation, updates/rollback, optional tools and actual production usage are now documented end to end. Release tooling binds VERSION, tag and exact Git commit, builds a deterministic allowlisted archive with manifests/checksums, verifies uploaded assets before publishing and refuses to replace differing released bytes. The checked installer preserves previous versions outside the skill discovery directory and refuses edited or unmanaged installations. A real Windows redirected-output failure on Chinese backup paths was reproduced, fixed and independently rerun successfully; ordinary generated Python caches no longer incorrectly block updates.

Local Windows Python 3.11: **263 tests discovered, 257 passed, 6 skipped** because local symbolic-link creation was unavailable. Windows junction refusal and archive symlink rejection passed. Repository validation and export privacy audit cover **192 allowlisted files**; the verified release adds one generated `.release.json` metadata member. The nine published request/response fingerprints were independently recalculated. The tag workflow runs its four Windows/Ubuntu × Python 3.11/3.13 jobs before publication; the actual workflow run and attached release identify the published result. Earlier counts below are historical.

The first hosted Windows run also exposed an 8.3 short-path alias mismatch in the release builder. It now resolves the repository root consistently before member comparison; the real-Git regression also exercises an equivalent noncanonical path. The failed run remains part of the CI history rather than being described as passing.

No new image, audio or video was generated or accepted. Real audience preference, author adoption, physical timing, per-provider performance and host-UI skill discovery remain separate verification tasks. The full English user/developer guides do not imply that every specialized reference has been translated from Chinese.

## Previous public quality revision — 2026-10-27

The current public edition has a shorter task router, optional compact versus persistent storyboard contracts, independent installation identity, and Chinese and English entrypoints, with installation and tooling guides. [Four actual synthetic text outputs](docs/text-trials-2026-10-27.md) are now published with their input, source revision, coordinating review and limits. Baseline and post-refactor runs are kept distinct; this is not a controlled before/after quality comparison or a cross-model success rate.

The scripts also provide a single missing-PyYAML diagnosis and concise expected CLI errors. Initializer `--force` still deliberately overwrites managed templates; documentation no longer recommends it for incremental character additions. Local Windows Python 3.11 regression: 241 tests discovered, 236 passed, 5 symbolic-link capability skips. Repository and export audit cover 172 allowlisted files. The release notes and CI record the exact published run. Earlier file/test counts below are historical snapshots, not a claim about every later revision.


## Historical methodology note — 2026-09-15

Historical entries below describe earlier evaluations, including a former 30,000-Han-character default. That default is superseded: deep biography now requires substantive coverage and author review, with no implicit word/page quota. Only an explicitly requested positive minimum is enforced. Historical passes are not evidence of current artistic quality; FT-26 and real author/actor validation remain pending.

## Public fixture revision — 2026-10-27

FT-01, FT-05 and FT-23–FT-27 now use independently authored synthetic inputs. Their current revisions are pending behavioral execution and human review. Earlier run counts or routing observations for the same case IDs apply only to the historical inputs and do not transfer to these replacements. Schema validation checks structure only. The synthetic dialogue examples in `references/natural-dialogue-repair.md` are demonstrations, not measured results.

Project-specific observations, transcripts, identifiable source examples and their measurements are excluded from this public record. The retained historical software checks below concern general development contracts; they do not establish that the current synthetic fixtures pass a model run.

## Independent public skill validation — 2026-10-27

The public edition now uses `role2reel-public` for metadata, invocation and archive root. Installation and removal are independent of an existing `role2reel` directory. A regression check extracts the complete archive beside an internal-skill sentinel and verifies that it remains unchanged; metadata checks reject the internal name and ambiguous invocation suffixes.

Local Windows Python 3.11: 237 discovered, 232 passed, 5 skipped because symbolic links were unavailable. Skill metadata, the 160-file repository contract, and the export privacy audit passed. These checks cover edition separation and software behavior; they do not add a new model or media-quality claim.

## Public candidate validation — 2026-10-27

- Skill metadata and repository validation passed for 160 release files.
- Local Windows Python 3.11 unit run: 235 discovered, 230 passed, 5 skipped because symbolic-link support was unavailable for those tests.
- Export audit passed across the explicit 160-file release inventory, including credential/link checks and an additional local-only confidential-term list. Automated scans do not certify semantic privacy.
- Release ZIP integrity and allowlist coverage are checked before publication.

These results validate software and packaging behavior. The newly synthesized forward cases above have not been executed as model-behavior trials, and no new image, video, actor or production-quality result is claimed.

Historical deterministic check: 2026-08-31

This document separates historical results, currently reproducible deterministic checks, and evaluations that are still pending. It is not evidence of production adoption-rate improvement.

## Evidence ledger

| Evidence | Version | Status | What it supports |
|---|---|---|---|
| Repository validation, unit tests, and release packaging | v0.1.0 | Historical completed record | Structure and deterministic script behavior in the v0.1 release |
| Forward cases FT-01–FT-04, FT-06, and FT-07 | v0.1.0 | Historical recorded runs | The listed hard invariants under the recorded development setup only |
| Repository validation, unit tests, life-path audit tests, and packaging | v0.2.0-beta.1 | Completed locally | Current deterministic contracts and script behavior |
| Forward manifest FT-01–FT-14 | v0.2.0-beta.1 | Schema validated only | Case definitions and the staged-deep record contract are well formed; no generation claim |
| Development cold runs and post-fix regressions for FT-01–FT-13 | v0.2.0-beta.1 | Completed informally | Case-level generation behavior in this Codex development session; not a formal recorded or human study |
| FT-14 staged deep run, three-arm comparison, and blinded human review | v0.2.0-beta.1 | Pending | No production-deep, comparative, adoption, or human-performance result may yet be claimed |
| Repository validation, unit tests, and release packaging | v0.3.0-beta.1 candidate | Completed locally | Additive 命线反演, CharacterOS, storyboard, continuity, and video-task contracts behave as tested |
| Forward manifest FT-01–FT-22 | v0.3.0-beta.1 candidate | Schema validated only | New 命线反演, two-stage retrieval, fused-pipeline, extension, edit, transition, and multi-panel case definitions are well formed; this alone is no behavior claim |
| FT-15–FT-17 independent development cold runs | v0.3.0-beta.1 candidate | Completed informally after recorded failures and repairs | Case-level model behavior under separate model review; not a human or production-deep study |
| FT-19–FT-22 video-mode development runs | v0.3.0-beta.1 candidate | Partial | Hard-case planning behavior was exercised; the post-fix FT-21/FT-22 prose runs were not complete executable `video-task.yaml` packages |
| FT-18 full fused staged run and FT-14 production-deep run | v0.3.0-beta.1 candidate | Pending | Missing real author-approved deep artifacts, isolated full-chain execution, actor review, and adoption decisions |
| Dynamic timing, paste-ready prompt contract, workbook profile, and clipboard auditor | v0.4.0-beta.2 candidate | Completed locally | Mechanical timing fields, fixed output syntax, source-segment offset handling, workbook formula reopening, segmented-label restart audit, and text-export audit; no provider or human-performance claim |
| Source-truth, atomic-shot, physical/sound continuity, post-composite text, and readiness review gates | v0.5.0-beta.1 candidate | Completed locally | Mechanical release blockers and structured review fields; no claim that source comparison or simulated panel findings are human or semantic proof |

## Current v0.4.0-beta.2 candidate deterministic validation

The additive v0.4 candidate source tree was checked locally on 2026-09-01:

| Check | Current result |
|---|---|
| Skill Creator `quick_validate.py` under UTF-8 mode | Pass |
| Role2Reel repository validator | Pass; 96 files checked |
| Python unit tests | 189 discovered; 184 pass and 5 symlink-capability tests skipped on local Windows |
| Release packaging | Pass; 93 allowlisted files packaged; ZIP integrity pass |
| Forward-case manifest contract | Pass; 22 case definitions, including FT-15–FT-22 |

New deterministic coverage checks the visible `explore` versus backstage `production-lock` 命线反演 surfaces; counter-reading and author-operation contracts; separate cognitive-resource and speech-corpus artifacts; two-stage turn references and approved expression evidence; proposition-level common ground and directional second-order belief provenance; exact raw-source/meaning-ledger/humanized-draft identity and approvals; source-bound concise/professional storyboards; visual-asset revisions; explicit continuity locks and state handoffs; deny-by-default reference borrowing; immutable local-media bytes or provider asset versions; exactly one provider-neutral video mode; exact timelines; extension seams; edit targets and protected regions; transition endpoints and bridges; multi-panel mappings; and current-capability evidence for provider-specific tasks. Modern production auditors fail closed without the real bound upstream files; explicit unbound-structure modes are draft lint only. Existing v0.1 and v0.2 compatibility tests remain in the same suite.

These checks still cannot prove that candidate lives are semantically diverse, that a 30,000-character biography has causal or artistic density, that a model truly used a resource rather than copied an ID, that a provider will honor a task, that a dynamic estimate is physically or performatively right, or that actors and production teams prefer the result.

## Current v0.5.0-beta.1 candidate deterministic validation

The source-truth and atomic-shot gate update was checked locally on 2026-09-01:

| Check | Current result |
|---|---|
| Skill Creator `quick_validate.py` under UTF-8 mode | Pass |
| Role2Reel repository validator | Pass; 106 files checked |
| Python unit tests | 194 discovered; 189 pass and 5 symlink-capability tests skipped on local Windows |
| Release packaging | Pass; 102 allowlisted files packaged; ZIP integrity pass |
| Readiness-gate audit tests | Pass; source-truth, atomicity, hard-floor, vacuum-carrier, and post-composite-text blockers covered |

This update generalizes the latest storyboard review findings into reusable contracts: compare dialogue ownership and plot facts against the actual source before polish; classify atomic shots versus split-required or author-approved clusters before timing; name environment-aware sound carriers and force sources; track state handoffs; mark exact text for post-compositing; and preserve simulated multi-role review as simulated evidence. These checks still cannot prove that the source comparison is semantically correct, that the timing is playable, or that a model, actor, or production team will prefer the result.

## v0.3.0-beta.1 development cold-run status: partial evidence

Fresh generators received the routed skill material and case request without the case's hard invariants or prior outputs. Separate model reviewers then scored the retained results. These are development-session model checks, not blinded human evaluation, actor review, or production adoption evidence.

| Scope | Retained result | What happened |
|---|---|---|
| FT-15 | 3/3 hard-case passes | Three fresh 命线反演 outputs preserved four causally different readable lives, a counter-reading, per-route residue and opening behavior, and author control without selecting a winner |
| FT-16 | Initial 0/3; post-fix 3/3 | The first runs skipped or flattened the cognition/expression middle and over-explained; repaired guidance then preserved the two retrieval stages and relationship-specific strategy with restrained surfaces |
| FT-17 | Initial 2/3; intermediate strict 0/3; final post-fix 3/3 | One first-run scene used redundant, controlling dialogue; a mute-pass repair fixed the behavior, but the next outputs omitted the required `light` evidence label; after both repairs, three fresh scenes passed path-to-behavior causality, total-line and duration limits, nonverbal-first playability, and the light/deep boundary |
| FT-19 / FT-20 | One development planning pass each | Extension and protected-edit outputs met the listed hard-case behavior, but this is not provider execution evidence |
| FT-21 / FT-22 | Initial hard-invariant failures; post-fix behavior pass, formal package fail | Transition and multi-panel repairs met the case behavior in fresh prose runs, but those runs omitted parts of the exact executable `video-task.yaml` binding contract and therefore are not production-contract passes |

The failed FT-17 drafts and both later repair stages remain in ignored local development artifacts; the final passing scenes were not substituted retroactively for the failures. FT-14 and FT-18 remain pending because no development agent may fabricate the real author path decision, separately approved 30,000-character biography, isolated full-chain tasks, actor/blinded review, or production adoption decision those cases require.

## Historical v0.1.0 record

The v0.1.0 pre-release report recorded the following deterministic results:

| Check | Recorded result |
|---|---|
| Skill Creator `quick_validate.py` | Pass |
| Role2Reel repository validator | Pass |
| Python unit tests | 25 discovered; 24 pass and 1 symlink-capability test skipped on local Windows |
| Unit tests on local Python 3.9 and bundled Codex Python | Pass on both |
| YAML syntax parse | 18/18 files parse |
| SVG XML parse | Pass |
| Release ZIP integrity | 57/57 allowlisted files readable; no corrupt member |

The same report recorded three cold runs for each of FT-01, FT-02, FT-04, FT-06, and FT-07, and three post-fix cold runs for FT-03; all listed hard invariants passed in those runs. FT-05 received static routing review only and was not counted as a behavioral pass.

Those results remain historical v0.1 evidence. They were not rerun against the v0.2 skill, do not cover the new life-path workflow, and were not a three-arm blinded production study. The previously documented FT-03 failure concerned an adjacent reaction and unchanged ending hold being split into separate shots without a new audience task; the guidance was narrowed and the recorded post-fix runs passed that invariant.

## Current v0.2.0-beta.1 deterministic validation

The v0.2.0-beta.1 source tree was checked locally on 2026-08-31:

| Check | Current result |
|---|---|
| Skill Creator `quick_validate.py` under UTF-8 mode | Pass |
| Role2Reel repository validator | Pass; 67 files checked |
| Python unit tests | 125 discovered; 121 pass and 4 symlink-capability tests skipped on local Windows |
| Release packaging | Pass; 67 allowlisted files packaged |
| Forward-case manifest contract | Pass; 14 case definitions, including FT-08–FT-14 |

The deterministic suite now checks strict fact-boundary categories and stable claim references; three distinct root-candidate structures; author selection/lock-record consistency; candidate-content-bound lock declarations; character/package-bound path and biography approvals; the default 30,000-Han-character deep-biography gate; Markdown-body exclusions and obvious low-diversity padding; biography and artifact path containment; canonical and supported legacy provenance in real runtime and relationship files; candidate and biography hash freshness; exact outline-file review; shared-event content hashes, approval, time bounds, and cross-workbench participant bindings; current-character provenance in multi-character scene assets; and staged variant workbenches, input/source closures, independent task/file/byte outputs, trace bindings, and blind-output coverage. It also retains v0.1 additive compatibility, initialization, dialogue linting, storyboard timing, packaging, and repository safety. These checks do not establish that a human actually made a recorded decision, that a staged task really ran in isolation, or that its output has artistic quality.

The four local skips require symbolic-link creation privileges unavailable to the current Windows account. They are capability skips, not passes; the tests remain available for environments that permit symbolic links.

Deterministic success proves only the configured structural and mechanical invariants. In particular, `tests/test_forward_cases.py` validates the case manifest but does not execute a model or score its output. Character count does not prove causal coherence, individuality, truthful acting, or dramatic usefulness.

## v0.2.0-beta.1 development cold-run status: partial evidence

Five independent development generators read only each case ID, request, and input plus the routed skill documents. They were not shown `hard_invariants`, `human_rubric`, prior outputs, or this file. Separate Codex reviewers then applied the hard invariants and human-oriented rubric. These were development-session model reviews, not blinded human reviews. Exact model build, reasoning setting, and public run artifacts were not recorded as required by the formal protocol, so the results below are informal regression evidence rather than a formal behavioral benchmark.

The first two full runs exposed repeated failures: FT-03 still cut a short scene around spoken units, and FT-08 omitted exact source references or candidate evidence closures. Later runs exposed conditional path comparisons, shared-cue scenes whose private residue was too weak, a silent beat mislabeled as a silent shot, and invented hazards that confounded the shared-context cue. Those failures were retained locally, repaired as general workflow rules, and rerun rather than averaged away.

Final case-level regression status on the corrected guidance:

| Scope | Result | What was actually checked |
|---|---|---|
| FT-01, FT-02, FT-04, FT-06, FT-07, FT-10, FT-12, FT-13 | No hard failure in five full cold runs | Fidelity, knowledge boundaries, asset isolation, narrow-scope restraint, occupation/path separation, outline conflict, and refusal to fake deep completion |
| FT-08 | 3/3 consecutive post-fix full-run passes | Stable source references, candidate evidence-ID closure, feasibility, complete causal nodes, genuinely different paths, and author control |
| FT-03 | 3/3 final targeted passes, confirmed independently by two model reviewers | Two shots for three spoken units, continuous 0–28 seconds, and one wholly silent reaction shot |
| FT-09 | 3/3 final targeted passes, confirmed independently by two model reviewers | B-only formal runtime, A-only counterfactual isolation, C absence, light-tier honesty, and same-present material path differences |
| FT-11 | 3/3 final targeted passes, confirmed independently by two model reviewers | Shared-cue decoding, uninformed outsider behavior, distinct private residue, nonverbal restraint, and no confounding invented emergency |
| FT-05 | Routing-only correct in five runs | The skill correctly declined a generic administrative rewrite; notice-copy behavior was deliberately not generated or scored |

The final three-case regression artifacts have local SHA-256 values `9101DDA2…E7C16CB`, `BE0CC49A…B7F596`, and `88E7009F…C1FC9C`; A and C passed all three cases, while B preserved the last FT-09 conditional-comparison failure that triggered the final rule change. The three subsequent FT-09-only passing artifacts have `E0B89337…F605E1C`, `DB983F4E…CD0E48`, and `4ADE41CC…8857B`. They remain under ignored `test-results/` and are excluded from the release package.

FT-09 through FT-12 remain author-approved `light` unit fixtures. They test narrow behavior but cannot show that a long biography caused a scene. FT-14 still lacks an actual author-approved 30,000-countable-Han-character biography, separate compile and scene tasks, controlled variants, and human actor review. The development agents cannot fabricate that author approval. There is therefore no completed production-deep behavioral pass, three-arm comparison, adoption rate, effect size, or evidence that v0.2.0-beta.1 outperforms either baseline.

## Planned three-arm blinded comparison

Use the protocol in `tests/forward/README.md` and compare:

| Arm | Method |
|---|---|
| A — baseline | Pinned unmodified Role2Reel v0.1 workflow |
| B — biography length only | The same pinned v0.1 workflow plus a longer unstructured biography without candidate selection, lock, provenance, or runtime compilation |
| C — selected life path | Multiple causal candidates, explicit author path lock, a separately author-approved exact deep-biography revision and body hash when applicable, then runtime compilation, knowledge boundaries, and turn-state simulation |

Blind reviewers to the method and score three metric families:

1. **Adoption and editing burden:** direct adoption, light-edit adoption, rejection, edit magnitude and reasons, and whole-scene no-rewrite rate.
2. **Causal individuality and integrity:** name-hidden speaker identification, path-swap sensitivity, occupational-context stability, node ablation, branch leakage, knowledge integrity, character consistency, and scene consequence.
3. **Performance and dramatic usefulness:** actor read-aloud fluency, playable pursuit and tactics, subtext, relationship movement, nonverbal substitution, and reviewer preference with concrete repair reasons.

No production adoption-rate baseline is published here. A future comparison must use the same unit and adoption definition across arms, representative material, recorded denominators, blinded decisions, and uncertainty reporting; results must be supported by evidence authorized for that reporting scope.

## Claims boundary

These checks do not establish that every result will feel human or cinematic, that a long biography is artistically sufficient, that a specific provider feature remains current, or that writers, directors, actors, or editors will adopt more output. Any improvement claim requires completed comparable runs, retained decisions, blinded review, and reported failures as well as successes.
