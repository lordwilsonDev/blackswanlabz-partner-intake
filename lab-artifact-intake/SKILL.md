---
name: lab-artifact-intake
description: Use when a person or organization wants to partner with BlackSwanLabz or use its free lab (curriculum, skills, SOPs, human-resources pack, KPIs and OKRs, grant readiness, including measuring growth of people with special needs inside a company). Asks exactly five multiple-choice questions, then fetches the matching artifacts from the public research lab and drafts a labeled starter pack from them. Works for any AI model that can read files and run Python.
---

# Lab artifact intake: five questions, then the lab's artifacts

> Install location: works from `~/.agents/skills/lab-artifact-intake` (Codex and other agents) or `~/.claude/skills/lab-artifact-intake` (Claude Code). `<skill dir>` below means whichever holds this file.

**What this is for.** BlackSwanLabz wants to be a partner: say plainly what it is trying to do, and hand people the real artifacts from its public lab so they can use them with their own AI. This skill turns five checked answers into a fetched, labeled starter pack: curriculum, skills, SOPs, human-resources pack, KPIs and OKRs, and a grant-readiness checklist. One use is growth measurement for people with special needs inside a company, and a grant may pay for that work.

**Source:** the public lab `https://github.com/lordwilsonDev/blackswanlabz-research-lab`. Agent entry point: `https://raw.githubusercontent.com/lordwilsonDev/blackswanlabz-research-lab/HEAD/llms.txt`.

## Rules (read first)
1. **Partner stance, plain words.** Short sentences, no jargon, no hype. Say what the lab is and is not.
2. **Designed is not running is not proven.** Quote each lab page's own status banner. Label every draft "DRAFT (designed, not run)". Never invent a number, person, wage, customer, outcome or credential.
3. **No promises about money.** Never say a grant will be won or that someone is eligible. Funding rules come from the funder's current program, retrieved fresh, never from memory. A professional reviews anything submitted.
4. **Not a licensed advisor** (legal, tax, medical, clinical, HR law). Say where a qualified person must review.
5. **People with disabilities:** person first, strengths first, the worker helps set their goals, measure each person against their own baseline, collect the least data, no diagnoses in the pack, consent for records. The lab has no page on this: section 7 of `references/pack-templates.md` is new design and must say so.
6. **Ask before any outward action** (sending, publishing, signing up, submitting). Everything stays in a local folder until the person decides.
7. **Do not post the person's answers anywhere.** They are theirs.

## Steps
1. **Say what will happen** in two sentences: five questions, then you fetch the lab's artifacts and draft a starter pack; nothing is sent anywhere.
2. **Ask the five questions** exactly as written in `references/questions.md`, in order, with a multiple-choice UI if the tool has one (several boxes allowed where marked). Many tools cap a question at 4 options; these questions have 7 to 8, so in that case print the lettered list in chat and wait for the reply (found when the skill was first tested, 2026-10-25). Allow "Not sure" and "Other". No sixth question. If an answer is "Not sure", record UNKNOWN and keep going; if a question was skipped, ask it once more, then record UNKNOWN (see `references/questions.md`).
3. **Route** the answers to needs with the table at the bottom of `references/questions.md`. Tell the person which needs you chose and why, and let them add or remove one.
4. **Fetch** the artifacts. Make an output folder the person picks (default `lab-pack/`), then run
   `python3 <skill dir>/scripts/fetch_lab.py --needs <comma list> --out <folder>`
   (add `--clone <path>` if a local clone of the lab exists, as a fallback). Run `--check` first if you suspect the map is stale. The tool saves every file under `<folder>/lab/`, and a `MANIFEST.json` with URL, hash, size, date and each page's status banner. If any file fails, say which and carry on with the rest; never silently skip.
5. **Read** the fetched files before drafting. If the tool printed `STUB:` for a page, that page is not available: say so. Read `llms.txt` and `AGENTS.md` first (rule 11: go all the way through, assume nothing, name the scope of any claim of absence). Look up each page's status banner.
6. **Draft the pack** from `references/pack-templates.md`, sized by Q2, in `<folder>/`: `README.md` (cover page), then only what Q3 chose: `curriculum/`, `skills.md` (which lab skills to load and how), `sops/` (3 to 5), `hr/`, `kpi-okr.md`, `grant-readiness.md`; plus the growth-measurement design when Q1 includes people with disabilities or special needs. Cite the lab file for each part. Mark every unknown.
7. **Tell the person what you made**, in plain words: what came straight from the lab, what you drafted, what is new material not from the lab, what is unknown, and the one next step. Point them to `llms.txt` so their own AI can keep going.
8. **Offer, do not do:** adding a worker's or company's real data, contacting a funder, or submitting anything.

## Output contract
`README.md` with: the five answers in the person's words; needs chosen; files fetched (path, banner, hash); drafts made; unknowns; decisions for a human; next smallest step. Each draft has a status line and a source line.

## Common mistakes
| Mistake | Fix |
|---|---|
| Asking more than five questions, or rewording them | Use `references/questions.md` verbatim |
| Treating a lab SOP as something that runs | Quote its banner; say "target system" where the page says so |
| Calling L1 to L10 an occupational classification | It is a capability framework; say so |
| Writing KPI targets with no baseline | "baseline: measure first" |
| Presenting section 7 as lab material | It is new design, to be reviewed by qualified practitioners |
| Relabeling consulting or automation as training | The lab's anti-consulting rule: training counts only when a worker acquires and demonstrates a competency |
| Using the `/main/` raw URL | The lab's default branch is `master`; use the `HEAD` form |

## Files
- `references/questions.md`: the five questions and the routing table
- `references/artifact-map.md`: needs to lab files, what each supplies, caveats, what the lab does not have
- `references/pack-templates.md`: templates for every artifact, plus the growth-measurement design (section 7, new)
- `references/example-pack-readme.md`: what a finished cover page looks like (fictional)
- `scripts/fetch_lab.py`: fetch, manifest, `--check`; recovers archived pages from the lab's git history
