
import { useState, useEffect, useCallback } from 'react';

import Header from './components/Header';
import Sidebar from './components/Sidebar';
import GroupView from './components/GroupView';
import RightSidebar from './components/RightSidebar';
import LoadingSpinner from './components/LoadingSpinner';
import ErrorMessage from './components/ErrorMessage';
import NamePicker from './components/NamePicker';
import AddExpenseModal from './components/AddExpenseModal';
import GroupManagementModal from './components/GroupManagementModal';

import {
  fetchGroups,
  fetchGroup,
  fetchGroupExpenses,
  fetchSession,
  login,
  logout,
} from './api';

import './App.css';

export default function App() {
  const [currentUser, setCurrentUser] = useState(null);
  const [groups, setGroups] = useState([]);
  const [selectedGroupId, setSelectedGroupId] = useState(null);

  const [details, setDetails] = useState(null);
  const [expenses, setExpenses] = useState([]);
  const [refreshKey, setRefreshKey] = useState(0);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [isSwitchingUser, setIsSwitchingUser] = useState(false);
  const [isAddExpenseOpen, setIsAddExpenseOpen] = useState(false);
  const [groupModalMode, setGroupModalMode] = useState(null);

  const loadUserGroups = useCallback(async () => {
    setError(null);

    try {
      const groupsList = await fetchGroups();
      const availableGroups = groupsList || [];

      setGroups(availableGroups);

      setSelectedGroupId((previous) => {
        if (
          previous !== null &&
          availableGroups.some(
            (group) => group.id === previous
          )
        ) {
          return previous;
        }

        return availableGroups.length > 0
          ? availableGroups[0].id
          : null;
      });
    } catch (err) {
      setError(
        err.message ||
        'Failed to load groups. Please check your backend connection.'
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
            const availableGroups = groupsList || [];

            setGroups(availableGroups);

            setSelectedGroupId((previous) => {
              if (
                previous !== null &&
                availableGroups.some(
                  (group) => group.id === previous
                )
              ) {
                return previous;
              }

              return availableGroups.length > 0
                ? availableGroups[0].id
                : null;
            });
          }
        } else if (!ignore) {
          setCurrentUser(null);
        }
      } catch (err) {
        if (!ignore) {
          if (err && err.status === 401) {
            setCurrentUser(null);
          } else {
            try {
              const check = await fetchSession();

              if (check && check.name) {
                setCurrentUser(check.name);
                setError(
                  err.message || 'Failed to load groups.'
                );
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
    if (!selectedGroupId || !currentUser) {
      setDetails(null);
      setExpenses([]);
      return;
    }

    let isMounted = true;

    Promise.all([
      fetchGroup(selectedGroupId),
      fetchGroupExpenses(selectedGroupId),
    ])
      .then(([groupDetails, groupExpenses]) => {
        if (isMounted) {
          setDetails(groupDetails || null);
          setExpenses(groupExpenses || []);
        }
      })
      .catch(() => {
        if (isMounted) {
          setDetails(null);
          setExpenses([]);
        }
      });

    return () => {
      isMounted = false;
    };
  }, [selectedGroupId, currentUser, refreshKey]);

  const handleLogin = async (name) => {
    const session = await login(name);

    setCurrentUser(session.name);
    setIsSwitchingUser(false);
    setError(null);

    await loadUserGroups();
    setRefreshKey((key) => key + 1);
  };

  const handleLogout = async () => {
    try {
      await logout();
    } catch {
      // Clear local state even if logout fails.
    }

    setCurrentUser(null);
    setGroups([]);
    setSelectedGroupId(null);
    setDetails(null);
    setExpenses([]);
    setIsSwitchingUser(false);
    setIsAddExpenseOpen(false);
    setGroupModalMode(null);
    setError(null);
  };

  const handleSwitchUser = () => {
    setIsSwitchingUser(true);
  };

  const handleGroupCreated = async (newGroup) => {
    setGroups((previous) => {
      if (
        previous.some((group) => group.id === newGroup.id)
      ) {
        return previous;
      }

      return [...previous, newGroup];
    });

    setSelectedGroupId(newGroup.id);
    setDetails(null);
    setExpenses([]);
    setRefreshKey((key) => key + 1);
    setGroupModalMode(null);
  };

  const handleMemberAdded = async (updatedGroup) => {
    setGroups((previous) =>
      previous.map((group) =>
        group.id === updatedGroup.id
          ? updatedGroup
          : group
      )
    );

    setRefreshKey((key) => key + 1);
    setGroupModalMode(null);
  };

  const activeGroup =
    groups.find(
      (group) => group.id === selectedGroupId
    ) || null;

  return (
    <div className="app-container">
      <Header
        currentUser={currentUser}
        onSwitchUser={
          currentUser ? handleSwitchUser : undefined
        }
        onSignOut={
          currentUser ? handleLogout : undefined
        }
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
              onCreateGroup={() =>
                setGroupModalMode('create')
              }
              onAddFriend={() =>
                setGroupModalMode('add-member')
              }
            />

            <GroupView
              group={activeGroup}
              summary={
                details?.id === selectedGroupId
                  ? details.summary
                  : undefined
              }
              expenses={
                details?.id === selectedGroupId
                  ? expenses
                  : []
              }
              currentUser={currentUser}
              onAddExpense={() =>
                setIsAddExpenseOpen(true)
              }
              onAddMember={() =>
                setGroupModalMode('add-member')
              }
            />

            <RightSidebar
              balances={
                details?.id === selectedGroupId
                  ? details.balances
                  : []
              }
            />
          </div>

          {isAddExpenseOpen && (
            <AddExpenseModal
              isOpen={isAddExpenseOpen}
              onClose={() =>
                setIsAddExpenseOpen(false)
              }
              group={activeGroup}
              currentUser={currentUser}
              onExpenseConfirmed={() =>
                setRefreshKey((key) => key + 1)
              }
            />
          )}

          {groupModalMode && (
            <GroupManagementModal
              mode={groupModalMode}
              group={activeGroup}
              onClose={() =>
                setGroupModalMode(null)
              }
              onSuccess={
                groupModalMode === 'create'
                  ? handleGroupCreated
                  : handleMemberAdded
              }
            />
          )}

          {isSwitchingUser && (
            <NamePicker
              isModal
              currentUserName={currentUser}
              onSelectUser={handleLogin}
              onCancel={() =>
                setIsSwitchingUser(false)
              }
            />
          )}
        </>
      )}
    </div>
  );
}
