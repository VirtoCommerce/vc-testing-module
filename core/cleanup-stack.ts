export type CleanupAction = () => Promise<unknown>;

export type CleanupRunner = (description: string, action: CleanupAction) => Promise<unknown>;

interface CleanupEntry {
  readonly description: string;
  readonly action: CleanupAction;
}

export class CleanupStack {
  readonly #entries: CleanupEntry[] = [];

  push(description: string, action: CleanupAction): void {
    this.#entries.push({ description, action });
  }

  async unwind(run: CleanupRunner = runAction): Promise<void> {
    const errors: unknown[] = [];
    for (let entry = this.#entries.pop(); entry !== undefined; entry = this.#entries.pop()) {
      try {
        await run(entry.description, entry.action);
      } catch (error) {
        errors.push(error);
      }
    }
    if (errors.length === 1) {
      throw errors[0];
    }
    if (errors.length > 1) {
      throw new AggregateError(errors, `${errors.length} cleanup actions failed`);
    }
  }
}

function runAction(_description: string, action: CleanupAction): Promise<unknown> {
  return action();
}
