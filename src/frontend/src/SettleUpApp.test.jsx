import { render, screen, fireEvent, waitFor, within } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import App from './App';
import * as api from './api';

// #46: the Settle up button, refreshing after a payment, payment
// history, and the reminders inbox, wired into the main page.

const groups = [{ id: 1, name: 'Apartment 4B', members: ['Sarah', 'Kayla', 'Rui'] }];

function details(owedCents) {
  const transfers = owedCents ? [{ from: 'Kayla', to: 'Sarah', cents: owedCents }] : [];
  return {
    ...groups[0],
    nets: [],
    transfers,
    balances: [
      { name: 'Kayla', cents: owedCents, status: owedCents ? 'owes you' : 'settled up' },
      { name: 'Rui', cents: 0, status: 'settled up' },
    ],
    summary: { totalBalance: owedCents, youOwe: 0, youAreOwed: owedCents },
  };
}

const reminder = {
  id: 5,
  groupId: 1,
  from: 'Sarah',
  to: 'Kayla',
  cents: 2000,
  message: 'Hi Kayla, just a reminder that you still owe Sarah $20.00 for Apartment 4B. Thanks!',
  createdAt: '2026-11-10T13:00:00+00:00',
  readAt: null,
};

function signInAs(name, { notifications = [], settlements = [] } = {}) {
  vi.spyOn(api, 'fetchSession').mockResolvedValue({ name });
  vi.spyOn(api, 'fetchGroups').mockResolvedValue(groups);
  vi.spyOn(api, 'fetchGroupExpenses').mockResolvedValue([]);
  vi.spyOn(api, 'fetchSettlements').mockResolvedValue(settlements);
  vi.spyOn(api, 'fetchNotifications').mockResolvedValue(notifications);
}

describe('#46: Settle up on the group page', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('opens the Settle up dialog with the group transfers', async () => {
    signInAs('Sarah');
    vi.spyOn(api, 'fetchGroup').mockResolvedValue(details(3000));
    render(<App />);

    fireEvent.click(await screen.findByRole('button', { name: 'Settle up' }));

    const dialog = screen.getByRole('dialog', { name: 'Settle up' });
    expect(within(dialog).getByRole('radio', { name: 'Kayla owes you $30.00' })).toBeChecked();
  });

  it('refreshes balances and history after recording a payment', async () => {
    signInAs('Sarah');
    const fetchGroup = vi.spyOn(api, 'fetchGroup')
      .mockResolvedValueOnce(details(3000))
      .mockResolvedValue(details(2000));
    vi.spyOn(api, 'recordSettlement').mockResolvedValue({ remainingCents: 2000 });
    render(<App />);

    fireEvent.click(await screen.findByRole('button', { name: 'Settle up' }));
    fireEvent.change(screen.getByLabelText('Amount ($)'), { target: { value: '10' } });
    fireEvent.click(screen.getByRole('button', { name: 'Record payment' }));
    fireEvent.click(screen.getByRole('button', { name: 'Confirm payment' }));

    await waitFor(() => expect(fetchGroup.mock.calls.length).toBeGreaterThan(1));
    expect(api.fetchSettlements.mock.calls.length).toBeGreaterThan(1);
  });

  it('shows recorded payments on the group page', async () => {
    signInAs('Sarah', {
      settlements: [{
        id: 1,
        from: 'Kayla',
        to: 'Sarah',
        cents: 1000,
        recordedBy: 'Sarah',
        recordedAt: '2026-11-10T12:00:00+00:00',
      }],
    });
    vi.spyOn(api, 'fetchGroup').mockResolvedValue(details(2000));
    render(<App />);

    const payments = await screen.findByRole('region', { name: 'Payments' });
    expect(payments).toHaveTextContent('Kayla paid Sarah $10.00');
  });

  it('shows unread reminders to the recipient and marks them read', async () => {
    signInAs('Kayla', { notifications: [reminder] });
    vi.spyOn(api, 'fetchGroup').mockResolvedValue(details(0));
    const markRead = vi.spyOn(api, 'markNotificationRead').mockResolvedValue({ ok: true });
    render(<App />);

    fireEvent.click(await screen.findByRole('button', { name: 'Reminders (1 unread)' }));

    const inbox = screen.getByRole('region', { name: 'Reminders' });
    expect(inbox).toHaveTextContent('you still owe Sarah $20.00');

    fireEvent.click(within(inbox).getByRole('button', { name: 'Mark as read' }));
    await waitFor(() => expect(markRead).toHaveBeenCalledWith(5));
  });

  it('still loads the page if reminders cannot be fetched', async () => {
    signInAs('Sarah');
    vi.spyOn(api, 'fetchNotifications').mockRejectedValue(new Error('offline'));
    vi.spyOn(api, 'fetchGroup').mockResolvedValue(details(3000));
    render(<App />);

    expect(await screen.findByRole('heading', { level: 1, name: 'Apartment 4B' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Settle up' })).toBeInTheDocument();
  });
});
