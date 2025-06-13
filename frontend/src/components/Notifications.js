import React, { useState, useEffect } from "react";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Notifications = () => {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");

  useEffect(() => {
    fetchNotifications();
    // Set up polling for real-time notifications
    const interval = setInterval(fetchNotifications, 30000); // Poll every 30 seconds
    return () => clearInterval(interval);
  }, [filter]);

  const fetchNotifications = async () => {
    try {
      const params = new URLSearchParams();
      if (filter === "unread") params.append('unread_only', 'true');
      
      const response = await axios.get(`${API}/notifications?${params.toString()}`);
      setNotifications(response.data);
    } catch (error) {
      console.error("Error fetching notifications:", error);
    } finally {
      setLoading(false);
    }
  };

  const markAsRead = async (notificationId) => {
    try {
      await axios.put(`${API}/notifications/${notificationId}/read`);
      setNotifications(notifications.map(notif => 
        notif.id === notificationId 
          ? { ...notif, is_read: true, read_at: new Date().toISOString() }
          : notif
      ));
    } catch (error) {
      console.error("Error marking notification as read:", error);
    }
  };

  const markAllAsRead = async () => {
    const unreadNotifications = notifications.filter(n => !n.is_read);
    try {
      await Promise.all(
        unreadNotifications.map(notif => 
          axios.put(`${API}/notifications/${notif.id}/read`)
        )
      );
      fetchNotifications();
    } catch (error) {
      console.error("Error marking all notifications as read:", error);
    }
  };

  const getNotificationIcon = (type) => {
    switch (type) {
      case 'payment_due':
        return '💰';
      case 'promise_due':
        return '🤝';
      case 'escalation':
        return '⚠️';
      default:
        return '📢';
    }
  };

  const getNotificationColor = (type) => {
    switch (type) {
      case 'payment_due':
        return 'bg-yellow-50 border-yellow-200';
      case 'promise_due':
        return 'bg-blue-50 border-blue-200';
      case 'escalation':
        return 'bg-red-50 border-red-200';
      default:
        return 'bg-gray-50 border-gray-200';
    }
  };

  const unreadCount = notifications.filter(n => !n.is_read).length;

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="mb-6">
        <div className="flex justify-between items-center mb-4">
          <h1 className="text-3xl font-bold text-gray-900">Notifications</h1>
          {unreadCount > 0 && (
            <button
              onClick={markAllAsRead}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium"
            >
              Mark All as Read ({unreadCount})
            </button>
          )}
        </div>
        
        {/* Filter Buttons */}
        <div className="flex space-x-4">
          <button
            onClick={() => setFilter("all")}
            className={`px-4 py-2 rounded-lg text-sm font-medium ${
              filter === "all"
                ? "bg-blue-600 text-white"
                : "bg-gray-200 text-gray-700 hover:bg-gray-300"
            }`}
          >
            All Notifications
          </button>
          <button
            onClick={() => setFilter("unread")}
            className={`px-4 py-2 rounded-lg text-sm font-medium ${
              filter === "unread"
                ? "bg-blue-600 text-white"
                : "bg-gray-200 text-gray-700 hover:bg-gray-300"
            }`}
          >
            Unread ({unreadCount})
          </button>
        </div>
      </div>

      {/* Notifications List */}
      <div className="space-y-4">
        {notifications.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-gray-500 text-lg mb-2">📭</div>
            <p className="text-gray-500">
              {filter === "unread" ? "No unread notifications" : "No notifications found"}
            </p>
          </div>
        ) : (
          notifications.map((notification) => (
            <div
              key={notification.id}
              className={`border rounded-lg p-4 transition-all duration-200 hover:shadow-md ${
                notification.is_read 
                  ? "bg-white border-gray-200 opacity-75" 
                  : `${getNotificationColor(notification.notification_type)} shadow-sm`
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex items-start space-x-3">
                  <div className="text-2xl">
                    {getNotificationIcon(notification.notification_type)}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center space-x-2">
                      <h3 className="text-lg font-semibold text-gray-900">
                        {notification.title}
                      </h3>
                      {!notification.is_read && (
                        <span className="w-2 h-2 bg-blue-500 rounded-full"></span>
                      )}
                    </div>
                    <p className="text-gray-700 mt-1">
                      {notification.message}
                    </p>
                    <div className="flex items-center space-x-4 mt-3 text-sm text-gray-500">
                      <span>
                        {new Date(notification.sent_at).toLocaleString()}
                      </span>
                      <span className="capitalize">
                        {notification.notification_type.replace('_', ' ')}
                      </span>
                      <span className="capitalize">
                        {notification.recipient_type}
                      </span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  {!notification.is_read && (
                    <button
                      onClick={() => markAsRead(notification.id)}
                      className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                    >
                      Mark as Read
                    </button>
                  )}
                  {notification.is_read && (
                    <span className="text-xs text-gray-400">
                      Read {new Date(notification.read_at).toLocaleDateString()}
                    </span>
                  )}
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Generate Sample Notifications for Demo */}
      <div className="mt-8 p-4 bg-gray-50 rounded-lg">
        <h3 className="text-lg font-semibold text-gray-900 mb-3">Demo Actions</h3>
        <div className="space-x-3">
          <button
            onClick={() => {
              // Simulate creating notifications
              const sampleNotifications = [
                {
                  id: Date.now() + 1,
                  recipient_id: "demo_user",
                  recipient_type: "agent",
                  notification_type: "payment_due",
                  title: "Payment Overdue Alert",
                  message: "Member STM10001 has a payment overdue by 15 days. Outstanding: KES 125,000",
                  is_read: false,
                  sent_at: new Date().toISOString()
                },
                {
                  id: Date.now() + 2,
                  recipient_id: "demo_user",
                  recipient_type: "agent",
                  notification_type: "promise_due",
                  title: "Promise to Pay Due Today",
                  message: "Member STM10002 promised to pay KES 50,000 today. Follow up required.",
                  is_read: false,
                  sent_at: new Date().toISOString()
                },
                {
                  id: Date.now() + 3,
                  recipient_id: "demo_user",
                  recipient_type: "agent",
                  notification_type: "escalation",
                  title: "Case Escalated to External Partner",
                  message: "Loan LN12345 has been escalated to Elite Recovery Services for collection.",
                  is_read: false,
                  sent_at: new Date().toISOString()
                }
              ];
              setNotifications([...sampleNotifications, ...notifications]);
            }}
            className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg text-sm font-medium"
          >
            Generate Sample Notifications
          </button>
          <button
            onClick={() => setNotifications([])}
            className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg text-sm font-medium"
          >
            Clear All Notifications
          </button>
        </div>
      </div>
    </div>
  );
};

export default Notifications;
