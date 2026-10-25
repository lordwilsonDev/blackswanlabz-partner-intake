# BlackSwanLabz Partner Intake

> **Status (2026-10-25): a working draft skill, tested once by its author.** Free to use. It makes drafts, not results. It does not promise grants, eligibility or outcomes.

**What this is.** A free skill for an AI agent (Claude Code, Codex or any agent that can read files and run Python). It asks you five multiple-choice questions, goes to the public [BlackSwanLabz research lab](https://github.com/lordwilsonDev/blackswanlabz-research-lab), fetches the artifacts that match your answers (curriculum, skills, SOPs, a human-resources pack, KPIs and OKRs, a grant-readiness checklist), and drafts a labeled starter pack you can review. One use is measuring the growth of people with disabilities or special needs inside a company, which some workforce grants may help pay for.

**Who is behind it.** BlackSwanLabz is the work of Lord Wilson, made with AI assistance, published in the open. We would like to work with partners: people and organizations who want to use these artifacts for real. To talk about partnering, open an issue on this repository.

## What is real
- The skill, its five questions and its fetch tool are in this repository and run: `lab-artifact-intake/scripts/fetch_lab.py --needs all --check` tests that all 25 mapped lab files still resolve (all did on 2026-10-25).
- The lab it draws from is public, with its claims, statuses and gaps in the open: [research lab](https://github.com/lordwilsonDev/blackswanlabz-research-lab).
- The first test of the skill ran on its author's own answers and produced a draft pack (see "Limits").

## What is only designed
- Every artifact the skill drafts is a **draft, designed and not run**. The lab's own pages say the same about themselves (statuses such as `pending`, `archived`, `design`).
- The part on measuring growth of people with disabilities or special needs is **new design added by this skill; the lab has no page on it**. It must be reviewed by qualified disability-employment professionals before anyone uses it.
- The lab's grant material is built around one Wisconsin reference case. Your funder's current rules come from your funder, not from this repository.

## What we do not claim
No customers, no funded grants, no measured worker outcomes, no results from using these artifacts. Nothing here is legal, tax, medical, clinical or HR-law advice.

## Use it
Point your AI agent at [`llms.txt`](llms.txt), then at [`lab-artifact-intake/SKILL.md`](lab-artifact-intake/SKILL.md). The agent asks the five questions in [`lab-artifact-intake/references/questions.md`](lab-artifact-intake/references/questions.md), runs the fetch tool, and writes the pack to a folder you choose. Nothing is sent anywhere.

## Limits
Tested once, on the author's own answers (a fictional-scope test, not a real organization). The lab repository is the evidence base; this repository only routes you to it.

Licenses: text under [CC BY 4.0](LICENSE); code under [MIT](LICENSE-CODE).
