import { useState, useEffect, useRef } from 'react';
import { sendChatMessage } from '../api';
import ItemizedPreview from './ItemizedPreview';

const MAX_PROMPTS = 5;

function formatCents(cents) {
  if (cents === null || cents === undefined) return '$0.00';
  return `$${(Math.abs(cents) / 100).toFixed(2)}`;
}

export default function AddExpenseModal({
  isOpen,
  onClose,
  group,
  currentUser,
  onExpenseConfirmed,
}) {
  const [activeTab, setActiveTab] = useState('ai'); // 'ai' | 'manual'

  // AI Chat state
  const [conversationId, setConversationId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [promptCount, setPromptCount] = useState(0);
  const [preview, setPreview] = useState(null);
  const [lastUserMessage, setLastUserMessage] = useState('');

  // Manual entry state
  const [manualDesc, setManualDesc] = useState('');
  const [manualAmount, setManualAmount] = useState('');
  const [manualPayer, setManualPayer] = useState(
    currentUser && group?.members?.includes(currentUser)
      ? currentUser
      : group?.members?.[0] || ''
  );
  const [manualParticipants, setManualParticipants] = useState(group?.members || []);
  const [manualError, setManualError] = useState(null);
  const [manualSuccess, setManualSuccess] = useState(false);

  const chatBottomRef = useRef(null);
  const inputRef = useRef(null);

  // Scroll to bottom of chat when new messages appear
  useEffect(() => {
    if (
      chatBottomRef.current &&
      typeof chatBottomRef.current.scrollIntoView === 'function'
    ) {
      chatBottomRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, loading]);

  if (!isOpen) return null;

  const handleResetConversation = () => {
    setConversationId(null);
    setMessages([]);
    setInputMessage('');
    setLoading(false);
    setError(null);
    setPromptCount(0);
    setPreview(null);
    setLastUserMessage('');
  };

  const handleSendMessage = async (textToSend) => {
    const text = (textToSend || inputMessage).trim();
    if (!text || loading || promptCount >= MAX_PROMPTS) return;

    setError(null);
    setInputMessage('');
    setLastUserMessage(text);

    // Add user message to UI immediately
    const userMsg = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: text,
    };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    try {
      const response = await sendChatMessage({
        groupId: group?.id,
        conversationId,
        message: text,
      });

      if (response.conversationId) {
        setConversationId(response.conversationId);
      }
      if (typeof response.promptCount === 'number') {
        setPromptCount(response.promptCount);
      }

      if (response.type === 'question') {
        const assistantMsg = {
          id: `asst-${Date.now()}`,
          role: 'assistant',
          content: response.question,
          type: 'question',
        };
        setMessages((prev) => [...prev, assistantMsg]);
      } else if (response.type === 'preview') {
        setPreview(response.preview);
        const assistantMsg = {
          id: `asst-${Date.now()}`,
          role: 'assistant',
          content: 'Here is the itemized preview for your expense:',
          type: 'preview',
          preview: response.preview,
        };
        setMessages((prev) => [...prev, assistantMsg]);
      } else if (response.type === 'unresolved') {
        setPreview(null);
        const assistantMsg = {
          id: `asst-${Date.now()}`,
          role: 'assistant',
          content: response.reason || 'I am unable to resolve this expense. Please enter it manually.',
          type: 'unresolved',
          fallback: true,
        };
        setMessages((prev) => [...prev, assistantMsg]);
      } else {
        const assistantMsg = {
          id: `asst-${Date.now()}`,
          role: 'assistant',
          content: response.message || 'Something went wrong processing your expense.',
          type: 'error',
        };
        setMessages((prev) => [...prev, assistantMsg]);
      }
    } catch (err) {
      setError(err.message || 'Failed to send message. Please check connection and try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleRetryLastMessage = () => {
    if (lastUserMessage) {
      handleSendMessage(lastUserMessage);
    }
  };

  const toggleParticipant = (member) => {
    setManualParticipants((prev) =>
      prev.includes(member) ? prev.filter((m) => m !== member) : [...prev, member]
    );
  };

  const handleManualSave = (e) => {
    e.preventDefault();
    setManualError(null);

    const desc = manualDesc.trim();
    const amountVal = parseFloat(manualAmount);

    if (!desc) {
      setManualError('Please provide a description.');
      return;
    }
    if (isNaN(amountVal) || amountVal <= 0) {
      setManualError('Please provide a valid positive amount.');
      return;
    }
    if (manualParticipants.length === 0) {
      setManualError('Please select at least one participant.');
      return;
    }

    const cents = Math.round(amountVal * 100);
    const manualExpense = {
      description: desc,
      payer: manualPayer,
      amount_cents: cents,
      participants: manualParticipants,
    };

    setManualSuccess(true);
    if (onExpenseConfirmed) {
      onExpenseConfirmed(manualExpense);
    }
    setTimeout(() => {
      onClose();
    }, 400);
  };

  return (
    <div
      className="modalback open"
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
      role="presentation"
    >
      <div
        className="modal"
        role="dialog"
        aria-label="Add an expense"
        aria-modal="true"
      >
        <div className="modalhead">
          <span>Add an expense</span>
          <button
            type="button"
            className="close"
            id="closeModal"
            onClick={onClose}
            aria-label="Close modal"
          >
            ×
          </button>
        </div>

        {/* Tab Switcher */}
        <div className="mode" role="tablist">
          <button
            type="button"
            role="tab"
            aria-selected={activeTab === 'ai'}
            className={activeTab === 'ai' ? 'selected' : ''}
            onClick={() => setActiveTab('ai')}
          >
            ✦ AI assistant <span className="tab-pill">NEW</span>
          </button>
          <button
            type="button"
            role="tab"
            aria-selected={activeTab === 'manual'}
            className={activeTab === 'manual' ? 'selected' : ''}
            onClick={() => setActiveTab('manual')}
          >
            Manual entry
          </button>
        </div>

        {/* AI Assistant Tab Content */}
        {activeTab === 'ai' && (
          <div className="modalbody" id="aiBody">
            <div className="ai-header-row">
              <div>
                <p className="ai-title">
                  <b>✦ Describe your expense</b>
                </p>
                <p className="aihelper">
                  Explain who paid, what everyone ordered, and any exceptions. I&apos;ll ask for missing details before showing a preview.
                </p>
              </div>
              <div
                className="prompt-counter"
                aria-label={`Prompt count: ${promptCount} of ${MAX_PROMPTS}`}
              >
                Prompts: <b>{promptCount}</b> / {MAX_PROMPTS}
              </div>
            </div>

            {/* Quick Example Suggestions */}
            <div className="examples">
              <button
                type="button"
                className="example"
                onClick={() =>
                  handleSendMessage(
                    'Kayla and I shared the nachos, and everyone but Rui got a margarita. I paid.'
                  )
                }
                disabled={loading || promptCount >= MAX_PROMPTS}
              >
                Try restaurant split
              </button>
              <button
                type="button"
                className="example"
                onClick={() =>
                  handleSendMessage(
                    'I paid $36 for groceries, split between everyone except Rui.'
                  )
                }
                disabled={loading || promptCount >= MAX_PROMPTS}
              >
                Try groceries
              </button>
              <button
                type="button"
                className="example reset-example"
                onClick={handleResetConversation}
                disabled={loading || messages.length === 0}
              >
                Reset conversation
              </button>
            </div>

            {/* Message History */}
            <div
              className="chat"
              id="chat"
              aria-live="polite"
              aria-label="Conversation history"
            >
              {messages.length === 0 ? (
                <div className="chat-empty">
                  Describe how to split your expense in plain English above.
                </div>
              ) : (
                messages.map((msg) => (
                  <div
                    key={msg.id}
                    className={`bubble ${msg.role === 'user' ? 'user' : 'assistant'}`}
                  >
                    <div className="bubble-content">{msg.content}</div>

                    {/* Preview rendered in bubble if present */}
                    {msg.type === 'preview' && msg.preview && (
                      <div className="bubble-preview">
                        <div className="preview-header">
                          <strong>{msg.preview.payer}</strong> paid{' '}
                          <strong>{formatCents(msg.preview.total_cents)}</strong>
                        </div>
                        {msg.preview.items && (
                          <div className="preview-items-list">
                            {msg.preview.items.map((it, idx) => (
                              <div key={idx} className="preview-item-row">
                                <span>{it.description}</span>
                                <span>{formatCents(it.amount_cents)}</span>
                              </div>
                            ))}
                          </div>
                        )}
                        {msg.preview.shares && (
                          <div className="preview-shares-list">
                            <span className="shares-title">Each person&apos;s share:</span>
                            {Object.entries(msg.preview.shares).map(([name, cents]) => (
                              <div key={name} className="preview-share-row">
                                <span>{name}</span>
                                <b>{formatCents(cents)}</b>
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    )}

                    {/* Fallback button if unresolved */}
                    {msg.fallback && (
                      <div className="fallback-action">
                        <button
                          type="button"
                          className="primary btn-switch-manual"
                          onClick={() => setActiveTab('manual')}
                        >
                          Switch to manual entry
                        </button>
                      </div>
                    )}
                  </div>
                ))
              )}

              {loading && (
                <div className="bubble assistant loading" role="status">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                  <span className="loading-text">AI assistant is thinking...</span>
                </div>
              )}

              <div ref={chatBottomRef} />
            </div>

            {/* Itemized Preview with Confirmation */}
            {preview && (
              <ItemizedPreview
                preview={preview}
                conversationId={conversationId}
                currentUser={currentUser}
                onConfirm={(res) => {
                  if (onExpenseConfirmed) {
                    onExpenseConfirmed(res);
                  }
                  setTimeout(() => {
                    onClose();
                  }, 700);
                }}
                onEditInChat={() => {
                  if (inputRef.current) {
                    inputRef.current.focus();
                  }
                }}
                onCancel={() => setPreview(null)}
              />
            )}

            {/* Error Banner */}
            {error && (
              <div className="chat-error" role="alert">
                <span className="error-icon" aria-hidden="true">⚠</span>
                <span className="error-text">{error}</span>
                {lastUserMessage && (
                  <button
                    type="button"
                    className="retry-inline-btn"
                    onClick={handleRetryLastMessage}
                  >
                    Retry
                  </button>
                )}
              </div>
            )}

            {/* Prompt Limit Warning */}
            {promptCount >= MAX_PROMPTS && (
              <div className="prompt-limit-warning" role="alert">
                <span>
                  Maximum prompt limit ({MAX_PROMPTS}) reached for this conversation.
                </span>
                <button
                  type="button"
                  className="primary btn-switch-manual"
                  onClick={() => setActiveTab('manual')}
                >
                  Enter expense manually
                </button>
              </div>
            )}

            {/* Chat Input Field */}
            <div className="sendrow">
              <textarea
                ref={inputRef}
                className="field"
                id="msg"
                placeholder={
                  promptCount >= MAX_PROMPTS
                    ? 'Prompt limit reached. Switch to manual entry.'
                    : 'e.g. Kayla and I shared nachos; everyone but Rui had margaritas…'
                }
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyDown={handleKeyDown}
                disabled={loading || promptCount >= MAX_PROMPTS}
                rows={2}
                aria-label="Describe your expense"
              />
              <button
                type="button"
                className="primary"
                id="send"
                onClick={() => handleSendMessage()}
                disabled={loading || !inputMessage.trim() || promptCount >= MAX_PROMPTS}
              >
                Send ➜
              </button>
            </div>
          </div>
        )}

        {/* Manual Entry Tab Content */}
        {activeTab === 'manual' && (
          <form className="modalbody" id="manual" onSubmit={handleManualSave}>
            <p className="subtle" style={{ marginTop: 0 }}>
              Add an expense the traditional way.
            </p>

            {manualError && (
              <div className="chat-error" role="alert">
                <span className="error-icon" aria-hidden="true">⚠</span>
                <span>{manualError}</span>
              </div>
            )}
            {manualSuccess && (
              <div className="manual-success" role="status">
                ✓ Expense saved successfully!
              </div>
            )}

            <label className="minilabel" htmlFor="desc">
              Description
            </label>
            <input
              className="field"
              id="desc"
              placeholder="e.g. Dinner"
              value={manualDesc}
              onChange={(e) => setManualDesc(e.target.value)}
            />

            <div className="minirow">
              <div style={{ flex: 1 }}>
                <label className="minilabel" htmlFor="amount">
                  Amount ($)
                </label>
                <input
                  className="field"
                  id="amount"
                  type="number"
                  min="0.01"
                  step="0.01"
                  placeholder="0.00"
                  value={manualAmount}
                  onChange={(e) => setManualAmount(e.target.value)}
                />
              </div>

              <div style={{ flex: 1 }}>
                <label className="minilabel" htmlFor="payer">
                  Paid by
                </label>
                <select
                  className="field"
                  id="payer"
                  value={manualPayer}
                  onChange={(e) => setManualPayer(e.target.value)}
                >
                  {(group?.members || []).map((m) => (
                    <option key={m} value={m}>
                      {m}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <label className="minilabel">Split equally between</label>
            <div id="manualMembers" className="minirow checkbox-group">
              {(group?.members || []).map((m) => (
                <label key={m} className="member-checkbox">
                  <input
                    type="checkbox"
                    value={m}
                    checked={manualParticipants.includes(m)}
                    onChange={() => toggleParticipant(m)}
                  />{' '}
                  {m}
                </label>
              ))}
            </div>

            <div className="manualbuttons">
              <button
                type="button"
                className="secondary"
                id="cancelManual"
                onClick={onClose}
              >
                Cancel
              </button>
              <button type="submit" className="primary" id="saveManual">
                Save expense
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}
