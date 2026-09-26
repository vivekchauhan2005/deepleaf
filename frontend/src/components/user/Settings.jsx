import React, { useState } from 'react';
import { FaMoon, FaSun, FaGlobe, FaBell, FaEnvelope, FaShieldAlt, FaPalette } from 'react-icons/fa';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';

const Settings = () => {
  const [settings, setSettings] = useState({
    darkMode: false,
    language: 'english',
    notifications: true,
    emailAlerts: true,
    twoFactor: false,
    theme: 'green',
  });

  const handleToggle = (key) => {
    setSettings({ ...settings, [key]: !settings[key] });
    toast.success(`${key} updated!`);
  };

  const handleLanguageChange = (e) => {
    setSettings({ ...settings, language: e.target.value });
    toast.success('Language updated!');
  };

  const settingGroups = [
    {
      title: 'Appearance',
      icon: FaPalette,
      settings: [
        { key: 'darkMode', label: 'Dark Mode', icon: settings.darkMode ? FaMoon : FaSun },
        { key: 'theme', label: 'Theme Color', type: 'select', options: ['Green', 'Blue', 'Purple', 'Dark'] },
      ],
    },
    {
      title: 'Preferences',
      icon: FaGlobe,
      settings: [
        { key: 'language', label: 'Language', type: 'select', options: ['English', 'Hindi', 'Kannada', 'Tamil'] },
      ],
    },
    {
      title: 'Notifications',
      icon: FaBell,
      settings: [
        { key: 'notifications', label: 'Push Notifications' },
        { key: 'emailAlerts', label: 'Email Alerts' },
      ],
    },
    {
      title: 'Security',
      icon: FaShieldAlt,
      settings: [
        { key: 'twoFactor', label: 'Two-Factor Authentication' },
      ],
    },
  ];

  return (
    <div className="min-h-screen py-12 bg-gradient-to-br from-green-50 via-emerald-50 to-white">
      <div className="container mx-auto px-4">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="max-w-3xl mx-auto">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-dark-900">Settings ⚙️</h1>
            <p className="text-gray-500 mt-1">Customize your DeepLeaf experience</p>
          </div>

          <div className="space-y-6">
            {settingGroups.map((group, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="bg-white rounded-2xl shadow-lg p-6"
              >
                <div className="flex items-center space-x-3 mb-4">
                  <div className="w-10 h-10 bg-green-100 rounded-xl flex items-center justify-center text-green-600">
                    <group.icon />
                  </div>
                  <h2 className="text-lg font-bold text-dark-900">{group.title}</h2>
                </div>

                <div className="space-y-4">
                  {group.settings.map((setting) => (
                    <div key={setting.key} className="flex items-center justify-between py-2">
                      <div className="flex items-center space-x-3">
                        {setting.icon && <setting.icon className="text-gray-400" />}
                        <span className="text-gray-700">{setting.label}</span>
                      </div>
                      {setting.type === 'select' ? (
                        <select
                          value={settings[setting.key]}
                          onChange={setting.key === 'language' ? handleLanguageChange : (e) => {
                            setSettings({ ...settings, [setting.key]: e.target.value });
                            toast.success('Updated!');
                          }}
                          className="px-4 py-2 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-500"
                        >
                          {setting.options.map((option) => (
                            <option key={option} value={option.toLowerCase()}>{option}</option>
                          ))}
                        </select>
                      ) : (
                        <button
                          onClick={() => handleToggle(setting.key)}
                          className={`w-12 h-6 rounded-full transition-all ${
                            settings[setting.key] ? 'bg-green-500' : 'bg-gray-300'
                          } relative`}
                        >
                          <div
                            className={`w-5 h-5 bg-white rounded-full absolute top-0.5 transition-all ${
                              settings[setting.key] ? 'left-6' : 'left-0.5'
                            }`}
                          />
                        </button>
                      )}
                    </div>
                  ))}
                </div>
              </motion.div>
            ))}

            <div className="bg-white rounded-2xl shadow-lg p-6 text-center">
              <p className="text-gray-500 text-sm">
                Version 1.0.0 • Made with ❤️ for farmers and plant enthusiasts
              </p>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Settings;