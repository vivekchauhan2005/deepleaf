import React, { useState } from 'react';
import { FaUser, FaEnvelope, FaPhone, FaLock, FaEdit, FaSave, FaTimes } from 'react-icons/fa';
import { useAuth } from '../../context/AuthContext';
import toast from 'react-hot-toast';
import { motion } from 'framer-motion';

const Profile = () => {
  const { user } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    fullName: user?.name || 'Vivek Chauhan',
    email: user?.email || 'vivek@example.com',
    phone: user?.phone || '+91 9876543210',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSave = () => {
    toast.success('Profile updated successfully! 🎉');
    setIsEditing(false);
  };

  return (
    <div className="min-h-screen py-12 bg-gradient-to-br from-green-50 via-emerald-50 to-white">
      <div className="container mx-auto px-4">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="max-w-3xl mx-auto">
          <div className="bg-white rounded-3xl shadow-lg overflow-hidden">
            <div className="bg-gradient-to-r from-green-500 to-emerald-600 p-8 text-white">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className="w-20 h-20 bg-white/20 rounded-full flex items-center justify-center text-3xl font-bold">
                    {formData.fullName.charAt(0)}
                  </div>
                  <div>
                    <h1 className="text-2xl font-bold">{formData.fullName}</h1>
                    <p className="text-green-100">Plant Disease Detection Expert</p>
                  </div>
                </div>
                <button
                  onClick={() => setIsEditing(!isEditing)}
                  className="px-4 py-2 bg-white/20 backdrop-blur-sm rounded-xl hover:bg-white/30 transition-colors flex items-center space-x-2"
                >
                  {isEditing ? <FaTimes /> : <FaEdit />}
                  <span>{isEditing ? 'Cancel' : 'Edit Profile'}</span>
                </button>
              </div>
            </div>

            <div className="p-8">
              <h2 className="text-xl font-bold text-dark-900 mb-6">Account Information</h2>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Full Name</label>
                  <div className="relative">
                    <FaUser className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
                    <input
                      type="text"
                      name="fullName"
                      value={formData.fullName}
                      onChange={handleChange}
                      disabled={!isEditing}
                      className={`w-full pl-10 pr-4 py-3 rounded-xl border ${
                        isEditing ? 'bg-white border-gray-200 focus:ring-2 focus:ring-green-500' : 'bg-gray-50 border-gray-100'
                      } focus:outline-none transition-all`}
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Email Address</label>
                  <div className="relative">
                    <FaEnvelope className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
                    <input
                      type="email"
                      name="email"
                      value={formData.email}
                      onChange={handleChange}
                      disabled={!isEditing}
                      className={`w-full pl-10 pr-4 py-3 rounded-xl border ${
                        isEditing ? 'bg-white border-gray-200 focus:ring-2 focus:ring-green-500' : 'bg-gray-50 border-gray-100'
                      } focus:outline-none transition-all`}
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Phone Number</label>
                  <div className="relative">
                    <FaPhone className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
                    <input
                      type="tel"
                      name="phone"
                      value={formData.phone}
                      onChange={handleChange}
                      disabled={!isEditing}
                      className={`w-full pl-10 pr-4 py-3 rounded-xl border ${
                        isEditing ? 'bg-white border-gray-200 focus:ring-2 focus:ring-green-500' : 'bg-gray-50 border-gray-100'
                      } focus:outline-none transition-all`}
                    />
                  </div>
                </div>

                {isEditing && (
                  <div className="flex gap-4 pt-4">
                    <button
                      onClick={handleSave}
                      className="flex-1 py-3 bg-green-500 text-white rounded-xl font-semibold hover:bg-green-600 transition-all flex items-center justify-center space-x-2"
                    >
                      <FaSave />
                      <span>Save Changes</span>
                    </button>
                    <button
                      onClick={() => setIsEditing(false)}
                      className="flex-1 py-3 border-2 border-gray-300 text-gray-600 rounded-xl font-semibold hover:bg-gray-50 transition-all"
                    >
                      Cancel
                    </button>
                  </div>
                )}

                <div className="border-t border-gray-200 pt-6 mt-6">
                  <button className="flex items-center space-x-2 text-red-500 hover:text-red-600 transition-colors">
                    <FaLock />
                    <span>Change Password</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Profile;