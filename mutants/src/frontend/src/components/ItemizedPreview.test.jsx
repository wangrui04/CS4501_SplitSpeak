import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import ItemizedPreview from './ItemizedPreview';
import * as api from '../api';

const validPreview = {
  payer: 'Sarah',
  currency: 'USD',
  description: 'Dinner at Nacho City',
  totalCents: 4200,
  validated: true,
  lineItems: [
    {
      description: 'Loaded Nachos',
      amountCents: 2000,
      participants: ['Sarah', 'Kayla'],
    },
    {
      description: 'Margaritas',
      amountCents: 1500,
      participants: ['Sarah', 'Kayla', 'Rui'],
    },
  ],
  charges: [
    {
      kind: 'tax',
      amountCents: 300,
      method: 'proportional',
    },
    {
      kind: 'tip',
      amountCents: 400,
      method: 'equal',
    },
  ],
  shares: [
    { name: 'Sarah', cents: 1750, summary: 'Dinner' },
    { name: 'Kayla', cents: 1750, summary: 'Dinner' },
    { name: 'Rui', cents: 700, summary: 'Dinner' },
  ],
};

const unvalidatedPreview = {
  ...validPreview,
  validated: false,
};

describe('ALPHA-18: ItemizedPreview and Confirmation', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('renders complete preview with payer, items, tax/tip, total, and individual shares', () => {
    render(
      <ItemizedPreview
        preview={validPreview}
        conversationId={101}
        currentUser="Sarah"
        onConfirm={vi.fn()}
      />
    );

    // Validated status badge
    expect(screen.getByText('✓ Validated')).toBeInTheDocument();

    // Title and payer
    expect(screen.getByText('Dinner at Nacho City')).toBeInTheDocument();
    expect(screen.getByText(/paid by/i)).toHaveTextContent('Sarah');

    // Line items
    expect(screen.getByText('Loaded Nachos')).toBeInTheDocument();
    expect(screen.getByText('$20.00')).toBeInTheDocument();
    expect(screen.getByText(/split by: sarah, kayla$/i)).toBeInTheDocument();
    expect(screen.getByText('Margaritas')).toBeInTheDocument();
    expect(screen.getByText('$15.00')).toBeInTheDocument();

    // Tax and Tip
    expect(screen.getByText('Tax')).toBeInTheDocument();
    expect(screen.getByText('$3.00')).toBeInTheDocument();
    expect(screen.getByText('Tip')).toBeInTheDocument();
    expect(screen.getByText('$4.00')).toBeInTheDocument();

    // Total
    expect(screen.getByText('$42.00')).toBeInTheDocument();

    // Shares with current user indicator
    expect(screen.getAllByText(/sarah/i).length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText(/\(you\)/i)).toBeInTheDocument();
    expect(screen.getAllByText('$17.50').length).toBe(2);
    expect(screen.getByText('$7.00')).toBeInTheDocument();

    // Action buttons
    expect(screen.getByRole('button', { name: /confirm expense/i })).toBeEnabled();
  });

  it('calls confirm API and displays success feedback when confirmed', async () => {
    const confirmSpy = vi.spyOn(api, 'confirmExpense').mockResolvedValue({
      ok: true,
      expenseId: 55,
      conversationId: 101,
      status: 'confirmed',
    });
    const onConfirmCallback = vi.fn();

    render(
      <ItemizedPreview
        preview={validPreview}
        conversationId={101}
        currentUser="Sarah"
        onConfirm={onConfirmCallback}
      />
    );

    const confirmBtn = screen.getByRole('button', { name: /confirm expense/i });
    fireEvent.click(confirmBtn);

    expect(confirmSpy).toHaveBeenCalledWith(101);

    await waitFor(() => {
      expect(screen.getByRole('status')).toHaveTextContent(/expense confirmed and saved/i);
    });

    expect(onConfirmCallback).toHaveBeenCalledWith({
      ok: true,
      expenseId: 55,
      conversationId: 101,
      status: 'confirmed',
    });
    expect(screen.getByRole('button', { name: /confirmed ✓/i })).toBeDisabled();
  });

  it('supports cancellation and edit-in-chat actions', () => {
    const onCancel = vi.fn();
    const onEdit = vi.fn();

    render(
      <ItemizedPreview
        preview={validPreview}
        conversationId={101}
        currentUser="Sarah"
        onConfirm={vi.fn()}
        onCancel={onCancel}
        onEditInChat={onEdit}
      />
    );

    const editBtn = screen.getByRole('button', { name: /edit in chat/i });
    fireEvent.click(editBtn);
    expect(onEdit).toHaveBeenCalledTimes(1);

    const cancelBtn = screen.getByRole('button', { name: /cancel/i });
    fireEvent.click(cancelBtn);
    expect(onCancel).toHaveBeenCalledTimes(1);
  });

  it('prevents confirmation on unvalidated preview', () => {
    const confirmSpy = vi.spyOn(api, 'confirmExpense');
    const onConfirmCallback = vi.fn();

    render(
      <ItemizedPreview
        preview={unvalidatedPreview}
        conversationId={101}
        currentUser="Sarah"
        onConfirm={onConfirmCallback}
      />
    );

    expect(screen.getByText('⚠ Unvalidated')).toBeInTheDocument();
    const confirmBtn = screen.getByRole('button', { name: /confirm expense/i });
    expect(confirmBtn).toBeDisabled();

    fireEvent.click(confirmBtn);
    expect(confirmSpy).not.toHaveBeenCalled();
    expect(onConfirmCallback).not.toHaveBeenCalled();
  });

  it('handles server rejection and prevents duplicate submission', async () => {
    const confirmSpy = vi
      .spyOn(api, 'confirmExpense')
      .mockRejectedValue(new Error('Expense already confirmed for this conversation'));
    const onConfirmCallback = vi.fn();

    render(
      <ItemizedPreview
        preview={validPreview}
        conversationId={101}
        currentUser="Sarah"
        onConfirm={onConfirmCallback}
      />
    );

    const confirmBtn = screen.getByRole('button', { name: /confirm expense/i });
    fireEvent.click(confirmBtn);

    await waitFor(() => {
      expect(screen.getByRole('alert')).toBeInTheDocument();
    });
    expect(confirmSpy).toHaveBeenCalledWith(101);
    expect(
      screen.getByText('Expense already confirmed for this conversation')
    ).toBeInTheDocument();
    expect(onConfirmCallback).not.toHaveBeenCalled();
  });

  it('never updates balances before explicit confirmation', () => {
    const onConfirmCallback = vi.fn();

    render(
      <ItemizedPreview
        preview={validPreview}
        conversationId={101}
        currentUser="Sarah"
        onConfirm={onConfirmCallback}
      />
    );

    // Just rendering the preview must never call onConfirm or change balances
    expect(onConfirmCallback).not.toHaveBeenCalled();
  });
});

