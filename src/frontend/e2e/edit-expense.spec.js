
import { test, expect } from '@playwright/test';

let nextExpense = 1;

async function signIn(page) {
  await page.goto('/');
  await page.getByRole('radio', { name: 'Sarah' }).click();
  await page.getByRole('button', {
    name: 'Continue as Sarah',
  }).click();

  await expect(
    page.getByRole('heading', { name: 'Apartment 4B' })
  ).toBeVisible();
}

async function createExpense(page) {
  const name = `Dinner edit test ${nextExpense++}`;

  await page.getByRole('button', {
    name: 'Add an expense',
  }).click();

  await page.getByRole('tab', {
    name: 'Manual entry',
  }).click();

  await page.getByLabel('Description').fill(name);
  await page.getByLabel('Amount ($)').fill('30.00');

  await page.getByRole('button', {
    name: 'Save expense',
  }).click();

  await expect(
    page.getByRole('dialog', { name: 'Add an expense' })
  ).toHaveCount(0);

  await expect(
    page.getByRole('region', { name: 'Expenses' })
      .getByText(name, { exact: true })
  ).toBeVisible();

  return name;
}

async function openExpense(page, name) {
  await page.getByRole('region', {
    name: 'Expenses',
  }).getByText(name, { exact: true }).click();

  const modal = page.getByRole('dialog', {
    name: 'Expense details',
  });

  await expect(modal).toBeVisible();
  return modal;
}

test('saved expense opens a detailed breakdown', async ({
  page,
}) => {
  await signIn(page);
  const name = await createExpense(page);
  const modal = await openExpense(page, name);

  await expect(
    modal.getByText(name, { exact: true })
  ).toBeVisible();

  await expect(
    modal.getByText('Paid by Sarah')
  ).toBeVisible();

  await expect(
    modal.getByText("Kayla's share")
  ).toBeVisible();

  await expect(
    modal.getByText("Rui's share")
  ).toBeVisible();

  await expect(
    modal.getByText('Kayla owes Sarah')
  ).toBeVisible();

  await modal.getByRole('button', {
    name: 'Close',
  }).click();

  await expect(modal).not.toBeVisible();
});

test('editing a confirmed expense updates existing record', async ({
  page,
}) => {
  await signIn(page);
  const name = await createExpense(page);
  const modal = await openExpense(page, name);

  await modal.getByRole('button', {
    name: 'Edit expense',
  }).click();

  await modal.getByLabel('Description')
    .fill('Corrected dinner test expense');

  await modal.getByLabel('Total amount ($)')
    .fill('36.00');

  await modal.getByRole('button', {
    name: 'Save changes',
  }).click();

  await expect(modal).not.toBeVisible();

  const list = page.getByRole('region', {
    name: 'Expenses',
  });

  await expect(
    list.getByText('Corrected dinner test expense')
  ).toHaveCount(1);

  await expect(
    list.getByText(name, { exact: true })
  ).toHaveCount(0);

  await expect(
    page.locator('#owed')
  ).toHaveText(/\$24\.00/);
});

test('canceling changes keeps original expense', async ({
  page,
}) => {
  await signIn(page);
  const name = await createExpense(page);
  const modal = await openExpense(page, name);

  await modal.getByRole('button', {
    name: 'Edit expense',
  }).click();

  await modal.getByLabel('Description')
    .fill('Should not persist');

  await modal.getByRole('button', {
    name: 'Cancel',
  }).click();

  await expect(
    modal.getByText(name, { exact: true })
  ).toBeVisible();

  await expect(
    page.getByText('Should not persist')
  ).toHaveCount(0);
});
