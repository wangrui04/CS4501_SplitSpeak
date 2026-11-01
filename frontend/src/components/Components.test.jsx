import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import Header from './Header';
import Sidebar from './Sidebar';
import GroupView from './GroupView';
import RightSidebar from './RightSidebar';
import LoadingSpinner from './LoadingSpinner';
import ErrorMessage from './ErrorMessage';

describe('Reusable Components', () => {
  it('Header renders user initial, name, and action buttons', () => {
    const handleSwitch = vi.fn();
    const handleSignOut = vi.fn();

    render(
      <Header
        currentUser="Kayla"
        onSwitchUser={handleSwitch}
        onSignOut={handleSignOut}
      />
    );
    expect(screen.getByText('splitwise')).toBeInTheDocument();
    expect(screen.getByText('Kayla')).toBeInTheDocument();
    expect(screen.getByText('K')).toBeInTheDocument();

    const switchBtn = screen.getByRole('button', { name: /switch user/i });
    expect(switchBtn).toBeInTheDocument();
    fireEvent.click(switchBtn);
    expect(handleSwitch).toHaveBeenCalledTimes(1);

    const signOutBtn = screen.getByRole('button', { name: /sign out/i });
    expect(signOutBtn).toBeInTheDocument();
    fireEvent.click(signOutBtn);
    expect(handleSignOut).toHaveBeenCalledTimes(1);
  });

  it('Sidebar renders groups and calls onSelectGroup', () => {
    const handleSelect = vi.fn();
    const groups = [
      { id: 10, name: 'Ski Trip', members: ['Sarah', 'Ben'] },
      { id: 20, name: 'Dinner Club', members: ['Sarah', 'Kayla'] },
    ];

    render(
      <Sidebar
        groups={groups}
        selectedGroupId={10}
        onSelectGroup={handleSelect}
        friends={['Ben']}
        currentUser="Sarah"
      />
    );

    const tripBtn = screen.getByRole('button', { name: /ski trip/i });
    expect(tripBtn).toHaveClass('active');

    const clubBtn = screen.getByRole('button', { name: /dinner club/i });
    fireEvent.click(clubBtn);
    expect(handleSelect).toHaveBeenCalledWith(20);

    expect(screen.getByText(/ben/i)).toBeInTheDocument();
  });

  it('GroupView renders group header, sum strip, and empty state', () => {
    const group = { id: 1, name: 'Apartment 4B', members: ['Sarah', 'Kayla', 'Rui'] };
    const balances = { Sarah: 3000, Kayla: -1500, Rui: -1500 };

    render(
      <GroupView
        group={group}
        balances={balances}
        currentUser="Sarah"
        expenses={[]}
      />
    );

    expect(screen.getByRole('heading', { level: 1, name: 'Apartment 4B' })).toBeInTheDocument();
    expect(screen.getByText('+$30.00')).toBeInTheDocument();
    expect(screen.getByText('$30.00')).toBeInTheDocument();
    expect(screen.getByText('No expenses yet')).toBeInTheDocument();
  });

  it('RightSidebar formats balances and highlights positive and negative values', () => {
    const members = ['Sarah', 'Kayla', 'Rui'];
    const balances = { Sarah: 2000, Kayla: -1000, Rui: 1000 };

    render(
      <RightSidebar
        members={members}
        balances={balances}
        currentUser="Sarah"
      />
    );

    expect(screen.getByRole('heading', { level: 3, name: 'Group balances' })).toBeInTheDocument();
    expect(screen.getByText(/owes the group/i)).toBeInTheDocument();
    expect(screen.getByText(/is owed/i)).toBeInTheDocument();
  });

  it('LoadingSpinner renders status message', () => {
    render(<LoadingSpinner message="Fetching data..." />);
    expect(screen.getByRole('status')).toBeInTheDocument();
    expect(screen.getByText('Fetching data...')).toBeInTheDocument();
  });

  it('ErrorMessage renders alert and calls onRetry when clicked', () => {
    const retry = vi.fn();
    render(<ErrorMessage title="Error occurred" message="Network error" onRetry={retry} />);

    expect(screen.getByRole('alert')).toBeInTheDocument();
    expect(screen.getByText('Error occurred')).toBeInTheDocument();
    expect(screen.getByText('Network error')).toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: /try again/i }));
    expect(retry).toHaveBeenCalled();
  });
});

