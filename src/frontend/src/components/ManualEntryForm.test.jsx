import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import ManualEntryForm from './ManualEntryForm';
import * as api from '../api';

const group = { id: 1, name: 'Apartment 4B', members: ['Sarah', 'Kayla', 'Rui'] };

function renderForm(props = {}) {
  const onSaved = vi.fn();
  const onCancel = vi.fn();
  render(
    <ManualEntryForm
      group={group}
      currentUser="Sarah"
      onSaved={onSaved}
      onCancel={onCancel}
      {...props}
    />
  );
  return { onSaved, onCancel };
}

function fill(description, amount) {
  fireEvent.change(screen.getByLabelText('Description'), { target: { value: description } });
  fireEvent.change(screen.getByLabelText('Amount ($)'), { target: { value: amount } });
}

describe('ALPHA-27: Manual-entry form', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('matches the layout and defaults', () => {
    renderForm();

    expect(screen.getByText('Add an expense the usual way.')).toBeInTheDocument();
    expect(screen.getByLabelText('Description')).toHaveAttribute('placeholder', 'e.g. Dinner');
    expect(screen.getByLabelText('Amount ($)')).toHaveAttribute('placeholder', '0.00');
    expect(screen.getByLabelText('Paid by')).toHaveValue('Sarah');
    expect(screen.getByText('Split equally between')).toBeInTheDocument();
    for (const name of group.members) {
      expect(screen.getByRole('checkbox', { name })).toBeChecked();
    }
    expect(screen.getByRole('button', { name: 'Cancel' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Save expense' })).toBeDisabled();
  });

  it('defaults Paid by to the current user', () => {
    renderForm({ currentUser: 'Kayla' });

    expect(screen.getByLabelText('Paid by')).toHaveValue('Kayla');
  });

  it('builds payer options and checkboxes from the group, not a hardcoded list', () => {
    renderForm({ group: { id: 2, name: 'Trip', members: ['Sarah', 'Aly', 'Ben'] } });

    expect(screen.getByRole('checkbox', { name: 'Ben' })).toBeChecked();
    expect(screen.queryByRole('checkbox', { name: 'Kayla' })).not.toBeInTheDocument();
    expect(screen.getAllByRole('option').map((o) => o.textContent)).toEqual(['Sarah', 'Aly', 'Ben']);
  });

  it.each(['abc', '12.345', '1.2.3', '-5'])('shows an error for invalid amount %s', (amount) => {
    renderForm();
    fill('Dinner', amount);

    expect(screen.getByText(/digits and up to 2 decimals/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Save expense' })).toBeDisabled();
  });

  it('rejects a zero amount', () => {
    renderForm();
    fill('Dinner', '0.00');

    expect(screen.getByText(/greater than \$0/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Save expense' })).toBeDisabled();
  });

  it('shows an error when everyone is unchecked', () => {
    renderForm();
    fill('Dinner', '30');
    for (const name of group.members) {
      fireEvent.click(screen.getByRole('checkbox', { name }));
    }

    expect(screen.getByText(/at least one person/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Save expense' })).toBeDisabled();
  });

  it('enables Save once the form is valid', () => {
    renderForm();
    fill('Dinner', '30');

    expect(screen.getByRole('button', { name: 'Save expense' })).toBeEnabled();
  });

  it('submits the correct payload and reports success', async () => {
    const saveSpy = vi.spyOn(api, 'createManualExpense').mockResolvedValue({ ok: true, expenseId: 9 });
    const { onSaved } = renderForm();

    fill('  Coffee & Donuts ', '15.5');
    fireEvent.click(screen.getByRole('checkbox', { name: 'Rui' }));
    fireEvent.change(screen.getByLabelText('Paid by'), { target: { value: 'Kayla' } });
    fireEvent.click(screen.getByRole('button', { name: 'Save expense' }));

    await waitFor(() => expect(onSaved).toHaveBeenCalled());
    expect(saveSpy).toHaveBeenCalledWith(1, {
      description: 'Coffee & Donuts',
      amount: '15.5',
      paidBy: 'Kayla',
      splitBetween: ['Sarah', 'Kayla'],
    });
  });

  it('shows the server message on a 400', async () => {
    const error = Object.assign(new Error('Unknown member Kayla'), { status: 400 });
    vi.spyOn(api, 'createManualExpense').mockRejectedValue(error);
    const { onSaved } = renderForm();

    fill('Dinner', '30');
    fireEvent.click(screen.getByRole('button', { name: 'Save expense' }));

    expect(await screen.findByRole('alert')).toHaveTextContent('Unknown member Kayla');
    expect(onSaved).not.toHaveBeenCalled();
  });

  it('prefills the description but never the amount', () => {
    renderForm({ initialDescription: 'nachos for me and kayla' });

    expect(screen.getByLabelText('Description')).toHaveValue('nachos for me and kayla');
    expect(screen.getByLabelText('Amount ($)')).toHaveValue('');
  });

  it('calls onCancel', () => {
    const { onCancel } = renderForm();

    fireEvent.click(screen.getByRole('button', { name: 'Cancel' }));

    expect(onCancel).toHaveBeenCalled();
  });
});
