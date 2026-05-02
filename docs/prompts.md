# Agent Prompts

These prompts were used to test the `sql-insight-auditor` skill in Codex.

## Prompt 1: Normal Case

Use the `sql-insight-auditor` skill to review `inputs/normal_case.sql` with the business context in `inputs/business_question.md`. First, run the parser script to generate `outputs/normal_case_parsed_summary.json`. Then use `outputs/normal_case_parsed_summary.json` as the source of truth to create a stakeholder-ready SQL Insight Audit in `outputs/normal_case_stakeholder_explanation.md`.

## Prompt 2: Edge Case

Use the `sql-insight-auditor` skill to review `inputs/edge_case.sql` with the business context in `inputs/business_question.md`. First, run the parser script to generate `outputs/edge_case_parsed_summary.json`. Then use `outputs/edge_case_parsed_summary.json` as the source of truth to create a stakeholder-ready SQL Insight Audit in `outputs/edge_case_stakeholder_explanation.md`. Include any limitations caused by CTEs, joins, or rolling date logic.

## Prompt 3: Cautious Case

Use the `sql-insight-auditor` skill to review `inputs/cautious_case.sql` with the business context in `inputs/business_question.md`. First, run the parser script to generate `outputs/cautious_case_parsed_summary.json`. Then use `outputs/cautious_case_parsed_summary.json` as the source of truth to create a stakeholder-ready SQL Insight Audit in `outputs/cautious_case_stakeholder_explanation.md`. Be cautious if the SQL has unclear logic, `SELECT *`, missing join conditions, or ambiguous `AND` / `OR` logic.