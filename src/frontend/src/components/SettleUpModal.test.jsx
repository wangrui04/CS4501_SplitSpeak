import { render, screen, fireEvent, waitFor, within } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import SettleUpModal from './SettleUpModal';
import * as api from '../api';

// #46: only the person being paid records a payment, and the form
// sends the amount it showed so a stale form is rejected.

const group = {
  id: 1,
  name: 'Apartment 4B',
  members: ['Sarah', 'Kayla', 'Rui'],
  transfers: [
    { from: 'Kayla', to: 'Sarah', cents: 3000 },
    { from: 'Rui', to: 'Sarah', cents: 1250 },
  ],
};

function renderModal(props = {}) {
  const onClose = vi.fn();
  const onRecorded = vi.fn();
  const utils = render(
    <SettleUpModal
      isOpen
      onClose={onClose}
      onRecorded={onRecorded}
      group={group}
      currentUser="Sarah"
      {...props}
    />
  );
  return { ...utils, onClose, onRecorded };
}

function amountInput() {
  return screen.getByLabelText('Amount ($)');
}

function openReminderTab() {
  fireEvent.click(screen.getByRole('tab', { name: 'Send reminder' }));
}

describe('#46: Settle up dialog', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('renders nothing when closed', () => {
    renderModal({ isOpen: false });

    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  });

  it('opens on the Record payment tab', () => {
    renderModal();

    expect(screen.getByRole('dialog', { name: 'Settle up' })).toBeInTheDocument();
    expect(screen.getByRole('tab', { name: 'Record payment' })).toHaveAttribute('aria-selected', 'true');
    expect(screen.getByRole('tab', { name: 'Send reminder' })).toHaveAttribute('aria-selected', 'false');
  });

  it('closes from the close button', () => {
    const { onClose } = renderModal();

    fireEvent.click(screen.getByRole('button', { name: 'Close' }));

    expect(onClose).toHaveBeenCalled();
  });
});

