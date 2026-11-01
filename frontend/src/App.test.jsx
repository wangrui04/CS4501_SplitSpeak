import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import App from './App';
import * as api from './api';

const mockGroups = [
  {
    id: 1,
    name: 'Apartment 4B',
    members: ['Sarah', 'Kayla', 'Rui'],
  },
  {
    id: 2,
    name: 'Weekend trip',
    members: ['Sarah', 'Kayla', 'Rui', 'Aly', 'Ben'],
  },
];

const mockBalances1 = {
  Sarah: 2000,
  Kayla: -1000,
  Rui: -1000,
};

const mockBalances2 = {
  Sarah: 0,
  Kayla: 0,
  Rui: 0,
  Aly: 0,
  Ben: 0,
};

describe('ALPHA-15: Scaffold React Application', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  describe('1. Loading states', () => {
    it('renders loading state initially while fetching', () => {
      vi.spyOn(api, 'fetchGroups').mockReturnValue(new Promise(() => {}));
      vi.spyOn(api, 'fetchSession').mockReturnValue(new Promise(() => {}));

      render(<App />);

      expect(screen.getByRole('status')).toBeInTheDocument();
      expect(screen.getByText(/loading application/i)).toBeInTheDocument();
    });

    it('transitions from loading state to loaded content when data resolves', async () => {
      vi.spyOn(api, 'fetchSession').mockResolvedValue({ name: 'Sarah' });
      vi.spyOn(api, 'fetchGroups').mockResolvedValue(mockGroups);
      vi.spyOn(api, 'fetchGroupBalances').mockResolvedValue(mockBalances1);

      render(<App />);

      // Initially shows loading
      expect(screen.getByRole('status')).toBeInTheDocument();

      // Once resolved, loading disappears and main app appears
      await waitFor(() => {
        expect(screen.queryByRole('status')).not.toBeInTheDocument();
        expect(screen.getByRole('heading', { level: 1, name: 'Apartment 4B' })).toBeInTheDocument();
      });
    });

    it('displays error state and recovers on retry', async () => {
      const fetchGroupsSpy = vi
        .spyOn(api, 'fetchGroups')
        .mockRejectedValueOnce(new Error('Network connection failed'))
        .mockResolvedValueOnce(mockGroups);

      vi.spyOn(api, 'fetchSession').mockResolvedValue({ name: 'Sarah' });
      vi.spyOn(api, 'fetchGroupBalances').mockResolvedValue(mockBalances1);

      render(<App />);

      await waitFor(() => {
        expect(screen.getByRole('alert')).toBeInTheDocument();
      });
      expect(screen.getByText(/network connection failed/i)).toBeInTheDocument();

      // Click retry button
      const retryBtn = screen.getByRole('button', { name: /try again/i });
      fireEvent.click(retryBtn);

      await waitFor(() => {
        expect(screen.getByRole('heading', { level: 1, name: 'Apartment 4B' })).toBeInTheDocument();
      });
      expect(fetchGroupsSpy).toHaveBeenCalledTimes(2);
    });
  });

  describe('2. Basic rendering', () => {
    it('renders header, 3-column layout, action buttons, summary cards, and group balances', async () => {
      vi.spyOn(api, 'fetchSession').mockResolvedValue({ name: 'Sarah' });
      vi.spyOn(api, 'fetchGroups').mockResolvedValue(mockGroups);
      vi.spyOn(api, 'fetchGroupBalances').mockResolvedValue(mockBalances1);

      render(<App />);

      // Top brand and logged in user
      await waitFor(() => {
        expect(screen.getByText('splitwise')).toBeInTheDocument();
      });
      expect(screen.getByLabelText('Current user')).toHaveTextContent('Sarah');

      // Center pane heading and action buttons
      expect(screen.getByRole('heading', { level: 1, name: 'Apartment 4B' })).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /add an expense/i })).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /settle up/i })).toBeInTheDocument();

      // Summary strip cards (total balance, you are owed, you owe)
      await waitFor(() => {
        expect(screen.getByText('+$20.00')).toBeInTheDocument();
      });
      expect(screen.getByText('total balance')).toBeInTheDocument();
      expect(screen.getByText('you are owed')).toBeInTheDocument();
      expect(screen.getByText('you owe')).toBeInTheDocument();

      // Right sidebar
      expect(screen.getByRole('heading', { level: 3, name: 'Group balances' })).toBeInTheDocument();
      expect(screen.getByText('Kayla')).toBeInTheDocument();
      expect(screen.getByText('Rui')).toBeInTheDocument();

      // Click Add an expense button opens modal
      const addExpenseBtn = screen.getByRole('button', { name: /add an expense/i });
      fireEvent.click(addExpenseBtn);

      expect(screen.getByRole('dialog', { name: /add an expense/i })).toBeInTheDocument();
      expect(screen.getByRole('tab', { name: /ai assistant/i })).toBeInTheDocument();

      // Close modal
      const closeBtn = screen.getByRole('button', { name: /close modal/i });
      fireEvent.click(closeBtn);
      expect(screen.queryByRole('dialog', { name: /add an expense/i })).not.toBeInTheDocument();
    });
  });

  describe('3. Navigation', () => {
    it('renders sidebar navigation landmarks, links, and friend list', async () => {
      vi.spyOn(api, 'fetchSession').mockResolvedValue({ name: 'Sarah' });
      vi.spyOn(api, 'fetchGroups').mockResolvedValue(mockGroups);
      vi.spyOn(api, 'fetchGroupBalances').mockResolvedValue(mockBalances1);

      render(<App />);

      await waitFor(() => {
        expect(screen.getByRole('heading', { level: 1, name: 'Apartment 4B' })).toBeInTheDocument();
      });

      // Navigation links
      expect(screen.getByRole('button', { name: /dashboard/i })).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /recent activity/i })).toBeInTheDocument();

      // Groups navigation landmark
      const groupsNav = screen.getByRole('navigation', { name: /groups/i });
      expect(groupsNav).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /apartment 4b/i })).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /weekend trip/i })).toBeInTheDocument();

      // Friends in sidebar (excluding the signed-in user)
      expect(screen.getByRole('button', { name: /kayla/i })).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /rui/i })).toBeInTheDocument();
    });
  });

  describe('4. Group selection', () => {
    it('updates active group view, active styling, and fetches balances when selecting another group', async () => {
      vi.spyOn(api, 'fetchSession').mockResolvedValue({ name: 'Sarah' });
      vi.spyOn(api, 'fetchGroups').mockResolvedValue(mockGroups);
      const balanceSpy = vi.spyOn(api, 'fetchGroupBalances').mockImplementation((id) =>
        Promise.resolve(id === 1 ? mockBalances1 : mockBalances2)
      );

      render(<App />);

      // Wait for default selection (Apartment 4B)
      await waitFor(() => {
        expect(screen.getByRole('heading', { level: 1, name: 'Apartment 4B' })).toBeInTheDocument();
      });
      const aptBtn = screen.getByRole('button', { name: /apartment 4b/i });
      expect(aptBtn).toHaveClass('active');
      expect(aptBtn).toHaveAttribute('aria-current', 'page');

      // Click second group
      const weekendTripBtn = screen.getByRole('button', { name: /weekend trip/i });
      expect(weekendTripBtn).not.toHaveClass('active');
      fireEvent.click(weekendTripBtn);

      // Verify active view updates
      await waitFor(() => {
        expect(screen.getByRole('heading', { level: 1, name: 'Weekend trip' })).toBeInTheDocument();
      });
      expect(weekendTripBtn).toHaveClass('active');
      expect(weekendTripBtn).toHaveAttribute('aria-current', 'page');
      expect(aptBtn).not.toHaveClass('active');

      // Verify balances were requested for group 2
      expect(balanceSpy).toHaveBeenCalledWith(2);
    });
  });

  describe('ALPHA-16: Name-Picker and Authentication', () => {
    const mockNames = ['Sarah', 'Kayla', 'Rui', 'Aly', 'Ben'];

    it('displays name-picker screen when unauthenticated and signs in successfully', async () => {
      vi.spyOn(api, 'fetchSession').mockRejectedValue(new Error('Not signed in'));
      vi.spyOn(api, 'fetchAvailableNames').mockResolvedValue(mockNames);
      const loginSpy = vi.spyOn(api, 'login').mockResolvedValue({ name: 'Kayla' });
      vi.spyOn(api, 'fetchGroups').mockResolvedValue(mockGroups);
      vi.spyOn(api, 'fetchGroupBalances').mockResolvedValue(mockBalances1);

      render(<App />);

      // Wait for name-picker to load
      await waitFor(() => {
        expect(screen.getByRole('radio', { name: /kayla/i })).toBeInTheDocument();
      });

      // Select Kayla
      const kaylaOption = screen.getByRole('radio', { name: /kayla/i });
      fireEvent.click(kaylaOption);

      // Submit login
      const signInBtn = screen.getByRole('button', { name: /continue as kayla/i });
      fireEvent.click(signInBtn);

      expect(loginSpy).toHaveBeenCalledWith('Kayla');

      // Transitions to main app
      await waitFor(() => {
        expect(screen.getByLabelText('Current user')).toHaveTextContent('Kayla');
        expect(screen.getByRole('heading', { level: 1, name: 'Apartment 4B' })).toBeInTheDocument();
      });
    });

    it('supports sign-out, returning to name-picker screen', async () => {
      vi.spyOn(api, 'fetchSession').mockResolvedValue({ name: 'Sarah' });
      vi.spyOn(api, 'fetchGroups').mockResolvedValue(mockGroups);
      vi.spyOn(api, 'fetchGroupBalances').mockResolvedValue(mockBalances1);
      vi.spyOn(api, 'fetchAvailableNames').mockResolvedValue(mockNames);
      const logoutSpy = vi.spyOn(api, 'logout').mockResolvedValue({ ok: true });

      render(<App />);

      await waitFor(() => {
        expect(screen.getByLabelText('Current user')).toHaveTextContent('Sarah');
      });

      const signOutBtn = screen.getByRole('button', { name: /sign out/i });
      fireEvent.click(signOutBtn);

      expect(logoutSpy).toHaveBeenCalled();

      // Returns to name-picker screen
      await waitFor(() => {
        expect(screen.getByRole('region', { name: /sign in to splitwise/i })).toBeInTheDocument();
      });
    });

    it('supports switching users via modal dialog', async () => {
      vi.spyOn(api, 'fetchSession').mockResolvedValue({ name: 'Sarah' });
      vi.spyOn(api, 'fetchGroups').mockResolvedValue(mockGroups);
      vi.spyOn(api, 'fetchGroupBalances').mockResolvedValue(mockBalances1);
      vi.spyOn(api, 'fetchAvailableNames').mockResolvedValue(mockNames);
      const loginSpy = vi.spyOn(api, 'login').mockResolvedValue({ name: 'Ben' });

      render(<App />);

      await waitFor(() => {
        expect(screen.getByLabelText('Current user')).toHaveTextContent('Sarah');
      });

      // Click switch user
      const switchUserBtn = screen.getByRole('button', { name: /switch user/i });
      fireEvent.click(switchUserBtn);

      // Modal appears
      await waitFor(() => {
        expect(screen.getByRole('dialog', { name: /switch user/i })).toBeInTheDocument();
      });

      // Select Ben
      const benOption = screen.getByRole('radio', { name: /ben/i });
      fireEvent.click(benOption);

      const submitSwitchBtn = screen.getByRole('button', { name: /switch to ben/i });
      fireEvent.click(submitSwitchBtn);

      expect(loginSpy).toHaveBeenCalledWith('Ben');

      // User switched
      await waitFor(() => {
        expect(screen.getByLabelText('Current user')).toHaveTextContent('Ben');
      });
    });

    it('handles unsuccessful login attempts in name-picker', async () => {
      vi.spyOn(api, 'fetchSession').mockRejectedValue(new Error('Not signed in'));
      vi.spyOn(api, 'fetchAvailableNames').mockResolvedValue(mockNames);
      vi.spyOn(api, 'login').mockRejectedValue(new Error('Unknown name'));

      render(<App />);

      await waitFor(() => {
        expect(screen.getByRole('button', { name: /continue as sarah/i })).toBeInTheDocument();
      });

      const submitBtn = screen.getByRole('button', { name: /continue as sarah/i });
      fireEvent.click(submitBtn);

      await waitFor(() => {
        expect(screen.getByRole('alert')).toBeInTheDocument();
      });
      expect(screen.getByText('Unknown name')).toBeInTheDocument();
    });

    it('restores session automatically when session cookie exists', async () => {
      vi.spyOn(api, 'fetchSession').mockResolvedValue({ name: 'Sarah' });
      vi.spyOn(api, 'fetchGroups').mockResolvedValue(mockGroups);
      vi.spyOn(api, 'fetchGroupBalances').mockResolvedValue(mockBalances1);

      render(<App />);

      await waitFor(() => {
        expect(screen.queryByRole('region', { name: /sign in to splitwise/i })).not.toBeInTheDocument();
        expect(screen.getByLabelText('Current user')).toHaveTextContent('Sarah');
      });
    });
  });

  describe('ALPHA-19: Deliver US-01 Equal Splitting End-to-End', () => {
    it('executes US-01 equal split flow: natural language prompt -> validated preview -> confirmation -> updated balances', async () => {
      vi.spyOn(api, 'fetchSession').mockResolvedValue({ name: 'Sarah' });
      vi.spyOn(api, 'fetchGroups').mockResolvedValue(mockGroups);
      const balanceSpy = vi
        .spyOn(api, 'fetchGroupBalances')
        .mockResolvedValueOnce({ Sarah: 0, Kayla: 0, Rui: 0 })
        .mockResolvedValueOnce({ Sarah: 2000, Kayla: -1000, Rui: -1000 });

      const chatSpy = vi.spyOn(api, 'sendChatMessage').mockResolvedValue({
        type: 'preview',
        conversationId: 201,
        promptCount: 1,
        status: 'preview',
        preview: {
          payer: 'Sarah',
          currency: 'USD',
          totalCents: 3000,
          description: 'Dinner',
          validated: true,
          lineItems: [
            {
              description: 'Dinner',
              amountCents: 3000,
              participants: ['Sarah', 'Kayla', 'Rui'],
            },
          ],
          charges: [],
          shares: [
            { name: 'Sarah', cents: 1000, summary: 'Dinner' },
            { name: 'Kayla', cents: 1000, summary: 'Dinner' },
            { name: 'Rui', cents: 1000, summary: 'Dinner' },
          ],
        },
      });

      const confirmSpy = vi.spyOn(api, 'confirmExpense').mockResolvedValue({
        ok: true,
        expenseId: 77,
        conversationId: 201,
        status: 'confirmed',
      });

      render(<App />);

      // Wait for app load
      await waitFor(() => {
        expect(screen.getByRole('heading', { level: 1, name: 'Apartment 4B' })).toBeInTheDocument();
      });

      // Step 1: Open Add an expense modal
      const addBtn = screen.getByRole('button', { name: /add an expense/i });
      fireEvent.click(addBtn);

      expect(screen.getByRole('dialog', { name: /add an expense/i })).toBeInTheDocument();

      // Step 2: Submit US-01 expense description
      const input = screen.getByPlaceholderText(/e\.g\. kayla and i shared nachos/i);
      const sendBtn = screen.getByRole('button', { name: /send/i });

      fireEvent.change(input, {
        target: {
          value: 'I paid $30 for dinner for Sarah, Kayla, and Rui. Split it equally.',
        },
      });
      fireEvent.click(sendBtn);

      expect(chatSpy).toHaveBeenCalledWith({
        groupId: 1,
        conversationId: null,
        message: 'I paid $30 for dinner for Sarah, Kayla, and Rui. Split it equally.',
      });

      // Step 3: Verify preview is displayed with correct shares
      await waitFor(() => {
        expect(screen.getByTestId('itemized-preview')).toBeInTheDocument();
      });

      expect(screen.getByRole('heading', { level: 4, name: 'Dinner' })).toBeInTheDocument();
      expect(screen.getByText(/paid by/i)).toHaveTextContent('Sarah');
      expect(screen.getAllByText('$30.00').length).toBeGreaterThanOrEqual(1);
      expect(screen.getAllByText('$10.00').length).toBe(3); // Sarah, Kayla, Rui shares
      expect(screen.getByLabelText(/prompt count: 1 of 5/i)).toBeInTheDocument();

      // Step 4: Confirm expense
      const confirmBtn = screen.getByRole('button', { name: /confirm expense/i });
      fireEvent.click(confirmBtn);

      expect(confirmSpy).toHaveBeenCalledWith(201);

      await waitFor(() => {
        expect(screen.getByText(/expense confirmed and saved/i)).toBeInTheDocument();
      });

      // Modal closes and balances refresh
      await waitFor(() => {
        expect(screen.queryByRole('dialog', { name: /add an expense/i })).not.toBeInTheDocument();
      });

      expect(balanceSpy).toHaveBeenCalledWith(1);
    });
  });

  describe('ALPHA-20: Deliver US-02 Selected-Member Splitting End-to-End', () => {
    it('executes US-02 selected member split: excludes nonparticipants with $0.00 and charges selected members equally', async () => {
      vi.spyOn(api, 'fetchSession').mockResolvedValue({ name: 'Sarah' });
      vi.spyOn(api, 'fetchGroups').mockResolvedValue(mockGroups);
      const balanceSpy = vi
        .spyOn(api, 'fetchGroupBalances')
        .mockResolvedValueOnce({ Sarah: 0, Kayla: 0, Rui: 0 })
        .mockResolvedValueOnce({ Sarah: 2400, Kayla: -1200, Rui: -1200 });

      const chatSpy = vi.spyOn(api, 'sendChatMessage').mockResolvedValue({
        type: 'preview',
        conversationId: 202,
        promptCount: 1,
        status: 'preview',
        preview: {
          payer: 'Sarah',
          currency: 'USD',
          totalCents: 2400,
          description: 'Groceries',
          validated: true,
          lineItems: [
            {
              description: 'Groceries',
              amountCents: 2400,
              participants: ['Kayla', 'Rui'],
            },
          ],
          charges: [],
          shares: [
            { name: 'Sarah', cents: 0, summary: 'Groceries' },
            { name: 'Kayla', cents: 1200, summary: 'Groceries' },
            { name: 'Rui', cents: 1200, summary: 'Groceries' },
          ],
        },
      });

      const confirmSpy = vi.spyOn(api, 'confirmExpense').mockResolvedValue({
        ok: true,
        expenseId: 78,
        conversationId: 202,
        status: 'confirmed',
      });

      render(<App />);

      await waitFor(() => {
        expect(screen.getByRole('heading', { level: 1, name: 'Apartment 4B' })).toBeInTheDocument();
      });

      // Step 1: Open Add an expense modal
      fireEvent.click(screen.getByRole('button', { name: /add an expense/i }));

      // Step 2: Submit US-02 expense description
      const input = screen.getByPlaceholderText(/e\.g\. kayla and i shared nachos/i);
      const sendBtn = screen.getByRole('button', { name: /send/i });

      fireEvent.change(input, {
        target: {
          value: 'I paid $24 for groceries, but only Kayla and Rui are sharing them.',
        },
      });
      fireEvent.click(sendBtn);

      expect(chatSpy).toHaveBeenCalledWith({
        groupId: 1,
        conversationId: null,
        message: 'I paid $24 for groceries, but only Kayla and Rui are sharing them.',
      });

      // Step 3: Verify preview displays $0.00 for excluded Sarah and $12.00 for Kayla and Rui
      await waitFor(() => {
        expect(screen.getByTestId('itemized-preview')).toBeInTheDocument();
      });

      expect(screen.getByRole('heading', { level: 4, name: 'Groceries' })).toBeInTheDocument();
      expect(screen.getByText(/paid by/i)).toHaveTextContent('Sarah');
      expect(screen.getAllByText('$24.00').length).toBeGreaterThanOrEqual(1);

      // Nonparticipant receives zero
      expect(screen.getAllByText('$0.00').length).toBeGreaterThanOrEqual(1);
      // Only specified participants charged ($12.00 each)
      expect(screen.getAllByText('$12.00').length).toBe(2);

      // Step 4: Confirm expense
      const confirmBtn = screen.getByRole('button', { name: /confirm expense/i });
      fireEvent.click(confirmBtn);

      expect(confirmSpy).toHaveBeenCalledWith(202);

      await waitFor(() => {
        expect(screen.getByText(/expense confirmed and saved/i)).toBeInTheDocument();
      });

      await waitFor(() => {
        expect(screen.queryByRole('dialog', { name: /add an expense/i })).not.toBeInTheDocument();
      });

      expect(balanceSpy).toHaveBeenCalledWith(1);
    });
  });

  describe('ALPHA-22: Deliver US-03 Itemized Multi-Way Splitting End-to-End', () => {
    it('executes US-03 itemized multi-way split: calculates each person share from individual items and shared items', async () => {
      vi.spyOn(api, 'fetchSession').mockResolvedValue({ name: 'Sarah' });
      vi.spyOn(api, 'fetchGroups').mockResolvedValue(mockGroups);
      const balanceSpy = vi.spyOn(api, 'fetchGroupBalances').mockResolvedValue(mockBalances1);

      const chatSpy = vi.spyOn(api, 'sendChatMessage').mockResolvedValue({
        type: 'preview',
        status: 'preview',
        promptCount: 1,
        conversationId: 303,
        preview: {
          payer: 'Sarah',
          currency: 'USD',
          totalCents: 4200,
          description: 'Dinner',
          validated: true,
          lineItems: [
            {
              description: 'Nachos',
              amountCents: 1200,
              participants: ['Sarah', 'Kayla'],
            },
            {
              description: 'Burger',
              amountCents: 1500,
              participants: ['Rui'],
            },
            {
              description: 'Pasta',
              amountCents: 1500,
              participants: ['Kayla'],
            },
          ],
          charges: [],
          shares: [
            { name: 'Sarah', cents: 600, summary: 'Dinner' },
            { name: 'Kayla', cents: 2100, summary: 'Dinner' },
            { name: 'Rui', cents: 1500, summary: 'Dinner' },
          ],
        },
      });

      const confirmSpy = vi.spyOn(api, 'confirmExpense').mockResolvedValue({
        ok: true,
        expenseId: 99,
        conversationId: 303,
        status: 'confirmed',
      });

      render(<App />);

      await waitFor(() => {
        expect(screen.getByRole('heading', { level: 1, name: 'Apartment 4B' })).toBeInTheDocument();
      });

      // Step 1: Open Add an expense modal
      fireEvent.click(screen.getByRole('button', { name: /add an expense/i }));

      // Step 2: Submit US-03 natural language prompt
      const input = screen.getByPlaceholderText(/e\.g\. kayla and i shared nachos/i);
      const sendBtn = screen.getByRole('button', { name: /send/i });

      fireEvent.change(input, {
        target: {
          value: 'I paid $42. Kayla and I shared $12 nachos. Rui had a $15 burger, and Kayla had a $15 pasta.',
        },
      });
      fireEvent.click(sendBtn);

      expect(chatSpy).toHaveBeenCalledWith({
        groupId: 1,
        conversationId: null,
        message: 'I paid $42. Kayla and I shared $12 nachos. Rui had a $15 burger, and Kayla had a $15 pasta.',
      });

      // Step 3: Verify preview renders line items and multi-way shares
      await waitFor(() => {
        expect(screen.getByTestId('itemized-preview')).toBeInTheDocument();
      });

      // Heading and total
      expect(screen.getByRole('heading', { level: 4, name: 'Dinner' })).toBeInTheDocument();
      expect(screen.getByText(/paid by/i)).toHaveTextContent('Sarah');
      expect(screen.getAllByText('$42.00').length).toBeGreaterThanOrEqual(1);

      // Multiple items identified
      expect(screen.getByText('Nachos')).toBeInTheDocument();
      expect(screen.getByText('$12.00')).toBeInTheDocument();
      expect(screen.getByText('Burger')).toBeInTheDocument();
      expect(screen.getByText('Pasta')).toBeInTheDocument();
      // $15.00 appears for Burger, Pasta, and Rui's share
      expect(screen.getAllByText('$15.00').length).toBe(3);

      // Itemized shares
      expect(screen.getByText('$6.00')).toBeInTheDocument();   // Sarah: half of nachos
      expect(screen.getByText('$21.00')).toBeInTheDocument();  // Kayla: half of nachos ($6) + pasta ($15)

      // Step 4: Confirm expense
      const confirmBtn = screen.getByRole('button', { name: /confirm expense/i });
      fireEvent.click(confirmBtn);

      expect(confirmSpy).toHaveBeenCalledWith(303);

      await waitFor(() => {
        expect(screen.getByText(/expense confirmed and saved/i)).toBeInTheDocument();
      });

      await waitFor(() => {
        expect(screen.queryByRole('dialog', { name: /add an expense/i })).not.toBeInTheDocument();
      });

      expect(balanceSpy).toHaveBeenCalledWith(1);
    });
  });

  describe('ALPHA-23: Deliver US-04 Quantities and Tax/Tip End-to-End', () => {
    it('executes US-04 quantities and tax/tip split: calculates quantities and distributes proportional tip', async () => {
      vi.spyOn(api, 'fetchSession').mockResolvedValue({ name: 'Sarah' });
      vi.spyOn(api, 'fetchGroups').mockResolvedValue(mockGroups);
      const balanceSpy = vi.spyOn(api, 'fetchGroupBalances').mockResolvedValue(mockBalances1);

      const chatSpy = vi.spyOn(api, 'sendChatMessage').mockResolvedValue({
        type: 'preview',
        status: 'preview',
        promptCount: 1,
        conversationId: 404,
        preview: {
          payer: 'Sarah',
          currency: 'USD',
          totalCents: 3600,
          description: 'Dinner',
          validated: true,
          lineItems: [
            {
              description: 'Drinks (2)',
              amountCents: 2000,
              participants: ['Kayla'],
            },
            {
              description: 'Drink (1)',
              amountCents: 1000,
              participants: ['Rui'],
            },
          ],
          charges: [
            {
              kind: 'tip',
              amountCents: 600,
              method: 'proportional',
            },
          ],
          shares: [
            { name: 'Sarah', cents: 0, summary: 'Dinner' },
            { name: 'Kayla', cents: 2400, summary: 'Dinner' },
            { name: 'Rui', cents: 1200, summary: 'Dinner' },
          ],
        },
      });

      const confirmSpy = vi.spyOn(api, 'confirmExpense').mockResolvedValue({
        ok: true,
        expenseId: 111,
        conversationId: 404,
        status: 'confirmed',
      });

      render(<App />);

      await waitFor(() => {
        expect(screen.getByRole('heading', { level: 1, name: 'Apartment 4B' })).toBeInTheDocument();
      });

      // Step 1: Open Add an expense modal
      fireEvent.click(screen.getByRole('button', { name: /add an expense/i }));

      // Step 2: Submit US-04 prompt
      const input = screen.getByPlaceholderText(/e\.g\. kayla and i shared nachos/i);
      const sendBtn = screen.getByRole('button', { name: /send/i });

      fireEvent.change(input, {
        target: {
          value:
            "I paid for dinner. Kayla got two $10 drinks, Rui got one $10 drink, and I didn't have anything. The tip was $6. Split the tip proportionally.",
        },
      });
      fireEvent.click(sendBtn);

      expect(chatSpy).toHaveBeenCalledWith({
        groupId: 1,
        conversationId: null,
        message:
          "I paid for dinner. Kayla got two $10 drinks, Rui got one $10 drink, and I didn't have anything. The tip was $6. Split the tip proportionally.",
      });

      // Step 3: Verify preview elements
      await waitFor(() => {
        expect(screen.getByTestId('itemized-preview')).toBeInTheDocument();
      });

      expect(screen.getByRole('heading', { level: 4, name: 'Dinner' })).toBeInTheDocument();
      expect(screen.getByText(/paid by/i)).toHaveTextContent('Sarah');

      // Quantities and line items
      expect(screen.getByText('Drinks (2)')).toBeInTheDocument();
      expect(screen.getAllByText('$20.00').length).toBeGreaterThanOrEqual(1);
      expect(screen.getByText('Drink (1)')).toBeInTheDocument();
      expect(screen.getByText('$10.00')).toBeInTheDocument();

      // Additional charges (Tip)
      expect(screen.getByText('Tip')).toBeInTheDocument();
      expect(screen.getByText('$6.00')).toBeInTheDocument();

      // Total
      expect(screen.getAllByText('$36.00').length).toBeGreaterThanOrEqual(1);

      // Participant shares: Sarah receives $0.00, Kayla gets $24.00, Rui gets $12.00
      expect(screen.getAllByText('$0.00').length).toBeGreaterThanOrEqual(1);
      expect(screen.getByText('$24.00')).toBeInTheDocument();
      expect(screen.getByText('$12.00')).toBeInTheDocument();

      // Step 4: Confirm expense
      const confirmBtn = screen.getByRole('button', { name: /confirm expense/i });
      fireEvent.click(confirmBtn);

      expect(confirmSpy).toHaveBeenCalledWith(404);

      await waitFor(() => {
        expect(screen.getByText(/expense confirmed and saved/i)).toBeInTheDocument();
      });

      await waitFor(() => {
        expect(screen.queryByRole('dialog', { name: /add an expense/i })).not.toBeInTheDocument();
      });

      expect(balanceSpy).toHaveBeenCalledWith(1);
    });
  });

  describe('ALPHA-24: Deliver US-05 Missing Information Handling End-to-End', () => {
    it('executes US-05 multi-turn flow: asks follow-up question for missing prices and produces preview upon clarification', async () => {
      vi.spyOn(api, 'fetchSession').mockResolvedValue({ name: 'Sarah' });
      vi.spyOn(api, 'fetchGroups').mockResolvedValue(mockGroups);
      const balanceSpy = vi.spyOn(api, 'fetchGroupBalances').mockResolvedValue(mockBalances1);

      const chatSpy = vi
        .spyOn(api, 'sendChatMessage')
        .mockResolvedValueOnce({
          type: 'question',
          status: 'pending',
          promptCount: 1,
          conversationId: 505,
          question: 'How much were the nachos and each drink?',
        })
        .mockResolvedValueOnce({
          type: 'preview',
          status: 'preview',
          promptCount: 2,
          conversationId: 505,
          preview: {
            payer: 'Sarah',
            currency: 'USD',
            totalCents: 2600,
            description: 'Dinner',
            validated: true,
            lineItems: [
              {
                description: 'Nachos',
                amountCents: 1600,
                participants: ['Sarah', 'Kayla'],
              },
              {
                description: 'Drinks (2)',
                amountCents: 1000,
                participants: ['Rui'],
              },
            ],
            charges: [],
            shares: [
              { name: 'Sarah', cents: 800, summary: 'Dinner' },
              { name: 'Kayla', cents: 800, summary: 'Dinner' },
              { name: 'Rui', cents: 1000, summary: 'Dinner' },
            ],
          },
        });

      const confirmSpy = vi.spyOn(api, 'confirmExpense').mockResolvedValue({
        ok: true,
        expenseId: 125,
        conversationId: 505,
        status: 'confirmed',
      });

      render(<App />);

      await waitFor(() => {
        expect(screen.getByRole('heading', { level: 1, name: 'Apartment 4B' })).toBeInTheDocument();
      });

      // Step 1: Open Add an expense modal
      fireEvent.click(screen.getByRole('button', { name: /add an expense/i }));

      // Step 2: Submit Turn 1 prompt with missing prices
      const input = screen.getByPlaceholderText(/e\.g\. kayla and i shared nachos/i);
      const sendBtn = screen.getByRole('button', { name: /send/i });

      fireEvent.change(input, {
        target: {
          value: 'Me and Kayla shared nachoes, Rui got two drinks, and I paid.',
        },
      });
      fireEvent.click(sendBtn);

      expect(chatSpy).toHaveBeenNthCalledWith(1, {
        groupId: 1,
        conversationId: null,
        message: 'Me and Kayla shared nachoes, Rui got two drinks, and I paid.',
      });

      // Step 3: Verify follow-up question is displayed and prompt counter increments
      await waitFor(() => {
        expect(
          screen.getByText('How much were the nachos and each drink?')
        ).toBeInTheDocument();
      });
      expect(screen.getByLabelText(/prompt count: 1 of 5/i)).toBeInTheDocument();
      expect(screen.queryByTestId('itemized-preview')).not.toBeInTheDocument();

      // Step 4: Submit Turn 2 clarification with prices
      fireEvent.change(input, {
        target: {
          value: 'Nachos were $16 and drinks were $5 each. No tax or tip.',
        },
      });
      fireEvent.click(sendBtn);

      expect(chatSpy).toHaveBeenNthCalledWith(2, {
        groupId: 1,
        conversationId: 505,
        message: 'Nachos were $16 and drinks were $5 each. No tax or tip.',
      });

      // Step 5: Verify validated preview is displayed with prompt count 2 / 5
      await waitFor(() => {
        expect(screen.getByTestId('itemized-preview')).toBeInTheDocument();
      });
      expect(screen.getByLabelText(/prompt count: 2 of 5/i)).toBeInTheDocument();

      // Verify line items and prices
      expect(screen.getByText('Nachos')).toBeInTheDocument();
      expect(screen.getByText('$16.00')).toBeInTheDocument();
      expect(screen.getByText('Drinks (2)')).toBeInTheDocument();
      expect(screen.getAllByText('$10.00').length).toBeGreaterThanOrEqual(1);

      // Verify total
      expect(screen.getAllByText('$26.00').length).toBeGreaterThanOrEqual(1);

      // Verify participant shares ($8.00 for Sarah, $8.00 for Kayla, $10.00 for Rui)
      expect(screen.getAllByText('$8.00').length).toBe(2);

      // Step 6: Confirm expense
      const confirmBtn = screen.getByRole('button', { name: /confirm expense/i });
      fireEvent.click(confirmBtn);

      expect(confirmSpy).toHaveBeenCalledWith(505);

      await waitFor(() => {
        expect(screen.getByText(/expense confirmed and saved/i)).toBeInTheDocument();
      });

      await waitFor(() => {
        expect(screen.queryByRole('dialog', { name: /add an expense/i })).not.toBeInTheDocument();
      });

      expect(balanceSpy).toHaveBeenCalledWith(1);
    });
  });
});
