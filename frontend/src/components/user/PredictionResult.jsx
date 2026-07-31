import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { FaLeaf, FaCheckCircle, FaExclamationTriangle, FaArrowLeft, FaDownload, FaShareAlt } from 'react-icons/fa';
import { motion } from 'framer-motion';

const PredictionResult = () => {
  const navigate = useNavigate();

  const result = {
    plant: 'Tomato',
    disease: 'Early Blight',
    confidence: 92.45,
    status: 'Diseased',
    description: 'Early Blight is a common disease that affects tomato leaves and fruits. It is caused by the fungus Alternaria solani.',
    symptoms: [
      'Dark brown spots on leaves',
      'Yellowing of leaves',
      'Spots on leaves and fruit',
      'Severe infection leads to leaf drop',
    ],
    remedies: [
      'Remove infected leaves immediately',
      'Apply copper-based fungicide spray',
      'Ensure proper air circulation',
      'Avoid overhead watering',
      'Use crop rotation techniques',
    ],
  };

  return (
    <div className="min-h-screen py-12 bg-gradient-to-br from-green-50 via-emerald-50 to-white">
      <div className="container mx-auto px-4">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="max-w-4xl mx-auto">
          <div className="flex items-center justify-between mb-6">
            <button onClick={() => navigate(-1)} className="flex items-center space-x-2 text-green-600 hover:text-green-700">
              <FaArrowLeft />
              <span>Back</span>
            </button>
            <div className="flex items-center space-x-3">
              <button className="p-2 text-gray-500 hover:text-green-600 transition-colors">
                <FaShareAlt />
              </button>
              <button className="p-2 text-gray-500 hover:text-green-600 transition-colors">
                <FaDownload />
              </button>
            </div>
          </div>

          <div className="bg-white rounded-3xl shadow-lg overflow-hidden">
            <div className="bg-gradient-to-r from-green-500 to-emerald-600 p-8 text-white">
              <div className="flex items-center justify-between">
                <div>
                  <h1 className="text-3xl font-bold">Prediction Result</h1>
                  <p className="text-green-100 mt-1">Analysis complete for your plant leaf</p>
                </div>
                <div className="text-center">
                  <div className="text-5xl font-bold">{result.confidence}%</div>
                  <div className="text-sm text-green-100">Confidence</div>
                </div>
              </div>
            </div>

            <div className="p-8">
              <div className="flex items-start gap-8">
                <div className="flex-1">
                  <div className="mb-6">
                    <div className="flex items-center space-x-4">
                      <div className={`px-4 py-2 rounded-xl font-semibold ${result.status === 'Diseased' ? 'bg-red-100 text-red-600' : 'bg-green-100 text-green-600'}`}>
                        {result.status === 'Diseased' ? <FaExclamationTriangle className="inline mr-2" /> : <FaCheckCircle className="inline mr-2" />}
                        {result.status}
                      </div>
                      <div className="text-sm text-gray-500">Detected: {result.disease}</div>
                    </div>
                    <div className="mt-2">
                      <span className="text-gray-600">Plant:</span>
                      <span className="font-semibold text-dark-900 ml-2">{result.plant}</span>
                    </div>
                  </div>

                  <div className="mb-6">
                    <h3 className="text-lg font-bold text-dark-900 mb-2">About the Disease</h3>
                    <p className="text-gray-600">{result.description}</p>
                  </div>

                  <div className="mb-6">
                    <h3 className="text-lg font-bold text-dark-900 mb-2">Symptoms</h3>
                    <ul className="grid grid-cols-1 md:grid-cols-2 gap-2">
                      {result.symptoms.map((symptom, index) => (
                        <li key={index} className="flex items-center space-x-2 text-gray-600">
                          <span className="w-1.5 h-1.5 bg-red-400 rounded-full"></span>
                          <span>{symptom}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div>
                    <h3 className="text-lg font-bold text-dark-900 mb-2">Recommended Remedies</h3>
                    <ul className="space-y-2">
                      {result.remedies.map((remedy, index) => (
                        <li key={index} className="flex items-center space-x-2 text-gray-600">
                          <span className="w-5 h-5 bg-green-100 rounded-full flex items-center justify-center text-green-600 text-xs font-bold">
                            {index + 1}
                          </span>
                          <span>{remedy}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div className="mt-8 flex gap-4">
                    <Link to="/remedies" className="flex-1 px-6 py-3 bg-green-500 text-white rounded-xl font-semibold hover:bg-green-600 transition-all text-center">
                      View All Remedies
                    </Link>
                    <Link to="/detection" className="flex-1 px-6 py-3 border-2 border-green-500 text-green-600 rounded-xl font-semibold hover:bg-green-50 transition-all text-center">
                      New Detection
                    </Link>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default PredictionResult;