import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import AddExpenseModal from './AddExpenseModal';
import * as api from '../api';

const mockGroup = {
  id: 1,
  name: 'Apartment 4B',
  members: ['Sarah', 'Kayla', 'Rui'],
};

describe('ALPHA-17: AddExpenseModal with AI Chat', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
    window.HTMLElement.prototype.scrollIntoView = vi.fn();
  });

  it('renders modal dialog with AI chat as default tab and switches tabs', () => {
    render(
      <AddExpenseModal
        isOpen={true}
        onClose={vi.fn()}
        group={mockGroup}
        currentUser="Sarah"
      />
    );

    expect(screen.getByRole('dialog', { name: /add an expense/i })).toBeInTheDocument();
    expect(screen.getByRole('tab', { name: /ai assistant/i })).toHaveAttribute('aria-selected', 'true');
    expect(screen.getByPlaceholderText(/e\.g\. kayla and i shared nachos/i)).toBeInTheDocument();

    // Switch to Manual tab
    const manualTab = screen.getByRole('tab', { name: /manual entry/i });
    fireEvent.click(manualTab);

    expect(manualTab).toHaveAttribute('aria-selected', 'true');
    expect(screen.getByLabelText(/description/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/amount/i)).toBeInTheDocument();
  });

  it('submits a message, displays loading state, and renders clarification question', async () => {
    const chatSpy = vi.spyOn(api, 'sendChatMessage').mockResolvedValue({
      type: 'question',
      question: 'How much were the nachos and did everyone have drinks?',
      conversationId: 42,
      promptCount: 1,
      status: 'pending',
    });

    render(
      <AddExpenseModal
        isOpen={true}
        onClose={vi.fn()}
        group={mockGroup}
        currentUser="Sarah"
      />
    );

    const input = screen.getByPlaceholderText(/e\.g\. kayla and i shared nachos/i);
    const sendBtn = screen.getByRole('button', { name: /send/i });

    // Type and send message
    fireEvent.change(input, {
      target: { value: 'Kayla and I shared nachos at dinner.' },
    });
    fireEvent.click(sendBtn);

    // API called with group ID and text
    expect(chatSpy).toHaveBeenCalledWith({
      groupId: 1,
      conversationId: null,
      message: 'Kayla and I shared nachos at dinner.',
    });

    // User message visible in history
    expect(screen.getByText('Kayla and I shared nachos at dinner.')).toBeInTheDocument();

    // Assistant clarification question rendered
    await waitFor(() => {
      expect(
        screen.getByText('How much were the nachos and did everyone have drinks?')
      ).toBeInTheDocument();
    });

    // Prompt counter updated
    expect(screen.getByLabelText(/prompt count: 1 of 5/i)).toBeInTheDocument();
  });

  it('handles multi-turn conversation and renders validated preview', async () => {
    const chatSpy = vi
      .spyOn(api, 'sendChatMessage')
      .mockResolvedValueOnce({
        type: 'question',
        question: 'How much was total and did Sarah pay?',
        conversationId: 99,
        promptCount: 1,
        status: 'pending',
      })
      .mockResolvedValueOnce({
        type: 'preview',
        conversationId: 99,
        promptCount: 2,
        status: 'preview',
        preview: {
          payer: 'Sarah',
          total_cents: 3000,
          currency: 'USD',
          items: [
            {
              description: 'Nachos',
              amount_cents: 3000,
              participants: ['Sarah', 'Kayla'],
            },
          ],
          shares: {
            Sarah: 1500,
            Kayla: 1500,
          },
        },
      });

    render(
      <AddExpenseModal
        isOpen={true}
        onClose={vi.fn()}
        group={mockGroup}
        currentUser="Sarah"
      />
    );

    const input = screen.getByPlaceholderText(/e\.g\. kayla and i shared nachos/i);
    const sendBtn = screen.getByRole('button', { name: /send/i });

    // Turn 1
    fireEvent.change(input, { target: { value: 'Nachos for Sarah and Kayla' } });
    fireEvent.click(sendBtn);

    await waitFor(() => {
      expect(screen.getByText('How much was total and did Sarah pay?')).toBeInTheDocument();
    });

    // Turn 2
    fireEvent.change(input, { target: { value: 'It was $30 and Sarah paid.' } });
    fireEvent.click(sendBtn);

    expect(chatSpy).toHaveBeenLastCalledWith({
      groupId: 1,
      conversationId: 99,
      message: 'It was $30 and Sarah paid.',
    });

    // Preview rendered
    await waitFor(() => {
      expect(screen.getByTestId('itemized-preview')).toBeInTheDocument();
      expect(screen.getAllByText('$30.00').length).toBeGreaterThanOrEqual(1);
      expect(screen.getAllByText('Nachos').length).toBeGreaterThanOrEqual(1);
    });
    expect(screen.getByLabelText(/prompt count: 2 of 5/i)).toBeInTheDocument();
  });

  it('handles API errors with error banner and retry option', async () => {
    const chatSpy = vi
      .spyOn(api, 'sendChatMessage')
      .mockRejectedValueOnce(new Error('Network connection timeout'))
      .mockResolvedValueOnce({
        type: 'question',
        question: 'Who paid for the groceries?',
        conversationId: 50,
        promptCount: 1,
        status: 'pending',
      });

    render(
      <AddExpenseModal
        isOpen={true}
        onClose={vi.fn()}
        group={mockGroup}
        currentUser="Sarah"
      />
    );

    const input = screen.getByPlaceholderText(/e\.g\. kayla and i shared nachos/i);
    const sendBtn = screen.getByRole('button', { name: /send/i });

    fireEvent.change(input, { target: { value: 'Groceries split equally' } });
    fireEvent.click(sendBtn);

    // Error alert displayed
    await waitFor(() => {
      expect(screen.getByRole('alert')).toBeInTheDocument();
    });
    expect(screen.getByText(/network connection timeout/i)).toBeInTheDocument();

    // Click retry
    const retryBtn = screen.getByRole('button', { name: /retry/i });
    fireEvent.click(retryBtn);

    await waitFor(() => {
      expect(screen.getByText('Who paid for the groceries?')).toBeInTheDocument();
    });
    expect(chatSpy).toHaveBeenCalledTimes(2);
  });

  it('enforces maximum prompt limit and provides manual entry fallback', async () => {
    vi.spyOn(api, 'sendChatMessage').mockResolvedValue({
      type: 'unresolved',
      reason: 'Prompt limit exceeded (maximum 5 prompts). Please enter this expense manually.',
      conversationId: 88,
      promptCount: 5,
      status: 'unsuccessful',
      fallback: 'manual',
    });

    render(
      <AddExpenseModal
        isOpen={true}
        onClose={vi.fn()}
        group={mockGroup}
        currentUser="Sarah"
      />
    );

    const input = screen.getByPlaceholderText(/e\.g\. kayla and i shared nachos/i);
    const sendBtn = screen.getByRole('button', { name: /send/i });

    fireEvent.change(input, { target: { value: 'Still trying to resolve...' } });
    fireEvent.click(sendBtn);

    await waitFor(() => {
      expect(screen.getByText(/maximum prompt limit \(5\) reached/i)).toBeInTheDocument();
    });

    // Input is now disabled
    expect(input).toBeDisabled();
    expect(sendBtn).toBeDisabled();

    // Click "Enter expense manually"
    const fallbackBtn = screen.getAllByRole('button', { name: /enter expense manually|switch to manual entry/i })[0];
    fireEvent.click(fallbackBtn);

    // Switches to manual entry tab
    expect(screen.getByRole('tab', { name: /manual entry/i })).toHaveAttribute('aria-selected', 'true');
    expect(screen.getByLabelText(/description/i)).toBeInTheDocument();
  });

  it('supports quick example buttons', async () => {
    const chatSpy = vi.spyOn(api, 'sendChatMessage').mockResolvedValue({
      type: 'question',
      question: 'How much were the groceries?',
      conversationId: 10,
      promptCount: 1,
    });

    render(
      <AddExpenseModal
        isOpen={true}
        onClose={vi.fn()}
        group={mockGroup}
        currentUser="Sarah"
      />
    );

    const groceryBtn = screen.getByRole('button', { name: /try groceries/i });
    fireEvent.click(groceryBtn);

    await waitFor(() => {
      expect(chatSpy).toHaveBeenCalledWith({
        groupId: 1,
        conversationId: null,
        message: 'I paid $36 for groceries, split between everyone except Rui.',
      });
      expect(screen.getByText('How much were the groceries?')).toBeInTheDocument();
    });
  });

  it('supports manual expense form submission with validation', async () => {
    const onConfirmSpy = vi.fn();
    const onCloseSpy = vi.fn();

    render(
      <AddExpenseModal
        isOpen={true}
        onClose={onCloseSpy}
        group={mockGroup}
        currentUser="Sarah"
        onExpenseConfirmed={onConfirmSpy}
      />
    );

    // Switch to manual tab
    fireEvent.click(screen.getByRole('tab', { name: /manual entry/i }));

    const descInput = screen.getByLabelText(/description/i);
    const amountInput = screen.getByLabelText(/amount/i);
    const saveBtn = screen.getByRole('button', { name: /save expense/i });

    // Submit empty fails
    fireEvent.click(saveBtn);
    expect(screen.getByText(/please provide a description/i)).toBeInTheDocument();

    // Fill valid data
    fireEvent.change(descInput, { target: { value: 'Coffee & Donuts' } });
    fireEvent.change(amountInput, { target: { value: '15.50' } });
    fireEvent.click(saveBtn);

    expect(onConfirmSpy).toHaveBeenCalledWith({
      description: 'Coffee & Donuts',
      payer: 'Sarah',
      amount_cents: 1550,
      participants: ['Sarah', 'Kayla', 'Rui'],
    });
  });
});
