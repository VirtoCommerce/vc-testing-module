export type AttributeFilter = Readonly<Record<string, string | undefined>>;

export function attributeSelector(attributes: AttributeFilter): string {
  return Object.entries(attributes)
    .filter((entry): entry is [string, string] => entry[1] !== undefined)
    .map(([name, value]) => `[${name}=${JSON.stringify(value)}]`)
    .join("");
}
