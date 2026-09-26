import React from 'react';
import { FaLeaf, FaRocket, FaEye, FaHeart } from 'react-icons/fa';
import { motion } from 'framer-motion';

const About = () => {
  return (
    <div className="min-h-screen py-20">
      <div className="container mx-auto px-4">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="max-w-4xl mx-auto">
          <div className="text-center mb-12">
            <div className="flex items-center justify-center space-x-3 mb-4">
              <FaLeaf className="text-5xl text-green-500" />
            </div>
            <h1 className="text-4xl md:text-5xl font-bold gradient-text mb-4">About DeepLeaf</h1>
            <p className="text-xl text-gray-600">
              DeepLeaf is an AI-powered platform that helps farmers and plant enthusiasts detect plant diseases instantly and provides expert remedies and solutions.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8 mt-12">
            <motion.div initial={{ opacity: 0, x: -20 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }} className="bg-white p-8 rounded-2xl shadow-lg hover-card">
              <div className="w-16 h-16 bg-green-100 rounded-xl flex items-center justify-center mb-4">
                <FaRocket className="text-3xl text-green-600" />
              </div>
              <h3 className="text-2xl font-bold text-dark-900 mb-3">Our Mission</h3>
              <p className="text-gray-600">To protect crops and promote healthy farming using smart technology.</p>
            </motion.div>

            <motion.div initial={{ opacity: 0, x: 20 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }} className="bg-white p-8 rounded-2xl shadow-lg hover-card">
              <div className="w-16 h-16 bg-green-100 rounded-xl flex items-center justify-center mb-4">
                <FaEye className="text-3xl text-green-600" />
              </div>
              <h3 className="text-2xl font-bold text-dark-900 mb-3">Our Vision</h3>
              <p className="text-gray-600">A world where every plant is healthy and every farmer is empowered.</p>
            </motion.div>
          </div>

          <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="mt-12 bg-gradient-to-r from-green-50 to-emerald-50 p-8 rounded-2xl text-center">
            <FaHeart className="text-4xl text-green-500 mx-auto mb-4" />
            <h3 className="text-2xl font-bold text-dark-900 mb-2">Join Us in Making a Difference</h3>
            <p className="text-gray-600">Together, we can create a sustainable future for agriculture.</p>
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
};

export default About;