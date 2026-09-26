import React, { useState } from 'react';
import { FaSearch, FaFlask, FaSeedling, FaLeaf, FaCheckCircle, FaArrowRight } from 'react-icons/fa';
import { motion } from 'framer-motion';

const Remedies = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [category, setCategory] = useState('all');

  const remedies = [
    {
      id: 1,
      title: 'Neem Oil Spray',
      description: 'Natural fungicide that helps control fungus on plants.',
      category: 'chemical',
      icon: FaFlask,
      color: 'from-green-400 to-green-600',
    },
    {
      id: 2,
      title: 'Trichoderma',
      description: 'Beneficial fungus that protects plants roots from pathogens.',
      category: 'biological',
      icon: FaSeedling,
      color: 'from-blue-400 to-blue-600',
    },
    {
      id: 3,
      title: 'Baking Soda Solution',
      description: 'Mix baking soda with water and spray on affected areas.',
      category: 'chemical',
      icon: FaFlask,
      color: 'from-yellow-400 to-yellow-600',
    },
    {
      id: 4,
      title: 'Garlic Extract',
      description: 'Natural antifungal and antibacterial solution for plants.',
      category: 'biological',
      icon: FaLeaf,
      color: 'from-purple-400 to-purple-600',
    },
    {
      id: 5,
      title: 'Copper Fungicide',
      description: 'Effective against fungal and bacterial diseases.',
      category: 'chemical',
      icon: FaFlask,
      color: 'from-red-400 to-red-600',
    },
    {
      id: 6,
      title: 'Compost Tea',
      description: 'Rich in beneficial microorganisms for plant health.',
      category: 'organic',
      icon: FaSeedling,
      color: 'from-brown-400 to-brown-600',
    },
  ];

  const categories = [
    { value: 'all', label: 'All Remedies' },
    { value: 'chemical', label: 'Chemical Remedies' },
    { value: 'biological', label: 'Biological' },
    { value: 'organic', label: 'Organic' },
  ];

  const filteredRemedies = remedies.filter(r => {
    const matchesSearch = r.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          r.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = category === 'all' || r.category === category;
    return matchesSearch && matchesCategory;
  });

  return (
    <div className="min-h-screen py-12 bg-gradient-to-br from-green-50 via-emerald-50 to-white">
      <div className="container mx-auto px-4">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h1 className="text-3xl md:text-4xl font-bold text-dark-900 mb-4">
              Plant Disease <span className="gradient-text">Remedies</span>
            </h1>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Discover effective solutions to protect your plants and ensure healthy growth
            </p>
          </div>

          <div className="flex flex-col md:flex-row gap-4 mb-8">
            <div className="flex-1 relative">
              <FaSearch className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
              <input
                type="text"
                placeholder="Search remedies..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-3 bg-white border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-500 shadow-lg"
              />
            </div>
            <div className="flex gap-3 overflow-x-auto pb-2">
              {categories.map((cat) => (
                <button
                  key={cat.value}
                  onClick={() => setCategory(cat.value)}
                  className={`px-6 py-2 rounded-xl font-semibold transition-all whitespace-nowrap ${
                    category === cat.value
                      ? 'bg-green-500 text-white shadow-lg'
                      : 'bg-white text-gray-600 hover:bg-green-50'
                  }`}
                >
                  {cat.label}
                </button>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredRemedies.map((remedy, index) => (
              <motion.div
                key={remedy.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="bg-white rounded-2xl shadow-lg overflow-hidden hover-card group"
              >
                <div className={`p-6 bg-gradient-to-r ${remedy.color} text-white`}>
                  <div className="flex items-center justify-between">
                    <remedy.icon className="text-3xl" />
                    <span className="px-3 py-1 bg-white/20 rounded-full text-xs font-semibold">
                      {remedy.category}
                    </span>
                  </div>
                  <h3 className="text-xl font-bold mt-4">{remedy.title}</h3>
                </div>
                <div className="p-6">
                  <p className="text-gray-600 mb-4">{remedy.description}</p>
                  <button className="text-green-600 font-semibold hover:text-green-700 flex items-center space-x-1 group-hover:translate-x-1 transition-all">
                    <span>Learn More</span>
                    <FaArrowRight className="text-sm" />
                  </button>
                </div>
              </motion.div>
            ))}
          </div>

          {filteredRemedies.length === 0 && (
            <div className="text-center py-12">
              <p className="text-gray-500">No remedies found matching your search</p>
            </div>
          )}
        </motion.div>
      </div>
    </div>
  );
};

export default Remedies;