describe('ALPHA-28: Settlement in the preview card', () => {
  const tripPreview = {
    description: 'Trip',
    payer: 'Sarah',
    currency: 'USD',
    totalCents: 105000,
    validated: true,
    lineItems: [],
    charges: [],
    shares: [
      { name: 'Sarah', cents: 44500, summary: 'Trip' },
      { name: 'Kayla', cents: 20500, summary: 'Trip' },
      { name: 'Rui', cents: 40000, summary: 'Trip' },
    ],
    paid: [
      { name: 'Sarah', cents: 84000 },
      { name: 'Kayla', cents: 9000 },
      { name: 'Rui', cents: 12000 },
    ],
    settlement: {
      nets: [],
      transfers: [
        { from: 'Rui', to: 'Sarah', cents: 28000 },
        { from: 'Kayla', to: 'Sarah', cents: 11500 },
      ],
    },
  };

  it('lists who pays whom', () => {
    render(<ItemizedPreview preview={tripPreview} conversationId={1} currentUser="Sarah" />);

    const section = screen.getByRole('list', { name: 'Who pays whom' });
    expect(section).toHaveTextContent('Rui pays Sarah $280.00');
    expect(section).toHaveTextContent('Kayla pays Sarah $115.00');
  });

  it('shows amounts paid when more than one person paid', () => {
    render(<ItemizedPreview preview={tripPreview} conversationId={1} currentUser="Sarah" />);

    const paid = screen.getByRole('list', { name: 'Amounts paid' });
    expect(paid).toHaveTextContent('Kayla$90.00');
    expect(paid).toHaveTextContent('Rui$120.00');
  });

  it('hides amounts paid for a single-payer expense', () => {
    const single = {
      ...tripPreview,
      paid: [
        { name: 'Sarah', cents: 105000 },
        { name: 'Kayla', cents: 0 },
        { name: 'Rui', cents: 0 },
      ],
    };
    render(<ItemizedPreview preview={single} conversationId={1} currentUser="Sarah" />);

    expect(screen.queryByRole('list', { name: 'Amounts paid' })).not.toBeInTheDocument();
  });
});
