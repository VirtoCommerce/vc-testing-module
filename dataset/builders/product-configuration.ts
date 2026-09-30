import type { ConfigurationSectionInput, ProductConfigurationFragment } from "@api/graphql/generated/graphql";

export const LAST_OPTION = Number.POSITIVE_INFINITY;

export function optionOfEachSection(
  configuration: ProductConfigurationFragment,
  optionIndex = 0,
): ConfigurationSectionInput[] {
  return (configuration.configurationSections ?? []).flatMap((section) => {
    const options = section?.options ?? [];
    const option = options[Math.min(optionIndex, options.length - 1)];
    const productId = option?.product?.id;
    if (section?.type == null || option === undefined || option === null || productId === undefined) {
      return [];
    }
    return [{ sectionId: section.id, type: section.type, option: { productId, quantity: option.quantity } }];
  });
}
