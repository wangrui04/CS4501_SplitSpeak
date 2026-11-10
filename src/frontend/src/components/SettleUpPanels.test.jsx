import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import SettlementHistory from './SettlementHistory';
import RemindersInbox from './RemindersInbox';

describe('#46: Payment history', () => {
  const settlements = [
    {
      id: 2,
      from: 'Kayla',
      to: 'Sarah',
      cents: 2000,
      recordedBy: 'Sarah',
      recordedAt: '2026-11-10T13:00:00+00:00',
    },
    {
      id: 1,
      from: 'Kayla',
      to: 'Sarah',
      cents: 1000,
      recordedBy: 'Sarah',
      recordedAt: '2026-11-10T12:00:00+00:00',
    },
  ];

  it('lists each payment with amount, people, recorder, and time', () => {
    render(<SettlementHistory settlements={settlements} />);

    const region = screen.getByRole('region', { name: 'Payments' });
    const items = region.querySelectorAll('li');
    expect(items).toHaveLength(2);
    expect(items[0]).toHaveTextContent('Kayla paid Sarah $20.00');
    expect(items[0]).toHaveTextContent('Recorded by Sarah');
    expect(items[0].querySelector('time')).toHaveAttribute(
      'datetime',
      '2026-11-10T13:00:00+00:00'
    );
    expect(items[1]).toHaveTextContent('Kayla paid Sarah $10.00');
  });

  it('shows an empty state', () => {
    render(<SettlementHistory settlements={[]} />);

    expect(screen.getByText('No payments recorded yet.')).toBeInTheDocument();
  });
});

describe('#46: Reminders inbox', () => {
  const notifications = [
    {
      id: 5,
      groupId: 1,
      from: 'Sarah',
      to: 'Kayla',
      cents: 2000,
      message: 'Hi Kayla, just a reminder that you still owe Sarah $20.00 for Apartment 4B. Thanks!',
      createdAt: '2026-11-10T13:00:00+00:00',
      readAt: null,
    },
    {
      id: 4,
      groupId: 1,
      from: 'Rui',
      to: 'Kayla',
      cents: 500,
      message: 'Hi Kayla, just a reminder that you still owe Rui $5.00 for Apartment 4B. Thanks!',
      createdAt: '2026-11-09T09:00:00+00:00',
      readAt: '2026-11-09T10:00:00+00:00',
    },
  ];

  it('shows each reminder with its sender', () => {
    render(<RemindersInbox notifications={notifications} onMarkRead={vi.fn()} />);

    const region = screen.getByRole('region', { name: 'Reminders' });
    expect(region).toHaveTextContent('you still owe Sarah $20.00');
    expect(region).toHaveTextContent('From Sarah');
    expect(region).toHaveTextContent('From Rui');
  });

  it('marks an unread reminder as read', () => {
    const onMarkRead = vi.fn();
    render(<RemindersInbox notifications={notifications} onMarkRead={onMarkRead} />);

    const buttons = screen.getAllByRole('button', { name: 'Mark as read' });
    expect(buttons).toHaveLength(1);

    fireEvent.click(buttons[0]);
    expect(onMarkRead).toHaveBeenCalledWith(5);
  });

  it('shows an empty state', () => {
    render(<RemindersInbox notifications={[]} onMarkRead={vi.fn()} />);

    expect(screen.getByText('No reminders')).toBeInTheDocument();
  });
});
