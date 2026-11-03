// Money helpers. Amounts are integer cents everywhere; dollars appear
// only at the UI edge. Parsing is string-based, so no float math.

const AMOUNT_PATTERN = /^(\d+)(?:\.(\d{0,2}))?$|^\.(\d{1,2})$/;

// Digits and at most one decimal point, with at most 2 decimals.
export function isAmountInput(text) {
  return AMOUNT_PATTERN.test(text.trim());
}

// "12.5" -> 1250. Returns null for anything that is not a valid amount.
export function parseDollarsToCents(text) {
  const match = AMOUNT_PATTERN.exec(String(text).trim());
  if (!match) return null;

  const whole = match[1] ?? '0';
  const fraction = (match[2] ?? match[3] ?? '').padEnd(2, '0');
  return Number(whole) * 100 + Number(fraction);
}

// 1234 -> "$12.34". Signs are left to the caller.
export function formatCents(cents) {
  const value = Math.abs(cents ?? 0);
  const dollars = Math.floor(value / 100).toLocaleString('en-US');
  return `$${dollars}.${String(value % 100).padStart(2, '0')}`;
}
