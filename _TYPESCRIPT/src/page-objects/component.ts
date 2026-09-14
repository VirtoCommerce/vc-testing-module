import type { Locator } from "@playwright/test";

export abstract class Component {
  constructor(protected readonly root: Locator) {}
}
