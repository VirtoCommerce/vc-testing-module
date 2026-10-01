import type { Locator } from "@playwright/test";
import type { Card, DatePicker, Select } from "../shell/controls";

import { Blade } from "../shell/blade";
import { ConfirmationPopup } from "../shell/controls";
import { DetailsToolbar, Field, Section } from "./constants";

export interface PageFields {
  readonly name?: string;
  readonly permalink?: string;
}

export class PageDetailsBlade extends Blade {
  readonly basicSection: Card;
  readonly personalizationSection: Card;
  readonly schedulingSection: Card;
  readonly nameInput: Locator;
  readonly permalinkInput: Locator;
  readonly permalinkPrefix: Locator;
  readonly language: Select;
  readonly userGroups: Select;
  readonly organization: Select;
  readonly visibilityToggle: Locator;
  readonly visibilityControl: Locator;
  readonly startDate: DatePicker;
  readonly endDate: DatePicker;
  readonly saveButton: Locator;

  constructor(root: Locator) {
    super(root);
    this.basicSection = this.card(Section.basic);
    this.personalizationSection = this.card(Section.personalization);
    this.schedulingSection = this.card(Section.scheduling);
    this.nameInput = this.textInput(Field.name);
    this.permalinkInput = this.textInput(Field.permalink);
    this.permalinkPrefix = this.field(Field.permalink).locator("[data-test-id='permalink-prefix']");
    this.language = this.select(Field.language);
    this.userGroups = this.select(Field.userGroups);
    this.organization = this.select(Field.organization);
    this.visibilityToggle = root.locator("input[role='switch']").first();
    this.visibilityControl = root.locator(".vc-switch").first();
    this.startDate = this.datePicker(Field.startDate);
    this.endDate = this.datePicker(Field.endDate);
    this.saveButton = this.toolbar.button(DetailsToolbar.save);
  }

  async fill(fields: PageFields): Promise<void> {
    if (fields.name !== undefined) {
      await this.nameInput.fill(fields.name);
    }
    if (fields.permalink !== undefined) {
      await this.permalinkInput.fill(fields.permalink);
    }
  }

  async setVisibility(visibleToAll: boolean): Promise<void> {
    if ((await this.visibilityToggle.isChecked()) !== visibleToAll) {
      await this.visibilityControl.click();
    }
  }

  async archive(): Promise<void> {
    await this.toolbar.click(DetailsToolbar.archive);
    await new ConfirmationPopup(this.root.page()).confirm();
  }
}
