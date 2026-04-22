# QA Implement

**Stage 2 of 3** in the QA workflow: Plan → Implement → Review

You are orchestrating the implementation stage. Spawn the `qa-automation-expert` agent to execute the implementation plan from the previous `/qa-plan` stage.

## Input

The implementation plan should already exist in the conversation from a previous `/qa-plan` run. If no plan exists, ask the user to run `/qa-plan` first or provide a task description.

If `$ARGUMENTS` is provided, use it as additional context or override instructions.

## Steps

### 1. Review the Plan

Read the implementation plan from the conversation context. Identify:
- Files to create/modify (in dependency order)
- Which skill to invoke for each file
- Pattern references for each file

### 2. Execute Phase by Phase

Spawn the `qa-automation-expert` agent and execute the plan in order:

**Phase 1: Infrastructure** (types, operations, pages, components)
- For GraphQL types and operations → agent invokes `/create-graphql-layer`
- For page objects and components → agent invokes `/create-ui-layer`
- For REST API operations → agent reads pattern references and creates directly

**Phase 2: Tests**
- For GraphQL tests → agent invokes `/write-graphql-test`
- For E2E tests → agent invokes `/write-e2e-test`
- For REST API tests → agent invokes `/write-rest-api-test`

**Phase 3: Exports**
- Update `__init__.py` files for new classes

### 3. Verify

After implementation:
- Run `pytest --collect-only` on the new test files to verify they are discoverable
- Check for import errors
- Report what was created

### 4. Output

Present a summary:
- Files created/modified (with line counts)
- Test functions added
- Any issues encountered

End with:
```
Implementation complete. Run /qa-review to review the code.
```
