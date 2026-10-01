const REGEXP_SPECIAL_CHARACTERS = /[.*+?^${}()|[\]\\]/g;

export function exactText(value: string): RegExp {
  return new RegExp(`^\\s*${value.replace(REGEXP_SPECIAL_CHARACTERS, "\\$&")}\\s*$`);
}
