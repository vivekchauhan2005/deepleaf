import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaUpload, FaCamera, FaTrash, FaLeaf, FaChartLine, FaCheckCircle, FaExclamationTriangle } from 'react-icons/fa';
import toast from 'react-hot-toast';
import { motion } from 'framer-motion';

const Detection = () => {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  const stats = [
    { icon: FaCheckCircle, value: '16', label: 'Healthy', color: 'text-green-500' },
    { icon: FaExclamationTriangle, value: '8', label: 'Diseased', color: 'text-red-500' },
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
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImage(file);
        setPreview(reader.result);
      };
      reader.readAsDataURL(file);
    } else {
      toast.error('Please upload an image file');
    }
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
      toast.error('Please upload an image');
      return;
    }
    setLoading(true);
    try {
      await new Promise(resolve => setTimeout(resolve, 2000));
      toast.success('Analysis complete! 🌿');
      navigate('/result');
    } catch (error) {
      toast.error('Analysis failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen py-12 bg-gradient-to-br from-green-50 via-emerald-50 to-white">
      <div className="container mx-auto px-4">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="max-w-6xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2">
              <div className="bg-white rounded-3xl shadow-lg p-8">
                <h2 className="text-2xl font-bold text-dark-900 mb-6">Upload Plant Leaf Image</h2>

                <form onSubmit={handleSubmit}>
                  <div
                    className={`relative border-2 border-dashed rounded-2xl p-12 text-center transition-all ${
                      dragActive ? 'border-green-500 bg-green-50' : 'border-gray-300 hover:border-green-400'
                    }`}
                    onDragEnter={handleDrag}
                    onDragLeave={handleDrag}
                    onDragOver={handleDrag}
                    onDrop={handleDrop}
                  >
                    {preview ? (
                      <div className="relative">
                        <img src={preview} alt="Preview" className="max-h-64 mx-auto rounded-xl" />
                        <button
                          type="button"
                          onClick={handleRemoveImage}
                          className="absolute top-2 right-2 p-2 bg-red-500 text-white rounded-full hover:bg-red-600 transition-colors"
                        >
                          <FaTrash />
                        </button>
                      </div>
                    ) : (
                      <div>
                        <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                          <FaUpload className="text-3xl text-green-500" />
                        </div>
                        <p className="text-gray-600 mb-2">Drag & drop your image here, or</p>
                        <button
                          type="button"
                          onClick={() => fileInputRef.current.click()}
                          className="px-6 py-3 bg-green-500 text-white rounded-xl font-semibold hover:bg-green-600 transition-all"
                        >
                          Browse Files
                        </button>
                        <input
                          ref={fileInputRef}
                          type="file"
                          accept="image/*"
                          onChange={handleFileChange}
                          className="hidden"
                        />
                        <p className="text-gray-400 text-sm mt-4">Supports: JPG, PNG, WEBP</p>
                      </div>
                    )}
                  </div>

                  <div className="flex gap-4 mt-6">
                    <button
                      type="submit"
                      disabled={loading || !image}
                      className="flex-1 py-3 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-xl font-semibold hover:from-green-600 hover:to-green-700 transition-all hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {loading ? (
                        <span className="flex items-center justify-center">
                          <svg className="animate-spin h-5 w-5 mr-3 text-white" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                          </svg>
                          Analyzing...
                        </span>
                      ) : (
                        'Detect Disease'
                      )}
                    </button>
                    <button
                      type="button"
                      onClick={() => {
                        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
                          toast.info('Camera feature coming soon! 📸');
                        } else {
                          toast.error('Camera not supported');
                        }
                      }}
                      className="px-6 py-3 border-2 border-green-500 text-green-600 rounded-xl font-semibold hover:bg-green-50 transition-all flex items-center gap-2"
                    >
                      <FaCamera />
                      <span>Capture</span>
                    </button>
                  </div>
                </form>
              </div>
            </div>

            <div className="space-y-6">
              <div className="bg-white rounded-2xl shadow-lg p-6">
                <h3 className="text-lg font-bold text-dark-900 mb-4">Health Overview</h3>
                <div className="flex justify-between mb-4">
                  {stats.map((stat, index) => (
                    <div key={index} className="text-center">
                      <div className={`text-2xl font-bold ${stat.color}`}>{stat.value}</div>
                      <div className="text-sm text-gray-500">{stat.label}</div>
                    </div>
                  ))}
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div className="bg-green-500 h-3 rounded-full" style={{ width: '65%' }}></div>
                </div>
                <div className="text-right text-sm text-gray-500 mt-2">65% Health</div>
              </div>

              <div className="bg-gradient-to-br from-green-500 to-emerald-600 rounded-2xl p-6 text-white">
                <div className="flex items-center space-x-3 mb-3">
                  <FaLeaf className="text-3xl" />
                  <h3 className="text-lg font-bold">Quick Tips</h3>
                </div>
                <ul className="space-y-2 text-sm text-green-50">
                  <li>• Upload clear leaf images</li>
                  <li>• Use good lighting</li>
                  <li>• Get accurate results</li>
                  <li>• Follow expert remedies</li>
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