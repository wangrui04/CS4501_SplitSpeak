import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import NamePicker from './NamePicker';
import * as api from '../api';

const mockNames = ['Sarah', 'Kayla', 'Rui', 'Aly', 'Ben'];

describe('NamePicker Component', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('fetches and displays available profiles', async () => {
    vi.spyOn(api, 'fetchAvailableNames').mockResolvedValue(mockNames);

    render(<NamePicker onSelectUser={vi.fn()} />);

    expect(screen.getByText(/loading available profiles/i)).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText('Sarah')).toBeInTheDocument();
    });

    expect(screen.getByText('Kayla')).toBeInTheDocument();
    expect(screen.getByText('Rui')).toBeInTheDocument();
    expect(screen.getByText('Aly')).toBeInTheDocument();
    expect(screen.getByText('Ben')).toBeInTheDocument();
  });

  it('allows user selection and triggers onSelectUser', async () => {
    const handleSelect = vi.fn().mockResolvedValue();
    render(<NamePicker initialNames={mockNames} onSelectUser={handleSelect} />);

    // Click 'Kayla' profile
    const kaylaOption = screen.getByRole('radio', { name: /kayla/i });
    fireEvent.click(kaylaOption);

    expect(kaylaOption).toHaveAttribute('aria-checked', 'true');

    // Submit
    const submitBtn = screen.getByRole('button', { name: /continue as kayla/i });
    fireEvent.click(submitBtn);

    await waitFor(() => {
      expect(handleSelect).toHaveBeenCalledWith('Kayla');
    });
  });

  it('displays error message when login fails', async () => {
    const handleSelect = vi.fn().mockRejectedValue(new Error('Unknown name'));
    render(<NamePicker initialNames={mockNames} onSelectUser={handleSelect} />);

    const submitBtn = screen.getByRole('button', { name: /continue as sarah/i });
    fireEvent.click(submitBtn);

    await waitFor(() => {
      expect(screen.getByRole('alert')).toBeInTheDocument();
    });
    expect(screen.getByText('Unknown name')).toBeInTheDocument();
  });

  it('renders in modal mode with cancel button and close button', () => {
    const handleCancel = vi.fn();
    render(
      <NamePicker
        isModal
        currentUserName="Sarah"
        initialNames={mockNames}
        onSelectUser={vi.fn()}
        onCancel={handleCancel}
      />
    );

    expect(screen.getByRole('dialog', { name: /switch user/i })).toBeInTheDocument();

    const cancelBtn = screen.getByRole('button', { name: /cancel/i });
    fireEvent.click(cancelBtn);
    expect(handleCancel).toHaveBeenCalledTimes(1);

    const closeBtn = screen.getByRole('button', { name: /close/i });
    fireEvent.click(closeBtn);
    expect(handleCancel).toHaveBeenCalledTimes(2);
  });

  it('handles failure when fetching available names', async () => {
    vi.spyOn(api, 'fetchAvailableNames').mockRejectedValue(new Error('Service unavailable'));

    render(<NamePicker onSelectUser={vi.fn()} />);

    await waitFor(() => {
      expect(screen.getByRole('alert')).toBeInTheDocument();
    });
    expect(screen.getByText('Service unavailable')).toBeInTheDocument();
  });
});
