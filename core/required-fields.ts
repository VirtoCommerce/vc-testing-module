export type WithRequired<T, K extends keyof T> = T & { readonly [P in K]-?: NonNullable<T[P]> };

export function requireFields<T extends object, const K extends keyof T>(
  value: T | undefined,
  fields: readonly K[],
  label: string,
): WithRequired<T, K> {
  if (value === undefined) {
    throw new Error(`${label} is missing`);
  }
  const missing = fields.filter((field) => value[field] === undefined || value[field] === null);
  if (missing.length > 0) {
    throw new Error(`${label} has no ${missing.map(String).join(", ")}`);
  }
  return value as WithRequired<T, K>;
}
