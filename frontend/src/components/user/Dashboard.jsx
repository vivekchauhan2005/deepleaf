import React from 'react';
import { Link } from 'react-router-dom';
import { FaLeaf, FaHistory, FaPlus, FaUser, FaChartLine, FaCheckCircle, FaExclamationTriangle, FaArrowRight } from 'react-icons/fa';
import { motion } from 'framer-motion';
import { useAuth } from '../../context/AuthContext';

const Dashboard = () => {
  const { user } = useAuth();

  const stats = [
    { icon: FaChartLine, value: '24', label: 'Total Predictions', color: 'from-blue-500 to-blue-600' },
    { icon: FaCheckCircle, value: '16', label: 'Healthy Plants', color: 'from-green-500 to-green-600' },
    { icon: FaExclamationTriangle, value: '8', label: 'Diseased Plants', color: 'from-red-500 to-red-600' },
    { icon: FaUser, value: '95%', label: 'Accuracy Rate', color: 'from-purple-500 to-purple-600' },
  ];

  const recentPredictions = [
    { name: 'Tomato Leaf', disease: 'Early Blight', confidence: '90%', status: '⚠️' },
    { name: 'Potato Leaf', disease: 'Late Blight', confidence: '92%', status: '⚠️' },
    { name: 'Apple Leaf', disease: 'Healthy', confidence: '98%', status: '✅' },
  ];

  return (
    <div className="min-h-screen py-12 bg-gradient-to-br from-green-50 via-emerald-50 to-white">
      <div className="container mx-auto px-4">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="max-w-6xl mx-auto">
          <div className="bg-white rounded-3xl shadow-lg p-8 mb-8">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-dark-900">Welcome, {user?.name || 'User'}! 👋</h1>
                <p className="text-gray-500 mt-1">Here's what's happening with your plants today.</p>
              </div>
              <Link to="/detection" className="px-6 py-3 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-xl font-semibold hover:scale-105 transition-all flex items-center space-x-2">
                <FaPlus />
                <span>New Detection</span>
              </Link>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {stats.map((stat, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="bg-white rounded-2xl shadow-lg p-6 hover-card"
              >
                <div className={`w-12 h-12 bg-gradient-to-r ${stat.color} rounded-xl flex items-center justify-center text-white text-xl mb-3`}>
                  <stat.icon />
                </div>
                <div className="text-2xl font-bold text-dark-900">{stat.value}</div>
                <div className="text-gray-500 text-sm">{stat.label}</div>
              </motion.div>
            ))}
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold text-dark-900">Recent Predictions</h2>
                <Link to="/history" className="text-green-600 hover:text-green-700 flex items-center space-x-1 text-sm">
                  <span>View All</span>
                  <FaArrowRight />
                </Link>
              </div>
              <div className="space-y-3">
                {recentPredictions.map((item, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-xl hover:bg-green-50 transition-colors">
                    <div className="flex items-center space-x-3">
                      <div className="text-2xl">{item.status}</div>
                      <div>
                        <div className="font-semibold text-dark-900">{item.name}</div>
                        <div className="text-sm text-gray-500">{item.disease}</div>
                      </div>
                    </div>
                    <div className="font-bold text-green-600">{item.confidence}</div>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h2 className="text-xl font-bold text-dark-900 mb-4">Quick Actions</h2>
              <div className="grid grid-cols-2 gap-4">
                <Link to="/detection" className="p-4 bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl text-center hover:shadow-lg transition-all hover:scale-105">
                  <FaLeaf className="text-3xl text-green-500 mx-auto mb-2" />
                  <div className="font-semibold text-dark-900">New Detection</div>
                  <div className="text-xs text-gray-500">Upload & Analyze</div>
                </Link>
                <Link to="/history" className="p-4 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl text-center hover:shadow-lg transition-all hover:scale-105">
                  <FaHistory className="text-3xl text-blue-500 mx-auto mb-2" />
                  <div className="font-semibold text-dark-900">History</div>
                  <div className="text-xs text-gray-500">View Past Results</div>
                </Link>
                <Link to="/remedies" className="p-4 bg-gradient-to-br from-yellow-50 to-orange-50 rounded-xl text-center hover:shadow-lg transition-all hover:scale-105">
                  <FaLeaf className="text-3xl text-yellow-500 mx-auto mb-2" />
                  <div className="font-semibold text-dark-900">Remedies</div>
                  <div className="text-xs text-gray-500">Expert Solutions</div>
                </Link>
                <Link to="/profile" className="p-4 bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl text-center hover:shadow-lg transition-all hover:scale-105">
                  <FaUser className="text-3xl text-purple-500 mx-auto mb-2" />
                  <div className="font-semibold text-dark-900">Profile</div>
                  <div className="text-xs text-gray-500">Manage Account</div>
                </Link>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Dashboard;