import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';

describe('ALPHA-43: SplitSpeak branding', () => {
  it('uses SplitSpeak as the browser tab title', () => {
    const html = readFileSync(new URL('../index.html', import.meta.url), 'utf8');

    expect(html).toMatch(/<title>SplitSpeak<\/title>/);
  });
});
