import { useState, useEffect, useCallback } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import GroupView from './components/GroupView';
import RightSidebar from './components/RightSidebar';
import LoadingSpinner from './components/LoadingSpinner';
import ErrorMessage from './components/ErrorMessage';
import NamePicker from './components/NamePicker';
import AddExpenseModal from './components/AddExpenseModal';
import {
  fetchGroups,
  fetchGroupBalances,
  fetchSession,
  login,
  logout,
} from './api';
import './App.css';

export default function App() {
  const [currentUser, setCurrentUser] = useState(null);
  const [groups, setGroups] = useState([]);
  const [selectedGroupId, setSelectedGroupId] = useState(null);
  const [balances, setBalances] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isSwitchingUser, setIsSwitchingUser] = useState(false);
  const [isAddExpenseOpen, setIsAddExpenseOpen] = useState(false);

  const loadUserGroups = useCallback(async () => {
    setError(null);
    try {
      const groupsList = await fetchGroups();
      setGroups(groupsList || []);
      if (groupsList && groupsList.length > 0) {
        setSelectedGroupId((prev) => (prev !== null ? prev : groupsList[0].id));
      }
    } catch (err) {
      setError(
        err.message || 'Failed to load groups. Please check your backend connection.'
      );
    }
  }, []);

  useEffect(() => {
    let ignore = false;

    async function initSession() {
      try {
        const session = await fetchSession();
        if (!ignore && session && session.name) {
          setCurrentUser(session.name);
          const groupsList = await fetchGroups();
          if (!ignore) {
            setGroups(groupsList || []);
            if (groupsList && groupsList.length > 0) {
              setSelectedGroupId((prev) => (prev !== null ? prev : groupsList[0].id));
            }
          }
        } else {
          if (!ignore) {
            setCurrentUser(null);
          }
        }
      } catch (err) {
        // If session check itself throws, treat as unauthenticated
        // If session succeeded but fetchGroups failed, report error
        if (!ignore) {
          if (err && err.status === 401) {
            setCurrentUser(null);
          } else {
            // Check if we have a session
            try {
              const check = await fetchSession();
              if (check && check.name) {
                setCurrentUser(check.name);
                setError(err.message || 'Failed to load groups.');
              } else {
                setCurrentUser(null);
              }
            } catch {
              setCurrentUser(null);
            }
          }
        }
      } finally {
        if (!ignore) {
          setLoading(false);
        }
      }
    }

    initSession();

    return () => {
      ignore = true;
    };
  }, []);

  useEffect(() => {
    if (!selectedGroupId || !currentUser) return;

    let isMounted = true;
    fetchGroupBalances(selectedGroupId)
      .then((data) => {
        if (isMounted) {
          setBalances(data || {});
        }
      })
      .catch(() => {
        if (isMounted) {
          setBalances({});
        }
      });

    return () => {
      isMounted = false;
    };
  }, [selectedGroupId, currentUser]);

  const handleLogin = async (name) => {
    const session = await login(name);
    setCurrentUser(session.name);
    setIsSwitchingUser(false);
    setError(null);
    await loadUserGroups();
  };

  const handleLogout = async () => {
    try {
      await logout();
    } catch {
      // Continue client cleanup even if network fails
    }
    setCurrentUser(null);
    setGroups([]);
    setSelectedGroupId(null);
    setBalances({});
    setIsSwitchingUser(false);
    setError(null);
  };

  const handleSwitchUser = () => {
    setIsSwitchingUser(true);
  };

  const activeGroup = groups.find((g) => g.id === selectedGroupId) || null;

  return (
    <div className="app-container">
      <Header
        currentUser={currentUser}
        onSwitchUser={currentUser ? handleSwitchUser : undefined}
        onSignOut={currentUser ? handleLogout : undefined}
      />

      {loading ? (
        <LoadingSpinner message="Loading application..." />
      ) : !currentUser ? (
        <NamePicker onSelectUser={handleLogin} />
      ) : error ? (
        <ErrorMessage
          title="Unable to load groups"
          message={error}
          onRetry={loadUserGroups}
        />
      ) : (
        <>
          <div className="layout">
            <Sidebar
              groups={groups}
              selectedGroupId={selectedGroupId}
              onSelectGroup={setSelectedGroupId}
              friends={activeGroup?.members}
              currentUser={currentUser}
            />
            <GroupView
              group={activeGroup}
              balances={balances}
              currentUser={currentUser}
              onAddExpense={() => setIsAddExpenseOpen(true)}
            />
            <RightSidebar
              members={activeGroup?.members}
              balances={balances}
              currentUser={currentUser}
            />
          </div>

          {isAddExpenseOpen && (
            <AddExpenseModal
              isOpen={isAddExpenseOpen}
              onClose={() => setIsAddExpenseOpen(false)}
              group={activeGroup}
              currentUser={currentUser}
              onExpenseConfirmed={() => {
                // Refresh group balances on expense save
                if (selectedGroupId) {
                  fetchGroupBalances(selectedGroupId)
                    .then((data) => setBalances(data || {}))
                    .catch(() => {});
                }
              }}
            />
          )}

          {isSwitchingUser && (
            <NamePicker
              isModal
              currentUserName={currentUser}
              onSelectUser={handleLogin}
              onCancel={() => setIsSwitchingUser(false)}
            />
          )}
        </>
      )}
    </div>
  );
}
