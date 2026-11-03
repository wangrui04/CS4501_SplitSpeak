export default function ErrorMessage({ title = 'Error', message, onRetry }) {
  return (
    <div className="error-container" role="alert">
      <h4>{title}</h4>
      <p>{message || 'An unexpected error occurred.'}</p>
      {onRetry && (
        <button type="button" className="retry-btn" onClick={onRetry}>
          Try again
        </button>
      )}
    </div>
  );
}

