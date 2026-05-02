# SQL Insight Auditor Skill

## Skill Demo
**YouTube Link:** https://youtu.be/IlDDpbCjZV4

## Overview

This repository contains my Week 5 reusable AI skill project. The skill is called `sql-insight-auditor`, and it is designed to help analysts turn SQL queries into clear, stakeholder-ready documentation.

The skill reviews a SQL query, extracts the query structure with a deterministic Python script, and then uses the parsed output to support a plain-English SQL Insight Audit. The goal is to make SQL logic easier to explain to business or analytics audiences while also identifying assumptions, risks, and limitations.

## What the Skill Does

The `sql-insight-auditor` skill helps document and audit one SQL query at a time. It is intended for cases where a user provides a SQL query and wants to understand what the query is doing in business-friendly language.

The skill identifies:

- source tables
- selected fields
- joins
- filters
- date logic
- grouping and ordering logic
- aggregate metrics
- risks, caveats, and limitations

The final output is a stakeholder-ready SQL Insight Audit saved in the `outputs/` folder.

## Why I Chose This Skill

I chose this skill because, in Advertising, first-party client data is often used to support quarterly planning and audience strategy decisions. When numbers are delivered to strategy teams, they may ask follow-up questions about the output, the methodology, or whether the query logic is correct. In rare cases, especially when the numbers are unexpected or do not align with assumptions, the query itself needs to be reviewed and documented clearly.

This creates a real workflow challenge because technical documentation takes time, and it is not always easy to make SQL methodology clear for a non-technical audience. Most of the time, data scientists and analysts do not have the bandwidth to write detailed documentation for every query, especially when the explanation needs to be both accurate and stakeholder-friendly.

The `sql-insight-auditor` skill helps streamline that process. The Python script handles the deterministic parsing step by extracting the query structure, while the AI agent uses that structured output to create a plain-English audit. This makes the workflow more reusable, reduces the chance of missing important query details, and helps create documentation that is easier for strategy and planning teams to understand.

## Step-by-Step Codex Workflow
1. Open the Repository on Codex.
2. Confirm the project bis on the correct repository and branch:
    ````
    Repository: sql-insight-auditor
    Branch: main
    ````
3. Open the skill folder:
    ````
    .agents/skills/sql-insight-auditor/
    ````
4. Confirm the skill includes:
    ````
    SKILL.md
    scripts/parse_sql.py
    ````
5. Copy/ Paste a prompt from the saved `docs/ prompt.md` file into Codex and run.
6. Repeat the same workflow for the other cases.
7. Review the generated output files in:
    ````
    outputs/
    ````
    The expected output files are:
    ````
    outputs/normal_case_parsed_summary.json
    outputs/normal_case_stakeholder_explanation.md
    outputs/edge_case_parsed_summary.json
    outputs/edge_case_stakeholder_explanation.md
    outputs/cautious_case_parsed_summary.json
    outputs/cautious_case_stakeholder_explanation.md
    ````
8. Review the final audit files to confirm that the agent used the parsed JSON summaries as the source of truth and did not invent unsupported SQL logic.

## What the Scripts Does
The Python script performs the deterministic part of the workflow. It reads a .sql file, cleans the SQL text, and extracts common SQL components into a structured JSON summary.

The script extracts:
- `SELECT` fields
- source tables
- `JOIN` clauses
- `WHERE` filters
- `GROUP BY` fields
- `ORDER BY` fields
- date filters
- aggregate metrics
- parser limitations
- risk flags

This script is load-bearing because SQL structure should be extracted consistently before the AI writes a business-facing explanation. The model should orchestrate the workflow and write the final audit, but the script handles the part that code can do more reliably.

## Testing the Skill
The skill was tested on three prompts in Codex:

1. **Normal Case:** a monthly sales performance summary query.
2. **Edge Case:** a query using CTEs, rolling date logic, and anti-join logic.
3. **Cautious Case:** an intentionally unclear SQL query with risky patterns such as SELECT *, a join without a clear ON condition, and mixed AND / OR logic.

The test prompts are saved in: `docs/ prompts.md`

The test case documentation and evaluation summary are saved in: `evals/ test_cases.md`

The generated outputs are saved in: `outputs/`

## What Worked Well
The skill worked well for separating deterministic parsing from narrative explanation. The parser created structured JSON summaries, and the agent used those summaries as the source of truth when writing the SQL Insight Audits.

The normal case worked especially well because the SQL followed a common analytical structure with clear selected fields, filters, grouping logic, and aggregate metrics. The cautious case also worked well because the skill identified risky SQL patterns and avoided claiming that the query was business-ready. The edge case showed that the workflow can still be useful with more complex SQL, even when the parser has limitations.

## Limitations
The parser is intentionally lightweight. It works best for common analytical SQL patterns such as `SELECT`, `FROM`, `JOIN`, `WHERE`, `GROUP BY`, and `ORDER BY`.

Some limitations remain:
- Complex CTEs may only be partially parsed.
- Deeply nested queries may require manual review.
- Vendor-specific SQL syntax may not always be captured perfectly.
- The skill does not execute SQL.
- The skill does not validate whether query results are correct.
- The skill cannot confirm business logic unless enough context is provided.
- The final audit should still be reviewed by a human analyst before being used for business decisions.

## Git Workflow
This project was developed in stages using **GitHub Desktop, GitHub, and Codex.** I first created the repository and project folder structure, then added the reusable skill instructions in `SKILL.md`. After that, I added the business question and three SQL input cases, built the deterministic SQL parsing script, updated the script so each test case generated its own JSON output, and saved the Codex prompts used to test the skill.

The final stages focused on running the skill test cases, adding the generated outputs, documenting the evaluation, and preparing the README. This staged workflow made it easier to track how the project evolved from a reusable skill concept into a working agent-supported workflow.

## Commit Log
- **Initial commit:** Created the initial GitHub repository.
- **Create initial skill project structure:** Added the main repository folders, including the skill folder structure, `inputs/`, `outputs/`, `evals/`, and `docs/`.
- **Add SQL Insight Auditor skill instructions:** Added the initial `SKILL.md` file with the skill name, description, activation logic, expected inputs, workflow steps, output format, limitations, and quality checklist.
- **Add Business Question & 3 SQL input cases:** Added the shared business context and the normal, edge, and cautious SQL test cases.
- **Add deterministic SQL parsing script:** Added `parse_sql.py`, the load-bearing Python script used to parse SQL files into structured JSON summaries.
- **Update parse_sql.py to create case-specific output JSON files, instead of overwriting one file:** Updated the parser so each SQL input case creates its own parsed output file in the `outputs/` folder.
- **Update Codex prompts with case-specific JSON outputs:** Revised the saved Codex prompts so each test case points to its matching parsed JSON output file.
- **Added the expected output template for quick reference:** Added the reference template used to keep the final SQL Insight Audit format consistent.
- **Add Skill Test Outputs & Evaluation:** Added the parsed JSON outputs, stakeholder-ready SQL Insight Audits, and test evaluation summary.
- **Add README file with Project Description & YouTube Link**