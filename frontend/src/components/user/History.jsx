import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { FaSearch, FaFilter, FaCalendar, FaDownload, FaEye } from 'react-icons/fa';
import { motion } from 'framer-motion';

const History = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filter, setFilter] = useState('all');

  const predictions = [
    { id: 1, plant: 'Tomato', disease: 'Early Blight', confidence: 92, date: '2026-07-30', status: 'Diseased' },
    { id: 2, plant: 'Potato', disease: 'Late Blight', confidence: 88, date: '2026-07-29', status: 'Diseased' },
    { id: 3, plant: 'Apple', disease: 'Healthy', confidence: 98, date: '2026-07-28', status: 'Healthy' },
    { id: 4, plant: 'Wheat', disease: 'Rust', confidence: 85, date: '2026-07-27', status: 'Diseased' },
    { id: 5, plant: 'Rice', disease: 'Healthy', confidence: 96, date: '2026-07-26', status: 'Healthy' },
  ];

  const filteredPredictions = predictions.filter(p => {
    const matchesSearch = p.plant.toLowerCase().includes(searchTerm.toLowerCase()) || 
                          p.disease.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filter === 'all' || p.status.toLowerCase() === filter;
    return matchesSearch && matchesFilter;
  });

  return (
    <div className="min-h-screen py-12 bg-gradient-to-br from-green-50 via-emerald-50 to-white">
      <div className="container mx-auto px-4">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="max-w-6xl mx-auto">
          <div className="flex items-center justify-between mb-8">
            <div>
              <h1 className="text-3xl font-bold text-dark-900">Prediction History</h1>
              <p className="text-gray-500 mt-1">View all your past disease predictions</p>
            </div>
            <Link to="/detection" className="px-6 py-3 bg-green-500 text-white rounded-xl font-semibold hover:bg-green-600 transition-all">
              New Detection
            </Link>
          </div>

          <div className="bg-white rounded-3xl shadow-lg p-6">
            <div className="flex flex-col md:flex-row gap-4 mb-6">
              <div className="flex-1 relative">
                <FaSearch className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search by plant or disease..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-500"
                />
              </div>
              <div className="flex gap-3">
                <select
                  value={filter}
                  onChange={(e) => setFilter(e.target.value)}
                  className="px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-500"
                >
                  <option value="all">All Status</option>
                  <option value="healthy">Healthy</option>
                  <option value="diseased">Diseased</option>
                </select>
                <button className="px-4 py-3 bg-gray-100 rounded-xl hover:bg-gray-200 transition-colors">
                  <FaCalendar />
                </button>
                <button className="px-4 py-3 bg-gray-100 rounded-xl hover:bg-gray-200 transition-colors">
                  <FaDownload />
                </button>
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200">
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-500">Plant</th>
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-500">Disease</th>
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-500">Confidence</th>
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-500">Date</th>
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-500">Status</th>
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-500">Action</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredPredictions.map((prediction) => (
                    <motion.tr
                      key={prediction.id}
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      className="border-b border-gray-100 hover:bg-green-50 transition-colors"
                    >
                      <td className="py-3 px-4 font-semibold text-dark-900">{prediction.plant}</td>
                      <td className="py-3 px-4 text-gray-600">{prediction.disease}</td>
                      <td className="py-3 px-4">
                        <span className="font-semibold text-green-600">{prediction.confidence}%</span>
                      </td>
                      <td className="py-3 px-4 text-gray-500">{prediction.date}</td>
                      <td className="py-3 px-4">
                        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                          prediction.status === 'Healthy' 
                            ? 'bg-green-100 text-green-600' 
                            : 'bg-red-100 text-red-600'
                        }`}>
                          {prediction.status}
                        </span>
                      </td>
                      <td className="py-3 px-4">
                        <Link to={`/result/${prediction.id}`} className="text-green-600 hover:text-green-700">
                          <FaEye />
                        </Link>
                      </td>
                    </motion.tr>
                  ))}
                </tbody>
              </table>
            </div>

            {filteredPredictions.length === 0 && (
              <div className="text-center py-8">
                <p className="text-gray-500">No predictions found</p>
              </div>
            )}
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default History;