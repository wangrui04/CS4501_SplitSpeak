// Test-first E2E expectations for issues #44 and #45.
// RED until the expense detail modal and editing workflow are implemented.
import { test, expect } from '@playwright/test';

async function signIn(page) {
  await page.goto('/');
  await page.getByRole('button', { name: /continue as sarah/i }).click();
  await expect(page.getByRole('heading', { name: 'Apartment 4B' })).toBeVisible();
}

async function createExpense(page) {
  await page.getByRole('button', { name: /add an expense/i }).click();
  // Existing manual-entry path creates a saved expense before the popup test.
  await page.getByLabel('Description').fill('Dinner test expense');
  await page.getByLabel(/Amount/).fill('30.00');
  await page.getByRole('button', { name: /^confirm|^save/i }).click();
  await expect(page.getByText('Dinner test expense')).toBeVisible();
}

test('saved expense opens detail dialog with payer, shares and amount owed', async ({ page }) => {
  await signIn(page);
  await createExpense(page);
  await page.getByText('Dinner test expense').click();
  const modal = page.getByRole('dialog', { name: /expense details|dinner test expense/i });
  await expect(modal).toBeVisible();
  await expect(modal.getByText('Sarah')).toBeVisible();
  await expect(modal.getByText('$30.00')).toBeVisible();
  await expect(modal.getByText(/Kayla/)).toBeVisible();
  await expect(modal.getByText(/Rui/)).toBeVisible();
  await modal.getByRole('button', { name: /close/i }).click();
  await expect(modal).not.toBeVisible();
});

test('confirmed expense can be edited and saved without adding a duplicate', async ({ page }) => {
  await signIn(page);
  await createExpense(page);
  await page.getByText('Dinner test expense').click();
  const modal = page.getByRole('dialog', { name: /expense details|dinner test expense/i });
  await modal.getByRole('button', { name: /edit expense/i }).click();
  await modal.getByLabel(/description/i).fill('Corrected dinner test expense');
  await modal.getByLabel(/amount|total/i).fill('36.00');
  await modal.getByRole('button', { name: /save changes|confirm changes/i }).click();
  await expect(page.getByText('Corrected dinner test expense')).toHaveCount(1);
  await expect(page.getByText('Dinner test expense', { exact: true })).toHaveCount(0);
});

test('canceling expense edit leaves saved values unchanged', async ({ page }) => {
  await signIn(page);
  await createExpense(page);
  await page.getByText('Dinner test expense').click();
  const modal = page.getByRole('dialog', { name: /expense details|dinner test expense/i });
  await modal.getByRole('button', { name: /edit expense/i }).click();
  await modal.getByLabel(/description/i).fill('Should not persist');
  await modal.getByRole('button', { name: /cancel/i }).click();
  await expect(page.getByText('Dinner test expense')).toBeVisible();
  await expect(page.getByText('Should not persist')).toHaveCount(0);
});
