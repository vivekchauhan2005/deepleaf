
import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  FaUpload,
  FaCamera,
  FaTrash,
  FaLeaf,
  FaCheckCircle,
  FaExclamationTriangle,
} from 'react-icons/fa';
import toast from 'react-hot-toast';
import { motion } from 'framer-motion';
import { predictDisease } from '../../services/api';

const API_URL = 'http://127.0.0.1:8002';

const Detection = () => {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const [cameraOpen, setCameraOpen] = useState(false);
  const [cameraLoading, setCameraLoading] = useState(false);

  const [healthStats, setHealthStats] = useState(null);
  const [statsLoading, setStatsLoading] = useState(true);
  const [statsError, setStatsError] = useState('');

  const fileInputRef = useRef(null);
  const videoRef = useRef(null);
  const streamRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    const controller = new AbortController();

    const fetchHealthStats = async () => {
      setStatsLoading(true);
      setStatsError('');

      try {
        const token = localStorage.getItem('token');

        if (!token) {
          throw new Error('Please log in to view your health overview.');
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
              : 'Unable to load health statistics.'
          );
        }

        if (data.success !== true) {
          throw new Error('Invalid health statistics response.');
        }

        setHealthStats({
          healthy: Number(data.healthy_count) || 0,
          diseased: Number(data.diseased_count) || 0,
          total: Number(data.total_predictions) || 0,
        });
      } catch (error) {
        if (error.name !== 'AbortError') {
          setStatsError(error.message || 'Unable to load health statistics.');
        }
      } finally {
        if (!controller.signal.aborted) {
          setStatsLoading(false);
        }
      }
    };

    fetchHealthStats();

    return () => controller.abort();
  }, []);

  const stats = [
    {
      icon: FaCheckCircle,
      value: healthStats?.healthy ?? '—',
      label: 'Healthy',
      color: 'text-green-500',
    },
    {
      icon: FaExclamationTriangle,
      value: healthStats?.diseased ?? '—',
      label: 'Diseased',
      color: 'text-red-500',
    },
  ];

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();

    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const files = e.dataTransfer.files;

    if (files && files[0]) {
      handleFile(files[0]);
    }
  };

  const handleFile = (file) => {
    if (!file) return;

    const allowedTypes = [
      'image/jpeg',
      'image/png',
      'image/webp',
    ];

    if (!allowedTypes.includes(file.type)) {
      toast.error('Only JPG, PNG and WEBP images are allowed.');
      return;
    }

    setImage(file);

    // Keep the preview as a data URL so it remains available after navigation.
    // Object URLs can become invalid when the Detection component cleans up.
    const reader = new FileReader();
    reader.onload = () => {
      if (typeof reader.result === 'string') {
        setPreview(reader.result);
      } else {
        setPreview(null);
        toast.error('Unable to preview this image. Please select it again.');
      }
    };
    reader.onerror = () => {
      setPreview(null);
      toast.error('Unable to preview this image. Please select it again.');
    };
    reader.readAsDataURL(file);
  };

  const handleFileChange = (e) => {
    const files = e.target.files;

    if (files && files[0]) {
      handleFile(files[0]);
    }
  };

  const handleRemoveImage = () => {
    setImage(null);
    setPreview(null);

    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!image) {
      toast.error('Please upload an image.');
      return;
    }

    if (!preview) {
      toast.error('The image preview is still loading. Please wait a moment and try again.');
      return;
    }

    setLoading(true);

    try {
      const data = await predictDisease(image);

      if (!data || !data.success) {
        throw new Error('Prediction failed.');
      }

      toast.success('Analysis complete! 🌿');

      navigate('/result', {
        state: {
          ...data,
          is_leaf: data.is_leaf,
          leaf_confidence: data.leaf_confidence,
          disease: data.disease,
          formatted_disease: data.formatted_disease,
          plant_name: data.plant_name,
          confidence: data.confidence,
          severity: data.severity,
          status: data.status,
          message: data.message,
          filename: data.filename,
          preview,
          dataset_evidence: data.dataset_evidence,
          comparison: data.comparison,
          top_predictions: data.top_predictions,
          details: data.details,
          models_agree: data.models_agree,
          photography_tips: data.photography_tips,
          record_id: data.record_id,
          history_saved: data.history_saved,
        },
      });
    } catch (error) {
      console.error('Prediction error:', error);
      toast.error(error.message || 'Analysis failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }

    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }

    setCameraOpen(false);
    setCameraLoading(false);
  };

  const handleCapture = async () => {
    if (cameraOpen) return;

    if (!navigator.mediaDevices?.getUserMedia) {
      toast.error('Camera access requires HTTPS or localhost.');
      return;
    }

    try {
      setCameraLoading(true);
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: { ideal: 'environment' } },
        audio: false,
      });

      streamRef.current = stream;
      setCameraOpen(true);
    } catch (error) {
      console.error('Camera error:', error);

      if (error.name === 'NotAllowedError' || error.name === 'PermissionDeniedError') {
        toast.error('Camera permission was denied. Allow camera access and try again.');
      } else if (error.name === 'NotFoundError' || error.name === 'DevicesNotFoundError') {
        toast.error('No camera was found on this device.');
      } else {
        toast.error('Unable to open the camera. Please check your device settings.');
      }

      setCameraLoading(false);
    }
  };

  useEffect(() => {
    if (!cameraOpen || !videoRef.current || !streamRef.current) return;

    const video = videoRef.current;
    video.srcObject = streamRef.current;

    video.play()
      .then(() => setCameraLoading(false))
      .catch((error) => {
        console.error('Camera preview error:', error);
        toast.error('Unable to start the camera preview.');
        stopCamera();
      });
  }, [cameraOpen]);

  useEffect(() => {
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
      }
    };
  }, []);

  const capturePhoto = () => {
    const video = videoRef.current;

    if (!video || !video.videoWidth || !video.videoHeight) {
      toast.error('Camera is not ready. Please wait a moment.');
      return;
    }

    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext('2d');

    if (!context) {
      toast.error('Unable to capture the image.');
      return;
    }

    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    canvas.toBlob((blob) => {
      if (!blob) {
        toast.error('Unable to create the captured image.');
        return;
      }

      const file = new File([blob], `leaf-capture-${Date.now()}.jpg`, {
        type: 'image/jpeg',
      });
      stopCamera();
      handleFile(file);
      toast.success('Photo captured. Ready to analyze.');
    }, 'image/jpeg', 0.92);
  };

  const totalClassified =
    (healthStats?.healthy ?? 0) + (healthStats?.diseased ?? 0);

  const healthyPercentage =
    totalClassified > 0
      ? Math.round(((healthStats?.healthy ?? 0) / totalClassified) * 100)
      : 0;

  return (
    <div className="min-h-screen py-12 bg-gradient-to-br from-green-50 via-emerald-50 to-white">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="max-w-6xl mx-auto"
        >
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2">
              <div className="bg-white rounded-3xl shadow-lg p-8">
                <h2 className="text-2xl font-bold text-dark-900 mb-6">
                  Upload Plant Leaf Image
                </h2>

                <form onSubmit={handleSubmit}>
                  <div
                    className={`relative border-2 border-dashed rounded-2xl p-12 text-center transition-all ${
                      dragActive
                        ? 'border-green-500 bg-green-50'
                        : 'border-gray-300 hover:border-green-400'
                    }`}
                    onDragEnter={handleDrag}
                    onDragLeave={handleDrag}
                    onDragOver={handleDrag}
                    onDrop={handleDrop}
                  >
                    {preview ? (
                      <div className="relative">
                        <img
                          src={preview}
                          alt="Leaf Preview"
                          className="max-h-64 mx-auto rounded-xl object-contain"
                        />

                        <button
                          type="button"
                          onClick={handleRemoveImage}
                          className="absolute top-2 right-2 p-2 bg-red-500 text-white rounded-full hover:bg-red-600 transition-colors"
                          aria-label="Remove selected image"
                        >
                          <FaTrash />
                        </button>

                        <p className="text-sm text-gray-500 mt-4 break-all">
                          {image?.name}
                        </p>
                      </div>
                    ) : (
                      <div>
                        <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                          <FaUpload className="text-3xl text-green-500" />
                        </div>

                        <p className="text-gray-600 mb-2">
                          Drag & drop your image here, or
                        </p>

                        <button
                          type="button"
                          onClick={() => fileInputRef.current?.click()}
                          className="px-6 py-3 bg-green-500 text-white rounded-xl font-semibold hover:bg-green-600 transition-all"
                        >
                          Browse Files
                        </button>

                        <input
                          ref={fileInputRef}
                          type="file"
                          accept="image/jpeg,image/png,image/webp"
                          onChange={handleFileChange}
                          className="hidden"
                        />

                        <p className="text-gray-400 text-sm mt-4">
                          Supports: JPG, PNG, WEBP
                        </p>
                      </div>
                    )}
                  </div>

                  {cameraOpen && (
                    <div className="mt-4 rounded-xl border border-green-200 bg-gray-50 p-4">
                      <p className="mb-3 text-sm font-semibold text-gray-700">Live Camera Preview</p>
                      <video
                        ref={videoRef}
                        autoPlay
                        playsInline
                        muted
                        className="mx-auto max-h-80 w-full rounded-lg bg-black object-contain"
                        aria-label="Live camera preview"
                      />
                      {cameraLoading && (
                        <p className="mt-2 text-center text-sm text-gray-500">Starting camera...</p>
                      )}
                      <div className="mt-3 flex justify-center gap-3">
                        <button
                          type="button"
                          onClick={capturePhoto}
                          disabled={cameraLoading}
                          className="rounded-lg bg-green-600 px-5 py-2.5 font-semibold text-white transition hover:bg-green-700 disabled:opacity-50"
                        >
                          Capture Photo
                        </button>
                        <button
                          type="button"
                          onClick={stopCamera}
                          className="rounded-lg border border-gray-300 px-5 py-2.5 font-semibold text-gray-700 hover:bg-gray-100"
                        >
                          Cancel
                        </button>
                      </div>
                    </div>
                  )}

                  <div className="flex gap-4 mt-6">
                    <button
                      type="submit"
                      disabled={loading || !image}
                      className="flex-1 py-3 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-xl font-semibold hover:from-green-600 hover:to-green-700 transition-all hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {loading ? (
                        <span className="flex items-center justify-center">
                          <svg
                            className="animate-spin h-5 w-5 mr-3 text-white"
                            viewBox="0 0 24 24"
                          >
                            <circle
                              className="opacity-25"
                              cx="12"
                              cy="12"
                              r="10"
                              stroke="currentColor"
                              strokeWidth="4"
                              fill="none"
                            />
                            <path
                              className="opacity-75"
                              fill="currentColor"
                              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                            />
                          </svg>
                          Analyzing...
                        </span>
                      ) : (
                        'Detect Disease'
                      )}
                    </button>

                    <button
                      type="button"
                      onClick={handleCapture}
                      disabled={cameraLoading || cameraOpen}
                      className="px-6 py-3 border-2 border-green-500 text-green-600 rounded-xl font-semibold hover:bg-green-50 transition-all flex items-center gap-2"
                    >
                      <FaCamera />
                      <span>{cameraLoading ? 'Opening Camera...' : cameraOpen ? 'Camera Open' : 'Capture'}</span>
                    </button>
                  </div>
                </form>
              </div>
            </div>

            <div className="space-y-6">
              <div className="bg-white rounded-2xl shadow-lg p-6">
                <h3 className="text-lg font-bold text-dark-900 mb-4">
                  Health Overview
                </h3>

                {statsLoading ? (
                  <p className="text-sm text-gray-500 py-4">
                    Loading live health statistics...
                  </p>
                ) : statsError ? (
                  <div className="py-3" role="alert">
                    <p className="text-sm text-red-600">{statsError}</p>
                    <button
                      type="button"
                      onClick={() => window.location.reload()}
                      className="mt-3 text-sm text-green-600 font-semibold hover:underline"
                    >
                      Try Again
                    </button>
                  </div>
                ) : (
                  <>
                    <div className="flex justify-between mb-4">
                      {stats.map((stat) => {
                        const Icon = stat.icon;

                        return (
                          <div key={stat.label} className="text-center">
                            <Icon className={`text-xl mx-auto mb-1 ${stat.color}`} />
                            <div className={`text-2xl font-bold ${stat.color}`}>
                              {stat.value}
                            </div>
                            <div className="text-sm text-gray-500">
                              {stat.label}
                            </div>
                          </div>
                        );
                      })}
                    </div>

                    <p className="text-xs text-gray-400 mt-4 text-center">
                      {healthStats.total} total prediction attempts ·{' '}
                      {totalClassified} classified leaf results
                    </p>
                  </>
                )}
              </div>

              <div className="bg-gradient-to-br from-green-500 to-emerald-600 rounded-2xl p-6 text-white">
                <div className="flex items-center space-x-3 mb-3">
                  <FaLeaf className="text-3xl" />
                  <h3 className="text-lg font-bold">Quick Tips</h3>
                </div>

                <ul className="space-y-2 text-sm text-green-50">
                  <li>• Upload clear leaf images</li>
                  <li>• Use good lighting</li>
                  <li>• Keep the leaf in focus</li>
                  <li>• Review the result before acting</li>
                </ul>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Detection;
