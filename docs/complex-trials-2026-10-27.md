# Complex text trials — 2026-10-27

[中文首页](../README.md) · [English home](../README.en.md) · [Evidence ledger](../EVALS.md) · [Requests, outputs and source fingerprints](complex-trials-2026-10-27.json)

本轮完成三组独立执行，共七种请求、九份完整答案：多人跨场景交接、锁定镜界的APS-C摄影补充、有意重复的对白、同外观物品归属、不可容纳的台词时长、缺失/冲突参考图的依赖，以及液体状态连续性。下方保留完整输入和原始输出；通过指所列文本约束的审查，不是实际影片验收，也不是跨模型成功率。

## Protocol and source

Three fresh execution agents received the public skill snapshot and the requests assigned to their round. They were not given earlier answers, expected answers, suspected failures or the reviewers' conclusions. Round 1 ran E/F/G; round 2 ran H/I/J; round 3 independently repeated the exact E/F requests and added K. Within each round, one agent completed three requests in the same context. This is a small development exercise, not nine statistically independent samples or a benchmark.

The source was a frozen Git archive of [`1e77689`](https://github.com/niuyupeng/role2reel-public/tree/1e77689e8e00a2a93394854a607b882b4a5978ff). The exact opened reference files and SHA-256 values are in the JSON record. Those skill/reference bytes remain unchanged in this release; the release adds documentation, evidence and installation/release tooling. No private project, internal skill, other agent's response, network model API or media was supplied to the generators. The exact serving model identifier, reasoning setting, temperature and seed were not exposed; they are recorded as unknown. No cross-model result is claimed.

The coordinator reviewed the complete answers against the original requests. A separate model reviewer also checked the outputs, quoting evidence for each decision. This is model-assisted editorial review, not blinded human review, author adoption or an actor's performance test. Read-file hashes record accessed files; they cannot prove which instruction caused a decision.

## Results and observable checks

| Output | Actual request and original response | Constraint review | Concrete evidence |
|---|---|---|---|
| E1 | [Three people, two rooms, token handoff](examples/workshop-handoff.md) | Pass | Three 10-second source clips retain 1–9s each for 24 edited seconds. Only token 2 enters the pouch; token 1 and Neri remain in the workshop. Each clip closes its action before its tail. |
| F1 | [Four locked APS-C shots](examples/complex-F1.md) | Pass | Keeps 0–3/3–6/6–9/9–12s, both exact “还差一点。” lines and their speakers, real 24/35mm focal lengths with 1.6× equivalents; no added handles. Contact precedes release and grasp. |
| G1 | [The sealed letter](examples/complex-G1.md) | Pass | 362 whitespace-delimited words, inside the requested 300–450. “Not today.” appears first as Jo's refusal and then Farah's answer; Jo ends holding the unopened letter. No aunt's secret is invented. |
| H2 | [Two identical umbrellas](examples/complex-H2.md) | Pass | Custody follows two counter positions and visible handling, without new markings. Cora does not witness the transfer. Three retained 6s cores total 18s; corridor views keep the camera in the specified cafe region. |
| I2 | [Impossible two-second speech](examples/complex-I2.md) | Pass: conflict handled | Counts 41 Chinese characters, explains that the required sequential action leaves less than 2s to speak, and preserves the task as incomplete. The proposed 11–14s alternative is explicitly an estimate needing authorization; no rewritten finished prompt is substituted. |
| J2 | [Six reference specifications](examples/complex-J2.md) | Pass | Reuses declared identities, excludes the sheet's studio background, separates in-frame assets from stored objects, and keeps courtyard work independent of the invalid storeroom candidate. 2K/4K dimensions are targets, not inspected files. |
| E3 | [Fresh repeat of E](examples/complex-E3.md) | Pass | Independently retains the same three segment budgets, exact three lines, pouch/token custody and completed handovers; camera choices differ without rewriting the event. |
| F3 | [Fresh repeat of F](examples/complex-F3.md) | Pass | Preserves four locked windows and the repeated line, APS-C basis and real focal lengths; explicitly waits for the badge to settle before closing the box. |
| K3 | [Pour, speak, sip and set down](examples/complex-K3.md) | Pass | One cut at 4s, 8s total, one jug and one glass; water changes only by the visible pour and one sip. Tom speaks before the glass touches his lips and sets it down partly full. |

“Pass” does not mean the two-second request became executable: I2 passes because it detects and reports the irreducible conflict. Nor does J2 mean that reference images exist: it passes the requested planning-only contract. E and F were repeated twice each; the other five requests were executed once. All nine original answers are retained, without replacing a weaker answer with an edited demonstration.

## Useful qualifications

- E's reference images are declared but unattached. Its hook clearance and optics remain planning assumptions. E1 also refers to an established aspect ratio although none was supplied; a production handoff should explicitly carry the chosen ratio or mark it undecided. It is not verified image geometry.
- F preserves the crop basis, but real people, table dimensions, available lenses and optical depth were not measured. Framing/focus proposals need real reference or camera checks before shooting.
- G meets the knowledge and prose constraints. Its sentence explicitly describing Jo's knowledge could be edited for a less explanatory voice; the trial is not a unanimous taste judgment.
- H assumes a compact route between the entrance and counter. Actual room dimensions and the corridor sightline must be checked before treating its timing and framing as executable media direction.
- J's original six-shot framing details are not supplied. Its reference compositions are labelled proposals; they must not silently replace an author's more specific approved framing. The correct rear-door layout is still an input dependency.
- K's natural-speed action budget is an estimate. No recording establishes that these actors or a selected video model can execute that schedule.

These are actionable preparation limits, not facts hidden by the word “pass.” The public workflow should keep such assumptions visible and request only the missing information that blocks the chosen next step.

## Reproduce or challenge a result

1. Use the linked source commit, then check the relevant read-file hashes in the JSON record.
2. Start a fresh agent with only the skill and one linked request. Keep other outputs and this review hidden from the generator.
3. Save the whole first response, source revision, model/settings actually exposed and all relevant tool use. Do not report inaccessible model settings as known.
4. Check exact source constraints and quote the response that supports or violates them. Keep physical timing estimates separate from observed performance, and editorial preference separate from a hard contradiction.
5. If a fix is made, preserve the failed response and run a fresh regression. To claim reliability across models or human preference, add repeated controlled samples and independent human review rather than extrapolating this set.

The JSON fingerprints cover UTF-8 text between each page's `original-request-*` and `original-output-*` markers, normalized to LF endings with a terminal LF when absent. The complete public output blocks can be compared without private paths or raw tool logs.

No images, audio or videos were generated in these trials. There is no new evidence of skin/fur realism, lip sync, frame continuity, optical execution, provider support, production speed or user adoption.