describe('#46: Record payment', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('lists only people who owe the signed-in user, with amounts', () => {
    renderModal({
      group: {
        ...group,
        transfers: [
          { from: 'Kayla', to: 'Sarah', cents: 3000 },
          { from: 'Sarah', to: 'Rui', cents: 500 }, // Sarah owes Rui
          { from: 'Rui', to: 'Kayla', cents: 700 }, // not involving Sarah
        ],
      },
    });

    const options = screen.getAllByRole('radio');
    expect(options).toHaveLength(1);
    expect(screen.getByRole('radio', { name: 'Kayla owes you $30.00' })).toBeChecked();
  });

  it('defaults the amount to the full outstanding balance', () => {
    renderModal();

    expect(amountInput()).toHaveValue('30.00');

    fireEvent.click(screen.getByRole('radio', { name: 'Rui owes you $12.50' }));
    expect(amountInput()).toHaveValue('12.50');
  });

  it('Full payment restores the outstanding amount after editing', () => {
    renderModal();

    fireEvent.change(amountInput(), { target: { value: '5' } });
    fireEvent.click(screen.getByRole('button', { name: 'Full payment' }));

    expect(amountInput()).toHaveValue('30.00');
  });

  it('asks for confirmation and says no money is moved', () => {
    const spy = vi.spyOn(api, 'recordSettlement');
    renderModal();

    fireEvent.change(amountInput(), { target: { value: '10' } });
    fireEvent.click(screen.getByRole('button', { name: 'Record payment' }));

    expect(screen.getByText('Record Kayla paying you $10.00?')).toBeInTheDocument();
    expect(
      screen.getByText('This records a payment only; SplitSpeak does not transfer money.')
    ).toBeInTheDocument();
    expect(spy).not.toHaveBeenCalled();
  });

  it('Back returns to the form without recording', () => {
    const spy = vi.spyOn(api, 'recordSettlement');
    renderModal();

    fireEvent.click(screen.getByRole('button', { name: 'Record payment' }));
    fireEvent.click(screen.getByRole('button', { name: 'Back' }));

    expect(amountInput()).toHaveValue('30.00');
    expect(spy).not.toHaveBeenCalled();
  });

  it('records a partial payment with the shown balance, then refreshes', async () => {
    const spy = vi.spyOn(api, 'recordSettlement').mockResolvedValue({
      id: 7,
      from: 'Kayla',
      to: 'Sarah',
      cents: 1000,
      remainingCents: 2000,
    });
    const { onRecorded } = renderModal();

    fireEvent.change(amountInput(), { target: { value: '10' } });
    fireEvent.click(screen.getByRole('button', { name: 'Record payment' }));
    fireEvent.click(screen.getByRole('button', { name: 'Confirm payment' }));

    await waitFor(() => {
      expect(screen.getByRole('status')).toHaveTextContent('Recorded $10.00 from Kayla.');
    });
    expect(spy).toHaveBeenCalledWith(1, {
      from: 'Kayla',
      to: 'Sarah',
      cents: 1000,
      expectedOutstandingCents: 3000,
    });
    expect(onRecorded).toHaveBeenCalled();
  });

  it('records the full amount when unchanged', async () => {
    const spy = vi.spyOn(api, 'recordSettlement').mockResolvedValue({ remainingCents: 0 });
    renderModal();

    fireEvent.click(screen.getByRole('button', { name: 'Record payment' }));
    fireEvent.click(screen.getByRole('button', { name: 'Confirm payment' }));

    await waitFor(() => expect(spy).toHaveBeenCalled());
    expect(spy.mock.calls[0][1]).toMatchObject({ cents: 3000, expectedOutstandingCents: 3000 });
  });

  it('converts amounts with string math, not floats', async () => {
    const spy = vi.spyOn(api, 'recordSettlement').mockResolvedValue({ remainingCents: 1 });
    renderModal();

    fireEvent.change(amountInput(), { target: { value: '29.99' } });
    fireEvent.click(screen.getByRole('button', { name: 'Record payment' }));
    fireEvent.click(screen.getByRole('button', { name: 'Confirm payment' }));

    await waitFor(() => expect(spy).toHaveBeenCalled());
    expect(spy.mock.calls[0][1].cents).toBe(2999);
  });

  it.each(['', '0', '0.00', 'abc', '-5', '1.234'])(
    'rejects the amount "%s" without calling the API',
    (value) => {
      const spy = vi.spyOn(api, 'recordSettlement');
      renderModal();

      fireEvent.change(amountInput(), { target: { value } });
      fireEvent.click(screen.getByRole('button', { name: 'Record payment' }));

      expect(screen.getByRole('alert')).toHaveTextContent('Enter an amount greater than $0.00');
      expect(spy).not.toHaveBeenCalled();
    }
  );

  it('rejects more than is owed without calling the API', () => {
    const spy = vi.spyOn(api, 'recordSettlement');
    renderModal();

    fireEvent.change(amountInput(), { target: { value: '30.01' } });
    fireEvent.click(screen.getByRole('button', { name: 'Record payment' }));

    expect(screen.getByRole('alert')).toHaveTextContent('Amount is more than the $30.00 owed');
    expect(spy).not.toHaveBeenCalled();
  });

  it('shows the server message when the balance changed', async () => {
    const error = Object.assign(new Error('Balance changed, please refresh'), { status: 409 });
    vi.spyOn(api, 'recordSettlement').mockRejectedValue(error);
    const { onRecorded } = renderModal();

    fireEvent.click(screen.getByRole('button', { name: 'Record payment' }));
    fireEvent.click(screen.getByRole('button', { name: 'Confirm payment' }));

    await waitFor(() => {
      expect(screen.getByRole('alert')).toHaveTextContent('Balance changed, please refresh');
    });
    expect(onRecorded).not.toHaveBeenCalled();
  });

  it('records once even if Confirm is clicked twice', async () => {
    let resolve;
    const spy = vi.spyOn(api, 'recordSettlement').mockReturnValue(
      new Promise((done) => { resolve = done; })
    );
    renderModal();

    fireEvent.click(screen.getByRole('button', { name: 'Record payment' }));
    const confirm = screen.getByRole('button', { name: 'Confirm payment' });
    fireEvent.click(confirm);
    fireEvent.click(confirm);

    expect(spy).toHaveBeenCalledTimes(1);
    resolve({ remainingCents: 0 });
    await waitFor(() => expect(screen.getByRole('status')).toBeInTheDocument());
  });

  it('closing and reopening does not record anything', () => {
    const spy = vi.spyOn(api, 'recordSettlement');
    const { rerender } = renderModal();

    rerender(<SettleUpModal isOpen={false} onClose={vi.fn()} group={group} currentUser="Sarah" />);
    rerender(<SettleUpModal isOpen onClose={vi.fn()} group={group} currentUser="Sarah" />);

    expect(spy).not.toHaveBeenCalled();
    expect(amountInput()).toHaveValue('30.00');
  });

  it('shows an empty state when no one owes the user', () => {
    renderModal({ currentUser: 'Kayla' });

    expect(screen.getByText('No one owes you in this group.')).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Record payment' })).not.toBeInTheDocument();
  });
});

