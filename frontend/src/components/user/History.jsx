import React, { useState, useEffect, useMemo } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  FaSearch,
  FaFilter,
  FaCalendar,
  FaDownload,
  FaEye,
  FaTrash,
  FaRedo,
  FaLeaf,
  FaCheckCircle,
  FaExclamationTriangle,
  FaShieldAlt,
  FaChartLine,
  FaTrashAlt,
  FaSpinner,
} from 'react-icons/fa';
import { motion, AnimatePresence } from 'framer-motion';
import toast from 'react-hot-toast';
import {
  getPredictionHistory,
  deletePredictionRecord,
  clearPredictionHistory,
} from '../../services/api';

const STORAGE_KEY = 'deepleaf_live_history';

const History = () => {
  const navigate = useNavigate();

  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [severityFilter, setSeverityFilter] = useState('all');
  const [sortBy, setSortBy] = useState('newest');
  const [deletingId, setDeletingId] = useState(null);
  const [clearing, setClearing] = useState(false);

  // Load live detections from backend + local storage cache
  const loadHistory = async () => {
    setLoading(true);

    // 1. Initial hydrate from local storage for instantaneous display
    let localItems = [];
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        localItems = JSON.parse(stored);
      }
    } catch (e) {
      console.warn('Failed to parse local history cache:', e);
    }

    if (Array.isArray(localItems) && localItems.length > 0) {
      setPredictions(localItems);
    }

    // 2. Fetch fresh live records from backend
    try {
      const result = await getPredictionHistory();

      if (result && result.success && Array.isArray(result.predictions)) {
        const backendItems = result.predictions;

        // Map local items by id & filename for preview thumbnail enrichment
        const localMap = new Map();
        localItems.forEach((item) => {
          if (item.id) localMap.set(String(item.id), item);
          if (item.record_id) localMap.set(String(item.record_id), item);
          if (item.filename) localMap.set(item.filename, item);
        });

        // Enrich backend items with preview thumbnails stored locally
        const mergedBackend = backendItems.map((bItem) => {
          const match =
            localMap.get(String(bItem.id)) ||
            localMap.get(String(bItem.record_id)) ||
            localMap.get(bItem.filename);

          return {
            ...bItem,
            preview: bItem.preview || match?.preview || null,
          };
        });

        // Add any local items that might not be synced to backend yet
        const backendIds = new Set(
          mergedBackend.map((item) => String(item.id || item.record_id))
        );
        const unSyncedLocals = localItems.filter(
          (item) => !backendIds.has(String(item.id || item.record_id))
        );

        const combined = [...mergedBackend, ...unSyncedLocals];

        // Sort descending by date
        combined.sort((a, b) => {
          const dateA = new Date(a.created_at || a.date || 0);
          const dateB = new Date(b.created_at || b.date || 0);
          return dateB - dateA;
        });

        setPredictions(combined);
        // Sync back to local storage cache
        try {
          localStorage.setItem(STORAGE_KEY, JSON.stringify(combined.slice(0, 50)));
        } catch (storageErr) {
          console.warn('Unable to persist merged history:', storageErr);
        }
      }
    } catch (error) {
      console.warn('Backend history fetch error, using local cache:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

  // Filter & Search Logic
  const filteredPredictions = useMemo(() => {
    return predictions
      .filter((p) => {
        const term = searchTerm.toLowerCase().trim();
        const plantStr = (p.plant_name || p.plant || '').toLowerCase();
        const diseaseStr = (p.formatted_disease || p.disease || '').toLowerCase();
        const fileStr = (p.filename || '').toLowerCase();

        const matchesSearch =
          !term ||
          plantStr.includes(term) ||
          diseaseStr.includes(term) ||
          fileStr.includes(term);

        const currentStatus = (p.status || '').toLowerCase();
        const matchesStatus =
          statusFilter === 'all' ||
          (statusFilter === 'healthy' && currentStatus === 'healthy') ||
          (statusFilter === 'diseased' && currentStatus === 'diseased');

        const currentSeverity = (p.severity || '').toLowerCase();
        const matchesSeverity =
          severityFilter === 'all' ||
          currentSeverity === severityFilter.toLowerCase();

        return matchesSearch && matchesStatus && matchesSeverity;
      })
      .sort((a, b) => {
        if (sortBy === 'newest') {
          return new Date(b.created_at || b.date || 0) - new Date(a.created_at || a.date || 0);
        }
        if (sortBy === 'oldest') {
          return new Date(a.created_at || a.date || 0) - new Date(b.created_at || b.date || 0);
        }
        if (sortBy === 'confidence_desc') {
          return (Number(b.confidence) || 0) - (Number(a.confidence) || 0);
        }
        if (sortBy === 'confidence_asc') {
          return (Number(a.confidence) || 0) - (Number(b.confidence) || 0);
        }
        return 0;
      });
  }, [predictions, searchTerm, statusFilter, severityFilter, sortBy]);

  // Aggregate Metrics
  const stats = useMemo(() => {
    const total = predictions.length;
    const diseased = predictions.filter(
      (p) => (p.status || '').toLowerCase() === 'diseased'
    ).length;
    const healthy = predictions.filter(
      (p) => (p.status || '').toLowerCase() === 'healthy'
    ).length;
    const avgConfidence =
      total > 0
        ? Math.round(
            predictions.reduce((acc, p) => acc + (Number(p.confidence) || 0), 0) /
              total
          )
        : 0;

    return { total, diseased, healthy, avgConfidence };
  }, [predictions]);

  // Runnable action: Open diagnosis in /result
  const handleViewDiagnosis = (prediction) => {
    navigate('/result', {
      state: {
        ...prediction,
        is_leaf: prediction.is_leaf !== false,
        disease: prediction.disease,
        formatted_disease: prediction.formatted_disease || prediction.disease,
        plant_name: prediction.plant_name || prediction.plant,
        confidence: prediction.confidence,
        status: prediction.status,
        severity: prediction.severity,
        details: prediction.details,
        candidates_comparison: prediction.candidates_comparison || [],
        comparison: prediction.comparison || {},
        top_predictions: prediction.top_predictions || [],
        preview: prediction.preview,
        filename: prediction.filename,
        record_id: prediction.record_id || prediction.id,
      },
    });
  };

  // Runnable action: Re-test / re-run diagnosis
  const handleRetest = (prediction) => {
    navigate('/detection', {
      state: {
        preview: prediction.preview,
        retest: true,
        sourceFilename: prediction.filename,
      },
    });
  };

  // Delete a single live detection
  const handleDelete = async (prediction, e) => {
    e.stopPropagation();
    const idToDelete = prediction.id || prediction.record_id;

    if (!window.confirm(`Delete diagnosis record for "${prediction.formatted_disease || prediction.disease || 'this plant'}"?`)) {
      return;
    }

    setDeletingId(idToDelete);

    try {
      // 1. Delete from backend if persistent ID exists
      if (prediction.record_id || (prediction.id && !String(prediction.id).startsWith('live_'))) {
        await deletePredictionRecord(prediction.record_id || prediction.id);
      }

      // 2. Remove from local state
      const updated = predictions.filter(
        (p) => (p.id || p.record_id) !== idToDelete
      );
      setPredictions(updated);

      // 3. Update localStorage cache
      localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));

      toast.success('Diagnosis record deleted successfully.');
    } catch (err) {
      console.error('Delete error:', err);
      toast.error('Unable to delete from database, removed locally.');
    } finally {
      setDeletingId(null);
    }
  };

  // Clear all history
  const handleClearAll = async () => {
    if (predictions.length === 0) return;

    if (
      !window.confirm(
        'Are you sure you want to clear your entire live prediction history? This action cannot be undone.'
      )
    ) {
      return;
    }

    setClearing(true);

    try {
      await clearPredictionHistory();
      setPredictions([]);
      localStorage.removeItem(STORAGE_KEY);
      toast.success('All live prediction history cleared.');
    } catch (err) {
      console.error('Clear history error:', err);
      setPredictions([]);
      localStorage.removeItem(STORAGE_KEY);
      toast.success('History cleared locally.');
    } finally {
      setClearing(false);
    }
  };

  // Export history as CSV
  const handleExportCSV = () => {
    if (predictions.length === 0) {
      toast.error('No prediction records to export.');
      return;
    }

    const headers = [
      'Record ID',
      'Date & Time',
      'Plant Name',
      'Condition / Disease',
      'Confidence (%)',
      'Health Status',
      'Severity',
      'Filename',
    ];

    const rows = predictions.map((p) => [
      `"${p.id || p.record_id || ''}"`,
      `"${new Date(p.created_at || p.date || Date.now()).toLocaleString()}"`,
      `"${p.plant_name || p.plant || 'Unknown'}"`,
      `"${p.formatted_disease || p.disease || 'Undetected'}"`,
      p.confidence || '0',
      `"${p.status || 'Unknown'}"`,
      `"${p.severity || 'N/A'}"`,
      `"${p.filename || 'image.jpg'}"`,
    ]);

    const csvContent =
      'data:text/csv;charset=utf-8,' +
      [headers.join(','), ...rows.map((e) => e.join(','))].join('\n');

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute(
      'download',
      `deepleaf_diagnosis_history_${new Date().toISOString().slice(0, 10)}.csv`
    );
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    toast.success('Diagnosis history exported to CSV! 📊');
  };

  // Helper date formatter
  const formatDate = (isoOrDate) => {
    if (!isoOrDate) return 'Just now';
    try {
      const d = new Date(isoOrDate);
      if (isNaN(d.getTime())) return String(isoOrDate);
      return d.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    } catch {
      return String(isoOrDate);
    }
  };

  return (
    <div className="min-h-screen py-10 bg-gradient-to-br from-green-50 via-emerald-50/40 to-white">
      <div className="container mx-auto px-4 max-w-7xl">
        {/* Header Bar */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-8">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 bg-green-100 text-green-800 text-xs font-bold rounded-full uppercase tracking-wider mb-2">
              <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
              Live Detection Log
            </div>
            <h1 className="text-3xl font-extrabold text-gray-900 tracking-tight">
              Prediction History
            </h1>
            <p className="text-gray-500 text-sm mt-1">
              Interactive diagnostic records from your real-time plant leaf scans
            </p>
          </div>

          <div className="flex items-center gap-3">
            {predictions.length > 0 && (
              <>
                <button
                  onClick={handleExportCSV}
                  className="inline-flex items-center gap-2 px-4 py-2.5 bg-white border border-gray-200 text-gray-700 rounded-xl font-semibold text-sm hover:bg-gray-50 hover:border-gray-300 shadow-sm transition-all"
                  title="Export to CSV"
                >
                  <FaDownload className="text-green-600 text-xs" />
                  Export CSV
                </button>
                <button
                  onClick={handleClearAll}
                  disabled={clearing}
                  className="inline-flex items-center gap-2 px-4 py-2.5 bg-red-50 border border-red-200 text-red-600 rounded-xl font-semibold text-sm hover:bg-red-100 transition-all disabled:opacity-50"
                  title="Clear All History"
                >
                  <FaTrashAlt className="text-xs" />
                  {clearing ? 'Clearing...' : 'Clear All'}
                </button>
              </>
            )}

            <Link
              to="/detection"
              className="inline-flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white rounded-xl font-semibold text-sm shadow-md shadow-green-600/20 hover:shadow-lg transition-all"
            >
              <FaLeaf className="text-xs" />
              New Detection
            </Link>
          </div>
        </div>

        {/* Live Metrics Overview Bar */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-green-100 flex items-center justify-center text-green-600 text-xl font-bold">
              🌿
            </div>
            <div>
              <p className="text-xs font-semibold text-gray-500 uppercase">Total Scans</p>
              <p className="text-2xl font-extrabold text-gray-900">{stats.total}</p>
            </div>
          </div>

          <div className="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-red-100 flex items-center justify-center text-red-600 text-xl font-bold">
              ⚠️
            </div>
            <div>
              <p className="text-xs font-semibold text-gray-500 uppercase">Diseased Leaves</p>
              <p className="text-2xl font-extrabold text-red-600">{stats.diseased}</p>
            </div>
          </div>

          <div className="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-emerald-100 flex items-center justify-center text-emerald-600 text-xl font-bold">
              ✅
            </div>
            <div>
              <p className="text-xs font-semibold text-gray-500 uppercase">Healthy Crops</p>
              <p className="text-2xl font-extrabold text-emerald-600">{stats.healthy}</p>
            </div>
          </div>

          <div className="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-blue-100 flex items-center justify-center text-blue-600 text-xl font-bold">
              📈
            </div>
            <div>
              <p className="text-xs font-semibold text-gray-500 uppercase">Avg. Certainty</p>
              <p className="text-2xl font-extrabold text-blue-600">
                {stats.avgConfidence}%
              </p>
            </div>
          </div>
        </div>

        {/* Filter and Search Bar */}
        <div className="bg-white rounded-3xl shadow-sm border border-gray-100 p-6 mb-8">
          <div className="flex flex-col lg:flex-row gap-4">
            {/* Search Input */}
            <div className="flex-1 relative">
              <FaSearch className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" />
              <input
                type="text"
                placeholder="Search live diagnoses by plant species, disease name, or filename..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-11 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:bg-white transition-all"
              />
            </div>

            {/* Dropdown Filters */}
            <div className="flex flex-wrap items-center gap-3">
              <div className="flex items-center gap-2">
                <FaFilter className="text-gray-400 text-xs hidden sm:block" />
                <select
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value)}
                  className="px-3.5 py-3 bg-gray-50 border border-gray-200 rounded-xl text-sm font-medium text-gray-700 focus:outline-none focus:ring-2 focus:ring-green-500"
                >
                  <option value="all">All Conditions</option>
                  <option value="healthy">Healthy Only</option>
                  <option value="diseased">Diseased Only</option>
                </select>
              </div>

              <select
                value={severityFilter}
                onChange={(e) => setSeverityFilter(e.target.value)}
                className="px-3.5 py-3 bg-gray-50 border border-gray-200 rounded-xl text-sm font-medium text-gray-700 focus:outline-none focus:ring-2 focus:ring-green-500"
              >
                <option value="all">All Severities</option>
                <option value="high">High Severity</option>
                <option value="moderate">Moderate Severity</option>
                <option value="low">Low Severity</option>
              </select>

              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="px-3.5 py-3 bg-gray-50 border border-gray-200 rounded-xl text-sm font-medium text-gray-700 focus:outline-none focus:ring-2 focus:ring-green-500"
              >
                <option value="newest">Newest First</option>
                <option value="oldest">Oldest First</option>
                <option value="confidence_desc">Highest Certainty</option>
                <option value="confidence_asc">Lowest Certainty</option>
              </select>
            </div>
          </div>
        </div>

        {/* Live History Records Table */}
        <div className="bg-white rounded-3xl shadow-sm border border-gray-100 overflow-hidden">
          {loading && predictions.length === 0 ? (
            <div className="text-center py-20">
              <FaSpinner className="text-4xl text-green-600 animate-spin mx-auto mb-3" />
              <p className="text-gray-500 text-sm font-medium">
                Loading live diagnostic history...
              </p>
            </div>
          ) : filteredPredictions.length === 0 ? (
            <div className="text-center py-20 px-4">
              <div className="w-20 h-20 bg-green-50 text-green-600 rounded-3xl flex items-center justify-center mx-auto mb-4 border border-green-100 shadow-sm">
                <FaLeaf className="text-3xl" />
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-1">
                {predictions.length === 0
                  ? 'No Live Detections Yet'
                  : 'No Matching Detections Found'}
              </h3>
              <p className="text-gray-500 text-sm max-w-md mx-auto mb-6">
                {predictions.length === 0
                  ? 'Your diagnosis history is completely live and will record every plant leaf you analyze. Upload your first crop photo now to get started!'
                  : 'Try clearing your search terms or filters to see all recorded plant diagnoses.'}
              </p>
              {predictions.length === 0 ? (
                <Link
                  to="/detection"
                  className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-xl font-bold shadow-md hover:from-green-700 hover:to-emerald-700 transition-all text-sm"
                >
                  <FaLeaf /> Start Disease Detection
                </Link>
              ) : (
                <button
                  onClick={() => {
                    setSearchTerm('');
                    setStatusFilter('all');
                    setSeverityFilter('all');
                  }}
                  className="inline-flex items-center gap-2 px-5 py-2.5 bg-gray-100 text-gray-700 rounded-xl font-semibold text-sm hover:bg-gray-200 transition-all"
                >
                  Reset Filters
                </button>
              )}
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b border-gray-100 bg-gray-50/70 text-xs font-bold text-gray-500 uppercase tracking-wider">
                    <th className="py-4 px-5">Leaf Sample</th>
                    <th className="py-4 px-5">Plant Species</th>
                    <th className="py-4 px-5">Diagnosis Condition</th>
                    <th className="py-4 px-5">Certainty Score</th>
                    <th className="py-4 px-5">Date & Time</th>
                    <th className="py-4 px-5">Health Status</th>
                    <th className="py-4 px-5 text-right">Runnable Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  <AnimatePresence>
                    {filteredPredictions.map((item, idx) => {
                      const recordId = item.id || item.record_id || `row_${idx}`;
                      const isHealthy =
                        (item.status || '').toLowerCase() === 'healthy';
                      const plant =
                        item.plant_name || item.plant || 'Crop Specimen';
                      const disease =
                        item.formatted_disease ||
                        item.disease ||
                        'Undetected Condition';
                      const confidence = Number(item.confidence) || 0;

                      return (
                        <motion.tr
                          key={recordId}
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          exit={{ opacity: 0, height: 0 }}
                          transition={{ duration: 0.2 }}
                          onClick={() => handleViewDiagnosis(item)}
                          className="hover:bg-green-50/60 transition-colors cursor-pointer group"
                        >
                          {/* Thumbnail / Leaf Image */}
                          <td className="py-3.5 px-5">
                            <div className="w-12 h-12 rounded-xl overflow-hidden bg-gray-100 border border-gray-200 flex items-center justify-center shrink-0 shadow-xs">
                              {item.preview ? (
                                <img
                                  src={item.preview}
                                  alt={plant}
                                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-200"
                                />
                              ) : (
                                <FaLeaf className="text-green-600 text-lg opacity-70" />
                              )}
                            </div>
                          </td>

                          {/* Plant Species */}
                          <td className="py-3.5 px-5">
                            <div className="font-bold text-gray-900 group-hover:text-green-700 transition-colors">
                              {plant}
                            </div>
                            <div className="text-xs text-gray-400 truncate max-w-[150px]">
                              {item.filename || 'Camera scan'}
                            </div>
                          </td>

                          {/* Diagnosis / Condition */}
                          <td className="py-3.5 px-5">
                            <div className="font-semibold text-gray-800 text-sm flex items-center gap-1.5">
                              {disease}
                            </div>
                            {item.severity && item.severity !== 'None' && (
                              <span className="text-[11px] text-gray-400 font-medium">
                                Severity: {item.severity}
                              </span>
                            )}
                          </td>

                          {/* Certainty Confidence */}
                          <td className="py-3.5 px-5">
                            <div className="flex items-center gap-2">
                              <div className="w-16 bg-gray-100 rounded-full h-2 overflow-hidden">
                                <div
                                  className={`h-full rounded-full ${
                                    confidence >= 80
                                      ? 'bg-green-500'
                                      : confidence >= 60
                                      ? 'bg-amber-500'
                                      : 'bg-red-500'
                                  }`}
                                  style={{ width: `${Math.min(confidence, 100)}%` }}
                                ></div>
                              </div>
                              <span
                                className={`text-xs font-extrabold ${
                                  confidence >= 80
                                    ? 'text-green-700'
                                    : confidence >= 60
                                    ? 'text-amber-700'
                                    : 'text-red-700'
                                }`}
                              >
                                {confidence.toFixed(1)}%
                              </span>
                            </div>
                          </td>

                          {/* Date & Time */}
                          <td className="py-3.5 px-5 text-xs text-gray-500 whitespace-nowrap">
                            {formatDate(item.created_at || item.date)}
                          </td>

                          {/* Status Badge */}
                          <td className="py-3.5 px-5 whitespace-nowrap">
                            <span
                              className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold ${
                                isHealthy
                                  ? 'bg-emerald-100 text-emerald-800 border border-emerald-200'
                                  : 'bg-red-100 text-red-800 border border-red-200'
                              }`}
                            >
                              {isHealthy ? (
                                <FaCheckCircle className="text-[10px]" />
                              ) : (
                                <FaExclamationTriangle className="text-[10px]" />
                              )}
                              {isHealthy ? 'Healthy' : 'Diseased'}
                            </span>
                          </td>

                          {/* Runnable Action Buttons */}
                          <td className="py-3.5 px-5 text-right whitespace-nowrap">
                            <div
                              className="inline-flex items-center gap-1"
                              onClick={(e) => e.stopPropagation()}
                            >
                              {/* Runnable 1: View Full Diagnosis */}
                              <button
                                onClick={() => handleViewDiagnosis(item)}
                                className="p-2 rounded-lg bg-green-50 text-green-700 hover:bg-green-600 hover:text-white transition-colors shadow-xs"
                                title="Run & View Complete Diagnosis Report"
                              >
                                <FaEye className="text-sm" />
                              </button>

                              {/* Runnable 2: Re-run / Re-test */}
                              <button
                                onClick={() => handleRetest(item)}
                                className="p-2 rounded-lg bg-blue-50 text-blue-700 hover:bg-blue-600 hover:text-white transition-colors shadow-xs"
                                title="Re-run Diagnosis with this leaf image"
                              >
                                <FaRedo className="text-xs" />
                              </button>

                              {/* Runnable 3: Delete */}
                              <button
                                onClick={(e) => handleDelete(item, e)}
                                disabled={deletingId === recordId}
                                className="p-2 rounded-lg bg-red-50 text-red-600 hover:bg-red-600 hover:text-white transition-colors shadow-xs disabled:opacity-50"
                                title="Delete this diagnosis record"
                              >
                                <FaTrash className="text-xs" />
                              </button>
                            </div>
                          </td>
                        </motion.tr>
                      );
                    })}
                  </AnimatePresence>
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default History;
