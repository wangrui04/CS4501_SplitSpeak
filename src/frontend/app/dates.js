// "2026-11-10T13:00:00+00:00" -> "Nov 10, 1:00 PM" in the viewer's time zone.
export function formatWhen(iso) {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return iso;
  return date.toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  });
}