describe('#46: Send reminder', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('lists only people who owe the signed-in user', () => {
    renderModal();
    openReminderTab();

    expect(screen.getByRole('radio', { name: 'Kayla owes you $30.00' })).toBeChecked();
    expect(screen.getByRole('radio', { name: 'Rui owes you $12.50' })).toBeInTheDocument();
    expect(screen.getAllByRole('radio')).toHaveLength(2);
  });

  it('previews a polite message with the live amount', () => {
    renderModal();
    openReminderTab();

    const preview = screen.getByRole('region', { name: 'Reminder preview' });
    expect(preview).toHaveTextContent(
      'Hi Kayla, just a reminder that you still owe Sarah $30.00 for Apartment 4B. Thanks!'
    );

    fireEvent.click(screen.getByRole('radio', { name: 'Rui owes you $12.50' }));
    expect(preview).toHaveTextContent('you still owe Sarah $12.50');
  });

  it('says it is delivered in SplitSpeak, not by email or text', () => {
    renderModal();
    openReminderTab();

    expect(
      screen.getByText('Kayla will see this in SplitSpeak. No email or text is sent.')
    ).toBeInTheDocument();
  });

  it('sends the reminder and shows who it went to', async () => {
    const spy = vi.spyOn(api, 'sendReminder').mockResolvedValue({ id: 3, to: 'Kayla', cents: 3000 });
    renderModal();
    openReminderTab();

    fireEvent.click(screen.getByRole('button', { name: 'Send reminder' }));

    await waitFor(() => {
      expect(screen.getByRole('status')).toHaveTextContent('Reminder sent to Kayla in SplitSpeak.');
    });
    expect(spy).toHaveBeenCalledWith(1, 'Kayla');
  });

  it('sends once even if clicked twice', () => {
    const spy = vi.spyOn(api, 'sendReminder').mockReturnValue(new Promise(() => {}));
    renderModal();
    openReminderTab();

    const send = screen.getByRole('button', { name: 'Send reminder' });
    fireEvent.click(send);
    fireEvent.click(send);

    expect(spy).toHaveBeenCalledTimes(1);
  });

  it('shows the cooldown message from the server', async () => {
    const error = Object.assign(
      new Error('You already reminded Kayla in the last 60 minutes'),
      { status: 429 }
    );
    vi.spyOn(api, 'sendReminder').mockRejectedValue(error);
    renderModal();
    openReminderTab();

    fireEvent.click(screen.getByRole('button', { name: 'Send reminder' }));

    await waitFor(() => {
      expect(screen.getByRole('alert')).toHaveTextContent(
        'You already reminded Kayla in the last 60 minutes'
      );
    });
    expect(screen.queryByRole('status')).not.toBeInTheDocument();
  });

  it('copies the message for sharing outside the app', async () => {
    const writeText = vi.fn().mockResolvedValue();
    Object.defineProperty(navigator, 'clipboard', { value: { writeText }, configurable: true });
    const spy = vi.spyOn(api, 'sendReminder');
    renderModal();
    openReminderTab();

    fireEvent.click(screen.getByRole('button', { name: 'Copy message' }));

    await waitFor(() => expect(screen.getByRole('status')).toHaveTextContent('Message copied'));
    expect(writeText).toHaveBeenCalledWith(
      'Hi Kayla, just a reminder that you still owe Sarah $30.00 for Apartment 4B. Thanks!'
    );
    expect(spy).not.toHaveBeenCalled();
  });

  it('shows an empty state when no one owes the user', () => {
    renderModal({ currentUser: 'Rui' });
    openReminderTab();

    const panel = screen.getByRole('tabpanel');
    expect(within(panel).getByText('No one owes you in this group.')).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Send reminder' })).not.toBeInTheDocument();
  });
});
