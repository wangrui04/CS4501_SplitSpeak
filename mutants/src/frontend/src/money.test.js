import { describe, expect, it } from 'vitest';
import { formatCents, isAmountInput, parseDollarsToCents } from './money';

describe('money utils', () => {
  it.each([
    ['30', 3000],
    ['30.00', 3000],
    ['12.5', 1250],
    ['0.07', 7],
    ['.5', 50],
    ['10.', 1000],
    [' 19.99 ', 1999],
  ])('parses %s to %i cents', (text, cents) => {
    expect(parseDollarsToCents(text)).toBe(cents);
  });

  it.each(['abc', '', '12.345', '1.2.3', '-5', '$5', '1e3', '0x10'])(
    'rejects %s',
    (text) => {
      expect(parseDollarsToCents(text)).toBeNull();
      expect(isAmountInput(text)).toBe(false);
    }
  );

  it('avoids float rounding errors', () => {
    // 0.1 + 0.2 style errors: 19.99 * 100 is 1998.9999999999998 in floats.
    expect(parseDollarsToCents('19.99')).toBe(1999);
    expect(parseDollarsToCents('1.15')).toBe(115);
  });

  it('formats cents for display', () => {
    expect(formatCents(1234)).toBe('$12.34');
    expect(formatCents(5)).toBe('$0.05');
    expect(formatCents(-2500)).toBe('$25.00');
    expect(formatCents(123456)).toBe('$1,234.56');
  });
});
