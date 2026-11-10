// End-to-end smoke tests (issue #36). The backend runs with
// LLM_PROVIDER=fake, so AI replies come from
// src/backend/fixtures/llm_fixtures.json and no paid API is called.
import { expect, test } from '@playwright/test';

const US01 = 'I paid $30 for dinner for Sarah, Kayla, and Rui. Split it equally.';
const UNRESOLVABLE = 'we got some stuff at the place, figure it out';

test.describe.configure({ mode: 'serial' });

async function signInAs(page, name) {
  await page.goto('/');
  await page.getByRole('radio', { name: new RegExp(name) }).click();
  await page.getByRole('button', { name: `Continue as ${name}` }).click();
  await expect(page.getByRole('heading', { name: 'Apartment 4B' })).toBeVisible();
}

test('unauthenticated users see the name picker', async ({ page }) => {
  await page.goto('/');

  await expect(page.getByRole('heading', { name: 'Sign in to SplitSpeak' })).toBeVisible();
  await expect(page).toHaveTitle('SplitSpeak');
  await expect(page.getByRole('button', { name: 'Add an expense' })).toHaveCount(0);
});

test('AI expense: describe, preview, confirm, balances update', async ({ page }) => {
  await signInAs(page, 'Sarah');
  await expect(page.getByText('No expenses yet')).toBeVisible();

  await page.getByRole('button', { name: 'Add an expense' }).click();
  await page.getByRole('tab', { name: /AI assistant/ }).click();
  await page.getByLabel('Describe your expense').fill(US01);
  await page.getByRole('button', { name: /Send/ }).click();

  const preview = page.getByRole('region', { name: 'Itemized expense preview' });
  await expect(preview).toBeVisible();
  await expect(preview.getByText('$30.00').first()).toBeVisible();

  await preview.getByRole('button', { name: 'Confirm expense' }).click();
  await expect(page.getByRole('dialog', { name: 'Add an expense' })).toHaveCount(0);

  const list = page.getByRole('region', { name: 'Expenses' });
  await expect(list.getByText('Dinner')).toBeVisible();
  await expect(page.locator('#owed')).toHaveText('$20.00');

  const balances = page.getByRole('complementary', { name: 'Group balances' });
  await expect(balances.getByText(/Kayla/)).toContainText('owes you $10.00');
});

test('manual entry saves an equal split', async ({ page }) => {
  await signInAs(page, 'Sarah');

  await page.getByRole('button', { name: 'Add an expense' }).click();
  await page.getByRole('tab', { name: 'Manual entry' }).click();
  await expect(page.getByText('Add an expense the usual way.')).toBeVisible();

  await page.getByLabel('Description').fill('Groceries');
  await page.getByLabel('Amount ($)').fill('12.00');
  await page.getByRole('checkbox', { name: 'Rui' }).uncheck();
  await page.getByRole('button', { name: 'Save expense' }).click();

  await expect(page.getByRole('dialog', { name: 'Add an expense' })).toHaveCount(0);
  await expect(page.getByRole('region', { name: 'Expenses' }).getByText('Groceries')).toBeVisible();
});

test('switch to manual when the AI cannot resolve the expense', async ({ page }) => {
  await signInAs(page, 'Sarah');

  await page.getByRole('button', { name: 'Add an expense' }).click();
  await page.getByRole('tab', { name: /AI assistant/ }).click();
  await page.getByLabel('Describe your expense').fill(UNRESOLVABLE);
  await page.getByRole('button', { name: /Send/ }).click();

  await expect(page.getByText("I couldn't work this out. Switch to manual entry?")).toBeVisible();
  await page.getByRole('button', { name: 'Switch to manual entry' }).click();

  await expect(page.getByLabel('Description')).toHaveValue(UNRESOLVABLE);
  await expect(page.getByLabel('Amount ($)')).toHaveValue('');

  // Going back to the AI tab keeps the transcript.
  await page.getByRole('tab', { name: /AI assistant/ }).click();
  await expect(page.getByText(UNRESOLVABLE)).toBeVisible();
});
