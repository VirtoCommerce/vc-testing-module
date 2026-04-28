# QA Plan

**Stage 1 of 3** in the QA workflow: Plan → Implement → Review

You are orchestrating the planning stage. Spawn the `qa-planner` agent to analyze the requirement and produce both a test strategy and an implementation plan.

## Input

The user provides a requirement — this can be:
- A Jira ticket number or URL
- A feature description
- A bug report
- A plain-text requirement

Pass `$ARGUMENTS` as the requirement to the agent.

## Steps

### 1. Test Strategy

Spawn the `qa-planner` agent and ask it to invoke the `/plan-test-strategy` skill with the user's requirement.

The agent should:
- Analyze the requirement
- Explore existing test coverage in the codebase
- Produce a structured test strategy (test cases, types, priorities, data needs)

### 2. Implementation Plan

After the test strategy is complete, ask the `qa-planner` agent to invoke the `/plan-implementation` skill using the strategy it just produced.

The agent should:
- Identify all files to create or modify
- Determine implementation order (dependencies first)
- Reference existing patterns for each file
- Specify which skills the implementer should use

### 3. Output

Present the combined result to the user:
1. **Test Strategy** — what to test, priorities, coverage matrix
2. **Implementation Plan** — file-by-file steps with pattern references

End with:
```
Plan complete. Run /qa-implement to execute this plan.
```
