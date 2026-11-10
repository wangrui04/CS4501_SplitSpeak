import { describe, it, expect, vi, beforeEach } from 'vitest';
import {
  fetchNotifications,
  fetchSettlements,
  markNotificationRead,
  recordSettlement,
  sendReminder,
} from './api';

// #46: request shapes match docs/api.md (Settle up).

function mockFetch(body = {}, status = 200) {
  const fetchSpy = vi.fn().mockResolvedValue({
    ok: status < 400,
    status,
    json: () => Promise.resolve(body),
  });
  vi.stubGlobal('fetch', fetchSpy);
  return fetchSpy;
}

describe('#46: settle-up API calls', () => {
  beforeEach(() => {
    vi.unstubAllGlobals();
  });

  it('records a settlement with integer cents and the shown balance', async () => {
    const fetchSpy = mockFetch({ id: 1 });

    await recordSettlement(1, {
      from: 'Kayla',
      to: 'Sarah',
      cents: 1000,
      expectedOutstandingCents: 3000,
    });

    const [url, options] = fetchSpy.mock.calls[0];
    expect(url).toBe('/api/groups/1/settlements');
    expect(options.method).toBe('POST');
    expect(JSON.parse(options.body)).toEqual({
      from: 'Kayla',
      to: 'Sarah',
      cents: 1000,
      expectedOutstandingCents: 3000,
    });
  });

  it('fetches settlements for a group', async () => {
    const fetchSpy = mockFetch([]);

    await fetchSettlements(2);

    expect(fetchSpy.mock.calls[0][0]).toBe('/api/groups/2/settlements');
  });

  it('sends a reminder to one member', async () => {
    const fetchSpy = mockFetch({ id: 3 });

    await sendReminder(1, 'Kayla');

    const [url, options] = fetchSpy.mock.calls[0];
    expect(url).toBe('/api/groups/1/reminders');
    expect(options.method).toBe('POST');
    expect(JSON.parse(options.body)).toEqual({ to: 'Kayla' });
  });

  it('fetches and marks notifications', async () => {
    const fetchSpy = mockFetch([]);

    await fetchNotifications();
    await markNotificationRead(5);

    expect(fetchSpy.mock.calls[0][0]).toBe('/api/notifications');
    expect(fetchSpy.mock.calls[1][0]).toBe('/api/notifications/5/read');
    expect(fetchSpy.mock.calls[1][1].method).toBe('POST');
  });

  it('passes the server message and status through on errors', async () => {
    mockFetch({ detail: 'Balance changed, please refresh' }, 409);

    await expect(
      recordSettlement(1, { from: 'Kayla', to: 'Sarah', cents: 1, expectedOutstandingCents: 9 })
    ).rejects.toMatchObject({ message: 'Balance changed, please refresh', status: 409 });
  });
});
