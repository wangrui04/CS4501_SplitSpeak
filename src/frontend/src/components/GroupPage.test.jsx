import { render, screen, within } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import GroupView from './GroupView';
import RightSidebar from './RightSidebar';

const group = { id: 1, name: 'Apartment 4B', members: ['Sarah', 'Kayla', 'Rui'] };

function expense(overrides) {
  return {
    id: 1,
    description: 'Dinner',
    payer: 'Sarah',
    totalCents: 3000,
    created_at: '2026-10-14 19:30:00',
    payments: [{ name: 'Sarah', cents: 3000 }],
    shares: [
      { name: 'Sarah', cents: 1000 },
      { name: 'Kayla', cents: 1000 },
      { name: 'Rui', cents: 1000 },
    ],
    ...overrides,
  };
}

describe('ALPHA-29: Group summary bar', () => {
  it('shows total balance, you owe, and you are owed with colors', () => {
    render(
      <GroupView
        group={group}
        currentUser="Kayla"
        summary={{ totalBalance: -11500, youOwe: 11500, youAreOwed: 0 }}
        expenses={[]}
      />
    );

    expect(screen.getByText('-$115.00')).toHaveClass('orangeText');
    expect(screen.getByText('you owe').querySelector('b')).toHaveClass('orangeText');
    expect(screen.getByText('you owe').querySelector('b')).toHaveTextContent('$115.00');
    expect(screen.getByText('you are owed').querySelector('b')).toHaveTextContent('$0.00');
  });

  it('colors you are owed green', () => {
    render(
      <GroupView
        group={group}
        currentUser="Sarah"
        summary={{ totalBalance: 39500, youOwe: 0, youAreOwed: 39500 }}
        expenses={[]}
      />
    );

    expect(screen.getByText('+$395.00')).toHaveClass('green');
    expect(screen.getByText('you are owed').querySelector('b')).toHaveClass('green');
  });
});

describe('ALPHA-29: Expense list', () => {
  it('shows the empty state', () => {
    render(<GroupView group={group} currentUser="Sarah" expenses={[]} />);

    expect(screen.getByText('No expenses yet')).toBeInTheDocument();
    expect(screen.getByText('Add your first shared expense to see it here.')).toBeInTheDocument();
  });

  it('groups expenses under month headers', () => {
    render(
      <GroupView
        group={group}
        currentUser="Sarah"
        expenses={[
          expense({ id: 3, description: 'Taxi', created_at: '2026-11-01 10:00:00' }),
          expense({ id: 2, description: 'Groceries', created_at: '2026-10-20 10:00:00' }),
          expense({ id: 1, description: 'Dinner', created_at: '2026-10-14 10:00:00' }),
        ]}
      />
    );

    const headers = screen.getAllByRole('heading', { level: 2 }).map((h) => h.textContent);
    expect(headers).toEqual(['NOVEMBER 2026', 'OCTOBER 2026']);

    const october = screen.getByRole('list', { name: 'OCTOBER 2026' });
    expect(within(october).getAllByRole('listitem')).toHaveLength(2);
  });

  it('shows description, who paid, total, and "you lent" for the payer', () => {
    render(<GroupView group={group} currentUser="Sarah" expenses={[expense()]} />);

    const row = screen.getByRole('listitem');
    expect(row).toHaveTextContent('Dinner');
    expect(row).toHaveTextContent('Sarah paid $30.00');
    expect(row).toHaveTextContent('you lent$20.00');
  });

  it('shows "you owe" for someone who did not pay', () => {
    render(<GroupView group={group} currentUser="Kayla" expenses={[expense()]} />);

    expect(screen.getByRole('listitem')).toHaveTextContent('you owe$10.00');
  });

  it('shows "not involved" for someone with no share and no payment', () => {
    const groceries = expense({
      shares: [
        { name: 'Sarah', cents: 1500 },
        { name: 'Kayla', cents: 1500 },
        { name: 'Rui', cents: 0 },
      ],
    });
    render(<GroupView group={group} currentUser="Rui" expenses={[groceries]} />);

    expect(screen.getByRole('listitem')).toHaveTextContent('not involved');
  });

  it('uses amounts paid for multi-payer expenses', () => {
    const trip = expense({
      description: 'Trip',
      totalCents: 105000,
      payments: [
        { name: 'Sarah', cents: 84000 },
        { name: 'Kayla', cents: 9000 },
        { name: 'Rui', cents: 12000 },
      ],
      shares: [
        { name: 'Sarah', cents: 44500 },
        { name: 'Kayla', cents: 20500 },
        { name: 'Rui', cents: 40000 },
      ],
    });
    render(<GroupView group={group} currentUser="Kayla" expenses={[trip]} />);

    const row = screen.getByRole('listitem');
    expect(row).toHaveTextContent('3 people paid $1,050.00');
    expect(row).toHaveTextContent('you owe$115.00');
  });
});

describe('ALPHA-29: Group balances panel', () => {
  const balances = [
    { name: 'Kayla', cents: 1000, status: 'owes you' },
    { name: 'Rui', cents: -2500, status: 'you owe' },
    { name: 'Aly', cents: 0, status: 'settled up' },
  ];

  it('shows all three states with colors', () => {
    render(<RightSidebar balances={balances} />);

    const panel = screen.getByRole('complementary', { name: 'Group balances' });
    expect(within(panel).getByText('owes you $10.00')).toHaveClass('positive');
    expect(within(panel).getByText('you owe $25.00')).toHaveClass('negative');
    expect(within(panel).getByText('settled up $0.00')).toHaveClass('settled');
  });

  it('shows the simulated-balances note', () => {
    render(<RightSidebar balances={balances} />);

    expect(
      screen.getByText(
        'All balances here are simulated. Expenses are saved only after you confirm them.'
      )
    ).toBeInTheDocument();
  });

  it('handles a group with no other members', () => {
    render(<RightSidebar balances={[]} />);

    expect(screen.getByText(/no other members/i)).toBeInTheDocument();
  });
});
