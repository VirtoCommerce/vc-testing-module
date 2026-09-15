import { TopHeaderComponent } from "@page-objects/frontend/components/top-header";
import { Layout } from "@page-objects/layout";

export abstract class DefaultLayout extends Layout {
  get topHeader(): TopHeaderComponent {
    return new TopHeaderComponent(this.page.getByTestId("top-header"));
  }
}
