import React, { useState, useEffect } from 'react';
import { Link, useLocation, useNavigate, useParams } from 'react-router-dom';
import { getPredictionRecord } from '../../services/api';
import {
  FaLeaf,
  FaCheckCircle,
  FaExclamationTriangle,
  FaArrowLeft,
  FaDownload,
  FaShareAlt,
  FaShieldAlt,
  FaVial,
  FaSeedling,
  FaTint,
  FaSun,
  FaChartBar,
  FaChartLine,
  FaInfoCircle,
  FaCamera,
  FaNotesMedical,
  FaSpinner,
} from 'react-icons/fa';
import { motion, AnimatePresence } from 'framer-motion';

const PredictionResult = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { id } = useParams();
  const [prediction, setPrediction] = useState(location.state || null);
  const [loadingRecord, setLoadingRecord] = useState(false);

  const [activeTab, setActiveTab] = useState('overview');
  const [activeGraphMode, setActiveGraphMode] = useState('prediction'); // 'prediction' | 'benchmark'

  useEffect(() => {
    if (location.state) {
      setPrediction(location.state);
      return;
    }

    const resolveRecord = async () => {
      let candidate = null;
      try {
        const raw = localStorage.getItem('deepleaf_live_history');
        if (raw) {
          const list = JSON.parse(raw);
          if (Array.isArray(list) && list.length > 0) {
            if (id) {
              candidate = list.find(
                (item) => String(item.id) === String(id) || String(item.record_id) === String(id)
              );
            }
            if (!candidate && !id) {
              candidate = list[0];
            }
          }
        }
      } catch (e) {
        // ignore
      }

      if (candidate) {
        setPrediction(candidate);
        return;
      }

      if (id) {
        setLoadingRecord(true);
        try {
          const remote = await getPredictionRecord(id);
          if (remote) {
            setPrediction(remote);
          }
        } catch (err) {
          console.warn('Could not fetch prediction record:', err);
        } finally {
          setLoadingRecord(false);
        }
      }
    };

    resolveRecord();
  }, [id, location.state]);

  if (loadingRecord) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 via-emerald-50 to-white px-4">
        <div className="bg-white rounded-3xl shadow-xl p-8 text-center max-w-md border border-gray-100">
          <FaSpinner className="text-4xl text-green-600 animate-spin mx-auto mb-4" />
          <h2 className="text-xl font-bold text-gray-800 mb-1">Loading Diagnosis...</h2>
          <p className="text-gray-500 text-sm">Retrieving your plant disease analysis</p>
        </div>
      </div>
    );
  }

  if (!prediction) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 via-emerald-50 to-white px-4">
        <div className="bg-white rounded-3xl shadow-xl p-8 text-center max-w-md border border-gray-100">
          <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4 text-green-600">
            <FaLeaf className="text-4xl" />
          </div>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">No Prediction Found</h2>
          <p className="text-gray-500 mb-6 text-sm">
            Please upload a plant leaf image first to run the AI diagnosis.
          </p>
          <Link
            to="/detection"
            className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-xl font-semibold shadow-md hover:from-green-700 hover:to-emerald-700 transition-all"
          >
            Start Disease Detection
          </Link>
        </div>
      </div>
    );
  }

  const isLeaf = !(
    prediction.is_leaf === false ||
    String(prediction.is_leaf).toLowerCase() === 'false'
  );

  const disease = prediction.disease || 'Unknown';
  const confidenceValue = prediction.confidence;
  const confidence = Number(confidenceValue);
  const hasConfidence =
    confidenceValue !== null &&
    confidenceValue !== undefined &&
    confidenceValue !== '' &&
    Number.isFinite(confidence);

  const preview =
    prediction.preview ||
    prediction.imagePreview ||
    prediction.image_data_url ||
    prediction.imageUrl ||
    prediction.image_url ||
    prediction.image ||
    null;

  const filename = prediction.filename || 'Uploaded Image';
  const message = prediction.message || 'Analysis completed successfully.';

  // Structured details from backend
  const details = prediction.details || null;
  const topPredictions = Array.isArray(prediction.top_predictions)
    ? prediction.top_predictions
    : [];

  const candidatesComparison = Array.isArray(prediction.candidates_comparison)
    ? prediction.candidates_comparison
    : [];
  const comparisonGraphBase64 =
    prediction.comparison_graph_base64 ||
    prediction.comparisonGraphBase64 ||
    null;

  const plantName =
    prediction.plant_name ||
    details?.plant_name ||
    (disease.includes('___') ? disease.split('___')[0].replace(/_/g, ' ') : 'Plant');

  const scientificName = details?.scientific_name || `${plantName} sp.`;
  const plantFamily = details?.family || 'Plantae';

  const formatDiseaseName = (name) => {
    if (!name) return 'Unknown Condition';
    return name.replace(/___/g, ' - ').replace(/_/g, ' ');
  };

  const formattedDisease =
    prediction.formatted_disease ||
    details?.disease_name ||
    formatDiseaseName(disease);

  const isHealthy =
    disease.toLowerCase().includes('healthy') ||
    details?.status?.toLowerCase() === 'healthy';

  const status = isHealthy ? 'Healthy' : 'Diseased';
  const severity = details?.severity || prediction.severity || (isHealthy ? 'None' : 'Moderate');
  const pathogenType = details?.pathogen_type || (isHealthy ? 'None' : 'Pathogen');
  const causalAgent = details?.causal_agent || 'Identified by DeepLeaf AI';

  const symptoms = details?.symptoms || [
    `Foliar patterns consistent with ${formattedDisease}`,
    'Visual discoloration or texture changes on leaf blade',
  ];

  const causes = details?.causes || [
    'Environmental humidity and favorable temperature conditions',
    'Foliar pathogens or airborne spores',
  ];

  const immediateActions = details?.immediate_actions || [
    'Isolate affected plant from healthy crops',
    'Remove heavily spotted or wilted leaves and dispose of safely',
    'Avoid overhead watering; water strictly at soil level',
  ];

  const organicTreatments = details?.organic_treatments || [
    'Apply copper fungicide or potassium bicarbonate spray at recommended rates',
    'Use neem oil or biofungicide to protect new growth',
  ];

  const chemicalTreatments = details?.chemical_treatments || [
    'Consult local agricultural extension guidelines for approved crop treatments',
  ];

  const preventionTips = details?.prevention_tips || [
    'Ensure adequate spacing between plants to maximize canopy airflow',
    'Practice crop rotation and use disease-resistant cultivars',
  ];

  const fertilizerCare = details?.fertilizer_and_care || [
    'Maintain balanced soil fertility and avoid excessive late-season nitrogen',
  ];

  const photographyTips = prediction.photography_tips || [
    'Place a single leaf in sharp focus against a plain or natural background',
    'Ensure bright, even lighting without heavy shadows or lens glare',
    'Fill most of the camera frame with the leaf blade',
    'Capture visible spots, discoloration, or lesions clearly',
  ];

  const comparison = prediction.comparison || {};
  const cnnComparison = comparison.cnn || {};
  const vggComparison = comparison.vgg19 || {};
  const modelsAgree =
    prediction.models_agree ??
    (cnnComparison.disease && vggComparison.disease
      ? cnnComparison.disease === vggComparison.disease
      : false);

  const getSeverityBadgeClass = (sev) => {
    switch (String(sev).toLowerCase()) {
      case 'none':
        return 'bg-emerald-100 text-emerald-800 border-emerald-300';
      case 'low':
        return 'bg-blue-100 text-blue-800 border-blue-300';
      case 'moderate':
        return 'bg-amber-100 text-amber-800 border-amber-300';
      case 'high':
        return 'bg-orange-100 text-orange-800 border-orange-300';
      case 'severe':
      case 'critical':
        return 'bg-rose-100 text-rose-800 border-rose-300';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  const handleShare = async () => {
    const shareText = isLeaf
      ? `DeepLeaf AI Diagnosis: ${plantName} - ${formattedDisease} (${hasConfidence ? `${confidence.toFixed(1)}% confidence` : 'analyzed'})`
      : `DeepLeaf AI: ${message}`;

    try {
      if (navigator.share) {
        await navigator.share({
          title: 'DeepLeaf Plant Health Diagnosis',
          text: shareText,
        });
      } else {
        await navigator.clipboard.writeText(shareText);
        alert('Diagnosis summary copied to clipboard!');
      }
    } catch (err) {
      console.log('Share cancelled or unavailable', err);
    }
  };

  const handleDownload = async () => {
    const canvas = document.createElement('canvas');
    canvas.width = 1200;
    canvas.height = 2500;
    const ctx = canvas.getContext('2d');

    if (!ctx) {
      alert('Unable to initialize report canvas. Please try again.');
      return;
    }

    // Background
    ctx.fillStyle = '#f8fafc';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Header banner
    const gradient = ctx.createLinearGradient(0, 0, canvas.width, 0);
    gradient.addColorStop(0, '#047857');
    gradient.addColorStop(1, '#059669');
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, canvas.width, 220);

    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 50px Arial';
    ctx.fillText('🌿 DeepLeaf AI', 70, 85);
    ctx.font = 'bold 26px Arial';
    ctx.fillText('Comprehensive Plant Pathology & Disease Diagnosis Report', 70, 135);
    ctx.font = '18px Arial';
    ctx.fillText(`Generated: ${new Date().toLocaleString()}  |  DeepLeaf 2.0 Diagnostic Engine`, 70, 180);

    let y = 260;
    const left = 70;
    const cardWidth = canvas.width - left * 2;

    const drawCard = (height, bg = '#ffffff') => {
      ctx.fillStyle = bg;
      ctx.strokeStyle = '#e2e8f0';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.roundRect(left, y, cardWidth, height, 16);
      ctx.fill();
      ctx.stroke();
    };

    // Card 1: Executive Summary
    drawCard(380);
    ctx.fillStyle = '#0f172a';
    ctx.font = 'bold 30px Arial';
    ctx.fillText('1. Diagnostic Summary', left + 35, y + 50);

    // Thumbnail
    if (preview) {
      try {
        const reportImg = new Image();
        reportImg.crossOrigin = 'anonymous';
        await new Promise((res, rej) => {
          reportImg.onload = res;
          reportImg.onerror = rej;
          reportImg.src = preview;
        });
        const thumbW = 240;
        const thumbH = 240;
        ctx.drawImage(reportImg, left + 35, y + 80, thumbW, thumbH);
      } catch (e) {
        console.warn('Preview draw skipped', e);
      }
    }

    const colX = left + 310;
    const writeField = (label, val, rowY, valColor = '#0f172a') => {
      ctx.fillStyle = '#64748b';
      ctx.font = 'bold 18px Arial';
      ctx.fillText(label, colX, rowY);
      ctx.fillStyle = valColor;
      ctx.font = 'bold 20px Arial';
      ctx.fillText(String(val || 'N/A'), colX + 170, rowY);
    };

    writeField('Plant Species:', `${plantName} (${scientificName})`, y + 105);
    writeField('Diagnosis:', formattedDisease, y + 145, isHealthy ? '#059669' : '#dc2626');
    writeField('Health Status:', isHealthy ? 'Healthy Leaf' : 'Infected / Diseased', y + 185);
    writeField('Confidence:', hasConfidence ? `${confidence.toFixed(1)}%` : 'Analyzed', y + 225, '#059669');
    writeField('Severity Level:', severity, y + 265);
    writeField('Pathogen Type:', pathogenType, y + 305);

    y += 415;

    // Card 2: Symptoms & Pathogen Info
    drawCard(380);
    ctx.fillStyle = '#0f172a';
    ctx.font = 'bold 28px Arial';
    ctx.fillText('2. Symptoms & Diagnostic Findings', left + 35, y + 45);

    ctx.fillStyle = '#475569';
    ctx.font = '18px Arial';
    let sy = y + 85;
    symptoms.slice(0, 4).forEach((s) => {
      ctx.fillText(`•  ${s}`, left + 45, sy);
      sy += 34;
    });

    sy += 10;
    ctx.fillStyle = '#0f172a';
    ctx.font = 'bold 22px Arial';
    ctx.fillText('Environmental Causes & Triggers:', left + 35, sy);
    sy += 32;
    ctx.fillStyle = '#475569';
    ctx.font = '18px Arial';
    causes.slice(0, 3).forEach((c) => {
      ctx.fillText(`•  ${c}`, left + 45, sy);
      sy += 32;
    });

    y += 415;

    // Card 3: Actionable Treatment Plan
    drawCard(460);
    ctx.fillStyle = '#0f172a';
    ctx.font = 'bold 28px Arial';
    ctx.fillText('3. Treatment & Recovery Plan', left + 35, y + 45);

    let ty = y + 85;
    ctx.fillStyle = '#dc2626';
    ctx.font = 'bold 20px Arial';
    ctx.fillText('Immediate First-Aid Actions:', left + 35, ty);
    ty += 30;
    ctx.fillStyle = '#334155';
    ctx.font = '17px Arial';
    immediateActions.slice(0, 3).forEach((act) => {
      ctx.fillText(`1. ${act}`, left + 45, ty);
      ty += 28;
    });

    ty += 15;
    ctx.fillStyle = '#059669';
    ctx.font = 'bold 20px Arial';
    ctx.fillText('Organic & Biological Remedies:', left + 35, ty);
    ty += 30;
    ctx.fillStyle = '#334155';
    ctx.font = '17px Arial';
    organicTreatments.slice(0, 2).forEach((org) => {
      ctx.fillText(`• ${org}`, left + 45, ty);
      ty += 28;
    });

    ty += 15;
    ctx.fillStyle = '#2563eb';
    ctx.font = 'bold 20px Arial';
    ctx.fillText('Approved Chemical Treatments:', left + 35, ty);
    ty += 30;
    ctx.fillStyle = '#334155';
    ctx.font = '17px Arial';
    chemicalTreatments.slice(0, 2).forEach((chem) => {
      ctx.fillText(`• ${chem}`, left + 45, ty);
      ty += 28;
    });

    y += 490;

    // Card 4: Long-Term Prevention
    drawCard(320);
    ctx.fillStyle = '#0f172a';
    ctx.font = 'bold 28px Arial';
    ctx.fillText('4. Preventive Best Practices & Irrigation', left + 35, y + 45);

    let py = y + 85;
    ctx.fillStyle = '#334155';
    ctx.font = '18px Arial';
    preventionTips.slice(0, 3).forEach((tip) => {
      ctx.fillText(`✔  ${tip}`, left + 45, py);
      py += 34;
    });

    py += 15;
    ctx.fillStyle = '#0f172a';
    ctx.font = 'bold 20px Arial';
    ctx.fillText('Soil & Fertilization Guidance:', left + 35, py);
    py += 30;
    ctx.fillStyle = '#334155';
    ctx.font = '18px Arial';
    fertilizerCare.slice(0, 2).forEach((f) => {
      ctx.fillText(`✔  ${f}`, left + 45, py);
      py += 32;
    });

    y += 350;

    // Card 5: AI Model Verification & Transparency
    drawCard(280);
    ctx.fillStyle = '#0f172a';
    ctx.font = 'bold 26px Arial';
    ctx.fillText('5. DeepLeaf Multi-Model Consensus', left + 35, y + 45);

    ctx.fillStyle = '#475569';
    ctx.font = '18px Arial';
    ctx.fillText(
      `Primary Model (VGG19 Retrained - 97.3% accuracy): ${vggComparison.confidence ? `${vggComparison.confidence}%` : 'Evaluated'}`,
      left + 45,
      y + 90
    );
    ctx.fillText(
      `Secondary Model (Custom CNN Classifier): ${cnnComparison.confidence ? `${cnnComparison.confidence}%` : 'Evaluated'}`,
      left + 45,
      y + 125
    );
    ctx.fillText(
      `Multi-Model Agreement: ${modelsAgree ? 'Strong Consensus (Both models agree)' : 'Differential Analysis Active'}`,
      left + 45,
      y + 160
    );
    ctx.fillText(
      `Leaf Integrity Score: ${prediction.leaf_confidence ? `${prediction.leaf_confidence}% confirmed foliage` : 'Verified'}`,
      left + 45,
      y + 195
    );

    // Footer
    ctx.fillStyle = '#64748b';
    ctx.font = '16px Arial';
    ctx.fillText(
      'DeepLeaf AI Plant Pathology System  •  Agricultural decision support only. Confirm with local extension experts before applying restricted chemicals.',
      left,
      canvas.height - 40
    );

    canvas.toBlob((blob) => {
      if (!blob) {
        alert('Could not export report image.');
        return;
      }
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `DeepLeaf-Diagnosis-${plantName}-${formattedDisease.replace(/\s+/g, '_')}-${new Date().toISOString().slice(0, 10)}.png`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      URL.revokeObjectURL(url);
    }, 'image/png');
  };

  // -------------------------------------------------------------
  // NON-LEAF VIEW
  // -------------------------------------------------------------
  if (!isLeaf) {
    return (
      <div className="min-h-screen py-12 bg-gradient-to-br from-green-50 via-emerald-50 to-white">
        <div className="container mx-auto px-4 max-w-4xl">
          <div className="flex items-center justify-between mb-6">
            <button
              onClick={() => navigate('/detection')}
              className="inline-flex items-center space-x-2 text-green-700 hover:text-green-800 font-medium"
            >
              <FaArrowLeft />
              <span>Back to Upload</span>
            </button>
          </div>

          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-3xl shadow-xl overflow-hidden border border-amber-200"
          >
            <div className="bg-gradient-to-r from-amber-500 to-orange-500 p-8 text-white">
              <div className="flex items-center space-x-3 mb-2">
                <FaExclamationTriangle className="text-3xl text-amber-100" />
                <h1 className="text-3xl font-bold">Plant Leaf Not Confirmed</h1>
              </div>
              <p className="text-amber-100 text-sm">
                Our AI leaf-verification model could not detect clear crop foliage in this image.
              </p>
            </div>

            <div className="p-8">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
                <div>
                  {preview ? (
                    <div className="bg-gray-50 rounded-2xl p-4 border border-gray-200">
                      <img
                        src={preview}
                        alt="Uploaded input"
                        className="w-full max-h-80 object-contain rounded-xl"
                      />
                      <p className="text-xs text-gray-500 text-center mt-3 break-all">
                        {filename}
                      </p>
                    </div>
                  ) : (
                    <div className="bg-amber-50 rounded-2xl p-12 text-center text-amber-500">
                      <FaCamera className="text-6xl mx-auto mb-3" />
                      <p className="font-medium">No preview available</p>
                    </div>
                  )}
                </div>

                <div>
                  <div className="inline-flex items-center px-3.5 py-1.5 rounded-full text-xs font-semibold bg-amber-100 text-amber-800 mb-4">
                    <FaInfoCircle className="mr-1.5" />
                    Verification Confidence: {prediction.leaf_confidence ? `${prediction.leaf_confidence}% non-leaf` : 'High'}
                  </div>

                  <h2 className="text-2xl font-bold text-gray-900 mb-3">
                    Why was this image not analyzed?
                  </h2>

                  <p className="text-gray-600 mb-6 leading-relaxed">
                    {message}
                  </p>

                  <div className="bg-emerald-50 rounded-2xl p-5 border border-emerald-200 mb-6">
                    <h3 className="font-bold text-emerald-900 text-sm mb-3 flex items-center">
                      <FaCamera className="mr-2 text-emerald-600" />
                      Tips for Best Diagnosis Accuracy:
                    </h3>
                    <ul className="space-y-2 text-xs text-emerald-800">
                      {photographyTips.map((tip, idx) => (
                        <li key={idx} className="flex items-start">
                          <span className="text-emerald-500 font-bold mr-2">✓</span>
                          <span>{tip}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  <Link
                    to="/detection"
                    className="w-full inline-flex justify-center items-center px-6 py-3.5 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white rounded-xl font-semibold shadow-md transition-all"
                  >
                    Upload a Plant Leaf Image
                  </Link>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    );
  }

  // -------------------------------------------------------------
  // LEAF DIAGNOSIS VIEW (Detailed, Smooth, Professional)
  // -------------------------------------------------------------
  return (
    <div className="min-h-screen py-10 bg-gradient-to-br from-green-50 via-emerald-50 to-slate-50 text-gray-800">
      <div className="container mx-auto px-4 max-w-5xl">
        {/* Top bar */}
        <div className="flex items-center justify-between mb-6">
          <button
            onClick={() => navigate('/detection')}
            className="inline-flex items-center space-x-2 text-green-700 hover:text-green-800 font-semibold transition-colors"
          >
            <FaArrowLeft />
            <span>New Diagnosis</span>
          </button>

          <div className="flex items-center space-x-3">
            <button
              onClick={() => {
                const el = document.getElementById('model-comparison-section');
                if (el) {
                  el.scrollIntoView({ behavior: 'smooth' });
                }
              }}
              className="inline-flex items-center space-x-2 px-3.5 py-2 bg-blue-50 border border-blue-200 text-blue-700 hover:bg-blue-100 rounded-xl shadow-sm transition-all text-sm font-semibold"
              title="View CNN vs VGG-19 Comparison Line Graph"
            >
              <FaChartLine className="text-blue-600" />
              <span className="hidden sm:inline">Model Comparison</span>
            </button>

            <button
              onClick={handleShare}
              className="inline-flex items-center space-x-2 px-4 py-2 bg-white rounded-xl shadow-sm border border-gray-200 text-gray-700 hover:text-green-600 hover:border-green-300 transition-all text-sm font-medium"
              title="Share Diagnosis"
            >
              <FaShareAlt />
              <span className="hidden sm:inline">Share</span>
            </button>

            <button
              onClick={handleDownload}
              className="inline-flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-xl shadow-sm hover:from-green-700 hover:to-emerald-700 transition-all text-sm font-semibold"
              title="Download Full Report"
            >
              <FaDownload />
              <span>Download Report</span>
            </button>
          </div>
        </div>

        {/* Hero Card */}
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-3xl shadow-xl overflow-hidden border border-gray-100 mb-8"
        >
          {/* Header Gradient */}
          <div
            className={`p-8 text-white ${
              isHealthy
                ? 'bg-gradient-to-r from-emerald-600 via-green-600 to-teal-600'
                : 'bg-gradient-to-r from-emerald-700 via-teal-800 to-slate-900'
            }`}
          >
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
              <div>
                <div className="flex items-center space-x-3 mb-2 flex-wrap gap-2">
                  <span
                    className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-bold border ${getSeverityBadgeClass(
                      severity
                    )}`}
                  >
                    {isHealthy ? (
                      <FaCheckCircle className="mr-1.5" />
                    ) : (
                      <FaExclamationTriangle className="mr-1.5" />
                    )}
                    {isHealthy ? 'Optimal Health' : `${severity} Severity`}
                  </span>

                  {modelsAgree && (
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-white/20 backdrop-blur-sm text-white">
                      <FaShieldAlt className="mr-1.5 text-emerald-300" />
                      Dual-Model Consensus
                    </span>
                  )}
                </div>

                <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight">
                  {formattedDisease}
                </h1>

                <p className="text-emerald-100 text-base mt-1 flex items-center gap-2">
                  <span className="font-semibold text-white">{plantName}</span>
                  <span>•</span>
                  <span className="italic opacity-90">{scientificName}</span>
                  <span>•</span>
                  <span className="opacity-75">{plantFamily}</span>
                </p>
              </div>

              {/* Confidence Metric Box */}
              <div className="flex md:flex-col items-center justify-between md:justify-center bg-white/10 backdrop-blur-md rounded-2xl p-4 md:px-6 border border-white/20 min-w-[170px]">
                <div className="text-4xl md:text-5xl font-black text-white tracking-tight">
                  {hasConfidence ? `${confidence.toFixed(1)}%` : 'Analyzed'}
                </div>
                <div className="text-xs uppercase font-bold tracking-wider text-emerald-200 mt-0.5">
                  Diagnosis Certainty
                </div>
              </div>
            </div>
          </div>

          {/* Quick summary strip */}
          <div className="p-6 bg-slate-50 border-b border-gray-100 flex flex-wrap items-center justify-between gap-4 text-xs sm:text-sm text-gray-600">
            <div className="flex items-center space-x-2">
              <span className="font-semibold text-gray-800">Status:</span>
              <span
                className={`font-bold ${isHealthy ? 'text-emerald-600' : 'text-rose-600'}`}
              >
                {status}
              </span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="font-semibold text-gray-800">Pathogen:</span>
              <span>{pathogenType}</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="font-semibold text-gray-800">Causal Agent:</span>
              <span className="italic">{causalAgent}</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="font-semibold text-gray-800">Foliage Quality:</span>
              <span className="text-emerald-600 font-semibold">
                {prediction.leaf_confidence ? `${prediction.leaf_confidence}% verified` : 'High'}
              </span>
            </div>
          </div>

          {/* Main Content Layout */}
          <div className="p-8">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
              {/* Left Column: Image preview + AI confidence breakdown */}
              <div className="lg:col-span-4 space-y-6">
                <div className="bg-gray-50 rounded-2xl p-4 border border-gray-200 shadow-inner">
                  {preview ? (
                    <img
                      src={preview}
                      alt="Diagnosed plant leaf"
                      className="w-full max-h-72 object-contain rounded-xl shadow-sm"
                    />
                  ) : (
                    <div className="w-full h-56 bg-emerald-50 rounded-xl flex items-center justify-center text-emerald-600">
                      <FaLeaf className="text-6xl" />
                    </div>
                  )}
                  <div className="mt-3 text-center">
                    <p className="text-xs font-medium text-gray-500 truncate" title={filename}>
                      {filename}
                    </p>
                  </div>
                </div>

                {/* AI Probability Spectrum */}
                <div className="bg-slate-50 rounded-2xl p-5 border border-gray-200">
                  <h3 className="font-bold text-gray-900 text-sm mb-3 flex items-center">
                    <FaChartBar className="mr-2 text-emerald-600" />
                    Top Diagnostic Candidates:
                  </h3>
                  <div className="space-y-3">
                    {topPredictions.length > 0 ? (
                      topPredictions.map((cand, idx) => (
                        <div key={idx} className="space-y-1">
                          <div className="flex justify-between text-xs">
                            <span className="font-medium text-gray-700 truncate max-w-[180px]">
                              {cand.disease}
                            </span>
                            <span className="font-bold text-gray-900">
                              {cand.probability.toFixed(1)}%
                            </span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
                            <div
                              className={`h-full rounded-full transition-all duration-500 ${
                                idx === 0 ? 'bg-emerald-500' : 'bg-gray-400'
                              }`}
                              style={{ width: `${Math.min(cand.probability, 100)}%` }}
                            />
                          </div>
                        </div>
                      ))
                    ) : (
                      <div className="text-xs text-gray-500">
                        {formattedDisease}: {confidence.toFixed(1)}%
                      </div>
                    )}
                  </div>

                  <div className="mt-4 pt-3 border-t border-gray-200 text-[11px] text-gray-500 flex justify-between">
                    <span>Primary: VGG19 ({vggComparison.confidence ?? confidence.toFixed(1)}%)</span>
                    <span>CNN: {cnnComparison.confidence ? `${cnnComparison.confidence}%` : 'N/A'}</span>
                  </div>

                  <button
                    onClick={() => {
                      const el = document.getElementById('model-comparison-section');
                      if (el) {
                        el.scrollIntoView({ behavior: 'smooth' });
                      }
                    }}
                    className="mt-3 w-full inline-flex items-center justify-center gap-1.5 py-2 px-3 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white rounded-xl text-xs font-semibold shadow-sm transition"
                  >
                    <FaChartLine />
                    <span>View CNN vs VGG-19 Line Graph ↓</span>
                  </button>
                </div>
              </div>

              {/* Right Column: Interactive Tabs for Detailed Info */}
              <div className="lg:col-span-8">
                {/* Navigation Tabs */}
                <div className="flex border-b border-gray-200 mb-6 overflow-x-auto scrollbar-none gap-2">
                  {[
                    { id: 'overview', label: 'Diagnosis & Symptoms', icon: FaNotesMedical },
                    { id: 'treatment', label: 'Treatment & Remedies', icon: FaVial },
                    { id: 'prevention', label: 'Prevention & Care', icon: FaShieldAlt },
                  ].map((tab) => {
                    const Icon = tab.icon;
                    const isActive = activeTab === tab.id;
                    return (
                      <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        className={`inline-flex items-center space-x-2 py-3 px-4 font-semibold text-sm border-b-2 whitespace-nowrap transition-all ${
                          isActive
                            ? 'border-emerald-600 text-emerald-700 bg-emerald-50/50 rounded-t-xl'
                            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                        }`}
                      >
                        <Icon className={isActive ? 'text-emerald-600' : 'text-gray-400'} />
                        <span>{tab.label}</span>
                      </button>
                    );
                  })}
                </div>

                {/* Tab 1: Overview & Symptoms */}
                {activeTab === 'overview' && (
                  <motion.div
                    initial={{ opacity: 0, y: 6 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="space-y-6"
                  >
                    <div>
                      <h3 className="text-lg font-bold text-gray-900 mb-2">Description & Condition</h3>
                      <p className="text-gray-600 leading-relaxed text-sm">
                        {details?.description || message}
                      </p>
                    </div>

                    {/* Symptoms Checklist */}
                    <div className="bg-emerald-50/60 rounded-2xl p-5 border border-emerald-100">
                      <h4 className="font-bold text-emerald-950 text-sm mb-3 flex items-center">
                        <FaCheckCircle className="mr-2 text-emerald-600" />
                        Diagnostic Hallmarks & Visible Symptoms:
                      </h4>
                      <ul className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs sm:text-sm text-emerald-900">
                        {symptoms.map((sym, index) => (
                          <li key={index} className="flex items-start">
                            <span className="text-emerald-500 mr-2 font-bold">•</span>
                            <span>{sym}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    {/* Environmental Causes */}
                    <div className="bg-amber-50/60 rounded-2xl p-5 border border-amber-100">
                      <h4 className="font-bold text-amber-950 text-sm mb-3 flex items-center">
                        <FaSun className="mr-2 text-amber-600" />
                        Favorable Conditions & Disease Causes:
                      </h4>
                      <ul className="space-y-1.5 text-xs sm:text-sm text-amber-900">
                        {causes.map((cause, index) => (
                          <li key={index} className="flex items-start">
                            <span className="text-amber-500 mr-2 font-bold">•</span>
                            <span>{cause}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </motion.div>
                )}

                {/* Tab 2: Treatment & Remedies */}
                {activeTab === 'treatment' && (
                  <motion.div
                    initial={{ opacity: 0, y: 6 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="space-y-6"
                  >
                    {/* Immediate Actions */}
                    <div className="bg-rose-50 rounded-2xl p-5 border border-rose-100">
                      <h4 className="font-bold text-rose-950 text-sm mb-3 flex items-center">
                        <FaExclamationTriangle className="mr-2 text-rose-600" />
                        Immediate Action Steps:
                      </h4>
                      <ol className="space-y-2 text-xs sm:text-sm text-rose-900 list-decimal list-inside">
                        {immediateActions.map((act, index) => (
                          <li key={index} className="leading-relaxed">
                            {act}
                          </li>
                        ))}
                      </ol>
                    </div>

                    {/* Organic Solutions */}
                    <div className="bg-emerald-50 rounded-2xl p-5 border border-emerald-100">
                      <h4 className="font-bold text-emerald-950 text-sm mb-3 flex items-center">
                        <FaSeedling className="mr-2 text-emerald-600" />
                        Organic & Biological Remedies:
                      </h4>
                      <ul className="space-y-2 text-xs sm:text-sm text-emerald-900">
                        {organicTreatments.map((org, index) => (
                          <li key={index} className="flex items-start">
                            <span className="text-emerald-500 mr-2 font-bold">✔</span>
                            <span>{org}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    {/* Chemical Options */}
                    {!isHealthy && (
                      <div className="bg-blue-50 rounded-2xl p-5 border border-blue-100">
                        <h4 className="font-bold text-blue-950 text-sm mb-3 flex items-center">
                          <FaVial className="mr-2 text-blue-600" />
                          Recommended Chemical Treatments (When Necessary):
                        </h4>
                        <ul className="space-y-2 text-xs sm:text-sm text-blue-900">
                          {chemicalTreatments.map((chem, index) => (
                            <li key={index} className="flex items-start">
                              <span className="text-blue-500 mr-2 font-bold">✔</span>
                              <span>{chem}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </motion.div>
                )}

                {/* Tab 3: Prevention & Cultivation */}
                {activeTab === 'prevention' && (
                  <motion.div
                    initial={{ opacity: 0, y: 6 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="space-y-6"
                  >
                    <div className="bg-emerald-50 rounded-2xl p-5 border border-emerald-100">
                      <h4 className="font-bold text-emerald-950 text-sm mb-3 flex items-center">
                        <FaShieldAlt className="mr-2 text-emerald-600" />
                        Preventive Cultural Practices:
                      </h4>
                      <ul className="space-y-2 text-xs sm:text-sm text-emerald-900">
                        {preventionTips.map((tip, index) => (
                          <li key={index} className="flex items-start">
                            <span className="text-emerald-500 mr-2 font-bold">✔</span>
                            <span>{tip}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div className="bg-slate-50 rounded-2xl p-5 border border-slate-200">
                      <h4 className="font-bold text-slate-900 text-sm mb-3 flex items-center">
                        <FaTint className="mr-2 text-blue-500" />
                        Irrigation & Fertilizer Care:
                      </h4>
                      <ul className="space-y-2 text-xs sm:text-sm text-slate-700">
                        {fertilizerCare.map((f, index) => (
                          <li key={index} className="flex items-start">
                            <span className="text-emerald-500 mr-2 font-bold">✔</span>
                            <span>{f}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </motion.div>
                )}

                {/* Bottom Action buttons */}
                <div className="mt-8 pt-6 border-t border-gray-100 flex flex-wrap gap-4">
                  <Link
                    to="/remedies"
                    state={{ ...prediction, preview }}
                    className="flex-1 min-w-[160px] px-6 py-3 bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-xl font-semibold shadow hover:from-green-700 hover:to-emerald-700 transition-all text-center text-sm"
                  >
                    View All Remedies
                  </Link>

                  <Link
                    to="/detection"
                    className="flex-1 min-w-[160px] px-6 py-3 border-2 border-green-600 text-green-700 rounded-xl font-semibold hover:bg-green-50 transition-all text-center text-sm"
                  >
                    Test Another Leaf
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Model Comparison Line Graph Section */}
        <motion.div
          id="model-comparison-section"
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-3xl shadow-xl border border-gray-100 overflow-hidden mb-8"
        >
          {/* Section Header */}
          <div className="bg-gradient-to-r from-slate-900 via-slate-800 to-indigo-950 p-6 md:p-8 text-white">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div>
                <div className="flex items-center space-x-2 text-indigo-300 text-xs font-bold uppercase tracking-wider mb-1">
                  <FaChartLine className="text-sm" />
                  <span>Dual Architecture Analytics</span>
                </div>
                <h2 className="text-2xl md:text-3xl font-extrabold tracking-tight">
                  CNN vs VGG-19 Model Confidence Line Graph
                </h2>
                <p className="text-slate-300 text-xs sm:text-sm mt-1">
                  Compare diagnostic certainty score differences between Primary VGG-19 (97.3%) and Custom CNN (85.3%).
                </p>
              </div>

              {/* View Mode Toggle */}
              <div className="flex items-center bg-white/10 backdrop-blur-md p-1.5 rounded-2xl border border-white/20 self-start md:self-auto">
                <button
                  type="button"
                  onClick={() => setActiveGraphMode('prediction')}
                  className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all ${
                    activeGraphMode === 'prediction'
                      ? 'bg-emerald-500 text-white shadow-md'
                      : 'text-slate-200 hover:text-white'
                  }`}
                >
                  This Leaf Image
                </button>
                <button
                  type="button"
                  onClick={() => setActiveGraphMode('benchmark')}
                  className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all ${
                    activeGraphMode === 'benchmark'
                      ? 'bg-blue-600 text-white shadow-md'
                      : 'text-slate-200 hover:text-white'
                  }`}
                >
                  14-Crops Benchmark
                </button>
              </div>
            </div>
          </div>

          <div className="p-6 md:p-8">
            {activeGraphMode === 'prediction' ? (
              <div className="space-y-6">
                {/* Dynamically generated per-image line graph */}
                <div className="bg-slate-50 rounded-2xl p-4 border border-gray-200 shadow-inner overflow-hidden">
                  <div className="flex flex-wrap items-center justify-between gap-2 mb-3 text-xs text-gray-500">
                    <span className="font-semibold text-gray-700 flex items-center gap-1.5">
                      <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block"></span> VGG-19 Confidence
                      <span className="w-2.5 h-2.5 rounded-full bg-blue-600 inline-block ml-3"></span> CNN Confidence
                    </span>
                    <a
                      href="http://127.0.0.1:8002/predict/comparison/latest-line-graph.png"
                      download="leaf_diagnosis_cnn_vs_vgg19.png"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-indigo-600 hover:text-indigo-800 font-semibold underline flex items-center gap-1"
                    >
                      <FaDownload className="text-xs" />
                      <span>Download Graph PNG</span>
                    </a>
                  </div>

                  {comparisonGraphBase64 ? (
                    <img
                      src={comparisonGraphBase64}
                      alt="CNN vs VGG-19 Confidence Comparison Line Graph for this leaf"
                      className="w-full h-auto rounded-xl shadow-sm"
                    />
                  ) : (
                    <img
                      src="http://127.0.0.1:8002/predict/comparison/latest-line-graph.png"
                      alt="CNN vs VGG-19 Confidence Comparison Line Graph"
                      className="w-full h-auto rounded-xl shadow-sm"
                    />
                  )}
                </div>

                {/* Candidate comparison table */}
                {candidatesComparison.length > 0 && (
                  <div>
                    <h3 className="font-bold text-gray-900 text-sm mb-3 flex items-center gap-2">
                      <FaNotesMedical className="text-emerald-600" />
                      <span>Top Candidate Conditions Confidence Differential:</span>
                    </h3>
                    <div className="overflow-x-auto rounded-2xl border border-gray-200 shadow-sm">
                      <table className="w-full text-left text-xs sm:text-sm">
                        <thead className="bg-slate-100 text-gray-600 uppercase text-[11px] font-bold">
                          <tr>
                            <th className="py-3 px-4">Candidate Condition</th>
                            <th className="py-3 px-4 text-emerald-700">VGG-19 Score</th>
                            <th className="py-3 px-4 text-blue-700">CNN Score</th>
                            <th className="py-3 px-4">Confidence Difference (Δ)</th>
                            <th className="py-3 px-4 text-center">Leading Model</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-100">
                          {candidatesComparison.map((cand, idx) => {
                            const isVggLead = cand.vgg19_confidence >= cand.cnn_confidence;
                            return (
                              <tr key={idx} className="hover:bg-slate-50 transition">
                                <td className="py-3 px-4 font-semibold text-gray-900">
                                  {cand.label || cand.disease}
                                </td>
                                <td className="py-3 px-4 font-bold text-emerald-600">
                                  {cand.vgg19_confidence.toFixed(1)}%
                                </td>
                                <td className="py-3 px-4 font-bold text-blue-600">
                                  {cand.cnn_confidence.toFixed(1)}%
                                </td>
                                <td className="py-3 px-4 font-medium text-gray-700">
                                  {cand.difference > 0 ? (
                                    <span className="text-emerald-700 font-semibold">
                                      +{cand.difference.toFixed(1)}% (VGG-19 lead)
                                    </span>
                                  ) : cand.difference < 0 ? (
                                    <span className="text-blue-700 font-semibold">
                                      {cand.difference.toFixed(1)}% (CNN lead)
                                    </span>
                                  ) : (
                                    <span className="text-gray-500">0.0% (Tied)</span>
                                  )}
                                </td>
                                <td className="py-3 px-4 text-center">
                                  <span
                                    className={`inline-block px-2.5 py-1 rounded-full text-xs font-bold ${
                                      isVggLead
                                        ? 'bg-emerald-100 text-emerald-800'
                                        : 'bg-blue-100 text-blue-800'
                                    }`}
                                  >
                                    {isVggLead ? 'VGG-19' : 'CNN'}
                                  </span>
                                </td>
                              </tr>
                            );
                          })}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}
              </div>
            ) : (
              /* Benchmark Mode */
              <div className="space-y-6">
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  <div className="bg-emerald-50 rounded-2xl p-4 border border-emerald-200">
                    <div className="text-xs font-bold text-emerald-800 uppercase">VGG-19 Accuracy</div>
                    <div className="text-2xl font-black text-emerald-700 mt-1">97.32%</div>
                    <div className="text-xs text-emerald-600 mt-0.5">+12.03% Lead over CNN</div>
                  </div>
                  <div className="bg-blue-50 rounded-2xl p-4 border border-blue-200">
                    <div className="text-xs font-bold text-blue-800 uppercase">CNN Accuracy</div>
                    <div className="text-2xl font-black text-blue-700 mt-1">85.29%</div>
                    <div className="text-xs text-blue-600 mt-0.5">87.85% Mean Confidence</div>
                  </div>
                  <div className="bg-purple-50 rounded-2xl p-4 border border-purple-200">
                    <div className="text-xs font-bold text-purple-800 uppercase">Validation Dataset</div>
                    <div className="text-2xl font-black text-purple-700 mt-1">10,861</div>
                    <div className="text-xs text-purple-600 mt-0.5">Images across 38 Classes</div>
                  </div>
                </div>

                <div className="bg-slate-50 rounded-2xl p-4 border border-gray-200 shadow-inner overflow-hidden">
                  <img
                    src="http://127.0.0.1:8002/predict/comparison/line-graph.png?mode=combined"
                    alt="14-Crops Benchmark Line Graph"
                    className="w-full h-auto rounded-xl shadow-sm"
                  />
                </div>

                <div className="text-center">
                  <a
                    href="http://127.0.0.1:8002/predict/comparison/interactive-view"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center space-x-2 px-5 py-2.5 bg-slate-900 hover:bg-slate-800 text-white rounded-xl text-xs font-bold shadow-md transition"
                  >
                    <span>Open Fullscreen Benchmark Dashboard ↗</span>
                  </a>
                </div>
              </div>
            )}
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default PredictionResult;
