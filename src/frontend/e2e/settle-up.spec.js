// Settle up and reminders end to end (#46). Uses the Weekend trip
// group so it stays independent of the Apartment 4B smoke tests.
// Only the person being paid records a payment, so Sarah records both
// Kayla's partial payment and the remainder.
import { expect, test } from '@playwright/test';

test.describe.configure({ mode: 'serial' });

async function signInAs(page, name) {
  await page.goto('/');
  await page.getByRole('radio', { name: new RegExp(name) }).click();
  await page.getByRole('button', { name: `Continue as ${name}` }).click();
  await expect(page.getByRole('heading', { name: 'Apartment 4B' })).toBeVisible();
}

async function openWeekendTrip(page) {
  await page.getByRole('button', { name: /Weekend trip/ }).click();
  await expect(page.getByRole('heading', { level: 1, name: 'Weekend trip' })).toBeVisible();
}

test('record partial payment, remind, recipient sees it, pay remainder', async ({ page, browser }) => {
  // Sarah pays $60 split with Kayla, so Kayla owes Sarah $30.
  await signInAs(page, 'Sarah');
  await openWeekendTrip(page);
  await page.getByRole('button', { name: 'Add an expense' }).click();
  await page.getByRole('tab', { name: 'Manual entry' }).click();
  await page.getByLabel('Description').fill('Cabin');
  await page.getByLabel('Amount ($)').fill('60.00');
  for (const name of ['Rui', 'Aly', 'Ben']) {
    await page.getByRole('checkbox', { name }).uncheck();
  }
  await page.getByRole('button', { name: 'Save expense' }).click();

  const balances = page.getByRole('complementary', { name: 'Group balances' });
  await expect(balances.getByText(/Kayla/)).toContainText('owes you $30.00');

  // Record a partial payment of $10.
  await page.getByRole('button', { name: 'Settle up' }).click();
  const dialog = page.getByRole('dialog', { name: 'Settle up' });
  await expect(dialog.getByRole('radio', { name: 'Kayla owes you $30.00' })).toBeChecked();
  await dialog.getByLabel('Amount ($)').fill('10');
  await dialog.getByRole('button', { name: 'Record payment' }).click();
  await expect(
    dialog.getByText('This records a payment only; SplitSpeak does not transfer money.')
  ).toBeVisible();
  await dialog.getByRole('button', { name: 'Confirm payment' }).click();
  await expect(dialog.getByRole('status')).toHaveText('Recorded $10.00 from Kayla.');
  await dialog.getByRole('button', { name: 'Close' }).click();

  await expect(balances.getByText(/Kayla/)).toContainText('owes you $20.00');
  await expect(page.getByRole('region', { name: 'Payments' })).toContainText('Kayla paid Sarah $10.00');

  // Send Kayla a reminder for the remaining $20.
  await page.getByRole('button', { name: 'Settle up' }).click();
  await dialog.getByRole('tab', { name: 'Send reminder' }).click();
  await expect(dialog.getByRole('region', { name: 'Reminder preview' })).toContainText(
    'Hi Kayla, just a reminder that you still owe Sarah $20.00 for Weekend trip. Thanks!'
  );
  await dialog.getByRole('button', { name: 'Send reminder' }).click();
  await expect(dialog.getByRole('status')).toHaveText('Reminder sent to Kayla in SplitSpeak.');
  await dialog.getByRole('button', { name: 'Close' }).click();

  // Kayla, in her own browser session, sees the reminder.
  const kaylaContext = await browser.newContext();
  const kayla = await kaylaContext.newPage();
  await signInAs(kayla, 'Kayla');
  await kayla.getByRole('button', { name: 'Reminders (1 unread)' }).click();
  await expect(kayla.getByRole('region', { name: 'Reminders' })).toContainText(
    'you still owe Sarah $20.00 for Weekend trip'
  );
  await kaylaContext.close();

  // Sarah records the remaining $20; nobody is left to remind.
  await page.reload();
  await openWeekendTrip(page);
  await page.getByRole('button', { name: 'Settle up' }).click();
  await expect(dialog.getByLabel('Amount ($)')).toHaveValue('20.00');
  await dialog.getByRole('button', { name: 'Record payment' }).click();
  await dialog.getByRole('button', { name: 'Confirm payment' }).click();
  await expect(dialog.getByRole('status')).toHaveText('Recorded $20.00 from Kayla.');

  await dialog.getByRole('tab', { name: 'Send reminder' }).click();
  await expect(dialog.getByText('No one owes you in this group.')).toBeVisible();
  await expect(dialog.getByRole('button', { name: 'Send reminder' })).toHaveCount(0);
});
