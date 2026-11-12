
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  FaLeaf,
  FaHistory,
  FaPlus,
  FaUser,
  FaChartLine,
  FaCheckCircle,
  FaExclamationTriangle,
  FaArrowRight,
} from 'react-icons/fa';
import { motion } from 'framer-motion';
import { useAuth } from '../../context/AuthContext';

const API_URL = 'http://127.0.0.1:8002';

const Dashboard = () => {
  const { user } = useAuth();

  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const controller = new AbortController();

    const fetchDashboard = async () => {
      setLoading(true);
      setError('');

      try {
        const token = localStorage.getItem('token');

        if (!token) {
          throw new Error('Please log in to view your dashboard.');
        }

        const response = await fetch(`${API_URL}/predict/dashboard`, {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${token}`,
          },
          signal: controller.signal,
        });

        const data = await response.json();

        if (response.status === 401) {
          throw new Error('Your session has expired. Please log in again.');
        }

        if (!response.ok) {
          throw new Error(
            typeof data.detail === 'string'
              ? data.detail
              : 'Unable to load dashboard data.'
          );
        }

        if (data.success !== true) {
          throw new Error('The backend returned an invalid dashboard response.');
        }

        setDashboard(data);
      } catch (err) {
        if (err.name !== 'AbortError') {
          setError(err.message || 'Unable to load dashboard data.');
        }
      } finally {
        if (!controller.signal.aborted) {
          setLoading(false);
        }
      }
    };

    fetchDashboard();

    return () => controller.abort();
  }, []);

  const stats = [
    {
      icon: FaChartLine,
      value: dashboard?.total_predictions ?? 0,
      label: 'Total Predictions',
      color: 'from-blue-500 to-blue-600',
    },
    {
      icon: FaCheckCircle,
      value: dashboard?.healthy_count ?? 0,
      label: 'Healthy Plants',
      color: 'from-green-500 to-green-600',
    },
    {
      icon: FaExclamationTriangle,
      value: dashboard?.diseased_count ?? 0,
      label: 'Diseased Plants',
      color: 'from-red-500 to-red-600',
    },
  ];

  const recentPredictions = dashboard?.recent_predictions ?? [];

  const getResultLabel = (item) => {
    if (item.is_leaf === false) {
      return 'No plant leaf detected';
    }

    if (!item.disease) {
      return 'Disease not confirmed';
    }

    const disease = item.disease.replaceAll('___', ' — ').replaceAll('_', ' ');

    return disease.trim();
  };

  const isHealthy = (disease) =>
    typeof disease === 'string' &&
    /(^|___)healthy$/i.test(disease.trim());

  const formatDate = (value) => {
    if (!value) return 'Date unavailable';

    const date = new Date(value);

    if (Number.isNaN(date.getTime())) return 'Date unavailable';

    return date.toLocaleString(undefined, {
      dateStyle: 'medium',
      timeStyle: 'short',
    });
  };

  const formatConfidence = (confidence) => {
    if (
      confidence === null ||
      confidence === undefined ||
      confidence === '' ||
      !Number.isFinite(Number(confidence))
    ) {
      return 'N/A';
    }

    return `${Number(confidence).toFixed(1)}%`;
  };

  return (
    <div className="min-h-screen py-12 bg-gradient-to-br from-green-50 via-emerald-50 to-white">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="max-w-6xl mx-auto"
        >
          {/* Welcome */}
          <div className="bg-white rounded-3xl shadow-lg p-8 mb-8">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-5">
              <div>
                <h1 className="text-3xl font-bold text-dark-900">
                  Welcome, {user?.name || user?.username || user?.email || 'User'}! 👋
                </h1>
                <p className="text-gray-500 mt-2">
                  Here is your plant disease detection activity.
                </p>
                <p className="text-sm text-gray-400 mt-1">
                  Your dashboard is based on your saved prediction history.
                </p>
              </div>

              <Link
                to="/detection"
                className="px-6 py-3 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-xl font-semibold hover:scale-105 transition-all flex items-center justify-center space-x-2"
              >
                <FaPlus />
                <span>New Detection</span>
              </Link>
            </div>
          </div>

          {/* Loading */}
          {loading && (
            <div
              className="bg-white rounded-2xl shadow-lg p-8 mb-8 text-center"
              role="status"
            >
              <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-green-600 mx-auto mb-4" />
              <p className="text-gray-600">Loading your real dashboard data...</p>
            </div>
          )}

          {/* Error */}
          {!loading && error && (
            <div
              className="bg-white rounded-2xl shadow-lg p-6 mb-8 border border-red-100"
              role="alert"
            >
              <h2 className="font-bold text-red-600 mb-2">
                Dashboard data could not be loaded
              </h2>
              <p className="text-gray-600">{error}</p>
              <button
                type="button"
                onClick={() => window.location.reload()}
                className="mt-4 px-5 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
              >
                Try Again
              </button>
            </div>
          )}

          {/* Live statistics */}
          {!loading && !error && dashboard && (
            <>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                {stats.map((stat, index) => (
                  <motion.div
                    key={stat.label}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="bg-white rounded-2xl shadow-lg p-6 hover-card"
                  >
                    <div
                      className={`w-12 h-12 bg-gradient-to-r ${stat.color} rounded-xl flex items-center justify-center text-white text-xl mb-3`}
                    >
                      <stat.icon />
                    </div>
                    <div className="text-2xl font-bold text-dark-900">
                      {stat.value}
                    </div>
                    <div className="text-gray-500 text-sm">{stat.label}</div>
                  </motion.div>
                ))}
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Recent predictions from MongoDB */}
                <div className="bg-white rounded-2xl shadow-lg p-6">
                  <div className="flex items-center justify-between mb-5">
                    <h2 className="text-xl font-bold text-dark-900">
                      Recent Predictions
                    </h2>
                    <Link
                      to="/history"
                      className="text-green-600 hover:text-green-700 flex items-center space-x-1 text-sm"
                    >
                      <span>View All</span>
                      <FaArrowRight />
                    </Link>
                  </div>

                  {recentPredictions.length === 0 ? (
                    <div className="text-center py-10">
                      <FaLeaf className="text-4xl text-green-300 mx-auto mb-3" />
                      <p className="font-semibold text-gray-700">
                        No predictions yet
                      </p>
                      <p className="text-sm text-gray-500 mt-1">
                        Your saved results will appear here after your first detection.
                      </p>
                      <Link
                        to="/detection"
                        className="inline-flex mt-4 px-5 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
                      >
                        Start Detection
                      </Link>
                    </div>
                  ) : (
                    <div className="space-y-3">
                      {recentPredictions.map((item) => {
                        const healthy = isHealthy(item.disease);
                        const confirmedDisease =
                          item.is_leaf === true &&
                          Boolean(item.disease) &&
                          !healthy;

                        return (
                          <div
                            key={item.id}
                            className="flex items-start justify-between gap-3 p-4 bg-gray-50 rounded-xl hover:bg-green-50 transition-colors"
                          >
                            <div className="flex items-start gap-3 min-w-0">
                              <div
                                className={`w-10 h-10 shrink-0 rounded-lg flex items-center justify-center ${
                                  healthy
                                    ? 'bg-green-100 text-green-600'
                                    : confirmedDisease
                                      ? 'bg-red-100 text-red-600'
                                      : 'bg-gray-200 text-gray-600'
                                }`}
                              >
                                {healthy ? (
                                  <FaCheckCircle />
                                ) : confirmedDisease ? (
                                  <FaExclamationTriangle />
                                ) : (
                                  <FaLeaf />
                                )}
                              </div>

                              <div className="min-w-0">
                                <p className="font-semibold text-dark-900 break-words">
                                  {item.filename || 'Uploaded image'}
                                </p>
                                <p className="text-sm text-gray-600 break-words mt-1">
                                  {getResultLabel(item)}
                                </p>
                                <p className="text-xs text-gray-400 mt-2">
                                  {formatDate(item.created_at)}
                                </p>
                              </div>
                            </div>

                            <div className="text-right shrink-0">
                              <p className="font-bold text-gray-700">
                                {formatConfidence(item.confidence)}
                              </p>
                              <p className="text-xs text-gray-400 mt-1">
                                Confidence
                              </p>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  )}
                </div>

                {/* Quick actions */}
                <div className="bg-white rounded-2xl shadow-lg p-6">
                  <h2 className="text-xl font-bold text-dark-900 mb-4">
                    Quick Actions
                  </h2>

                  <div className="grid grid-cols-2 gap-4">
                    <Link
                      to="/detection"
                      className="p-4 bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl text-center hover:shadow-lg transition-all hover:scale-105"
                    >
                      <FaLeaf className="text-3xl text-green-500 mx-auto mb-2" />
                      <div className="font-semibold text-dark-900">
                        New Detection
                      </div>
                      <div className="text-xs text-gray-500">
                        Upload & Analyze
                      </div>
                    </Link>

                    <Link
                      to="/history"
                      className="p-4 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl text-center hover:shadow-lg transition-all hover:scale-105"
                    >
                      <FaHistory className="text-3xl text-blue-500 mx-auto mb-2" />
                      <div className="font-semibold text-dark-900">History</div>
                      <div className="text-xs text-gray-500">
                        View Past Results
                      </div>
                    </Link>

                    <Link
                      to="/remedies"
                      className="p-4 bg-gradient-to-br from-yellow-50 to-orange-50 rounded-xl text-center hover:shadow-lg transition-all hover:scale-105"
                    >
                      <FaLeaf className="text-3xl text-yellow-500 mx-auto mb-2" />
                      <div className="font-semibold text-dark-900">Remedies</div>
                      <div className="text-xs text-gray-500">
                        Expert Solutions
                      </div>
                    </Link>

                    <Link
                      to="/profile"
                      className="p-4 bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl text-center hover:shadow-lg transition-all hover:scale-105"
                    >
                      <FaUser className="text-3xl text-purple-500 mx-auto mb-2" />
                      <div className="font-semibold text-dark-900">Profile</div>
                      <div className="text-xs text-gray-500">
                        Manage Account
                      </div>
                    </Link>
                  </div>
                </div>
              </div>
            </>
          )}
        </motion.div>
      </div>
    </div>
  );
};

export default Dashboard;
