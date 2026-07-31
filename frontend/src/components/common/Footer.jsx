import React from 'react';
import { FaLeaf, FaFacebook, FaTwitter, FaInstagram, FaYoutube } from 'react-icons/fa';

const Footer = () => {
  return (
    <footer className="bg-dark-900 text-white py-12">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <FaLeaf className="text-3xl text-green-400" />
              <span className="text-2xl font-bold">DeepLeaf</span>
            </div>
            <p className="text-gray-400 text-sm">
              AI-Powered Plant Disease Detection and Diagnosis. Smart technology for healthier crops and better tomorrow.
            </p>
          </div>

          <div>
            <h3 className="font-semibold text-lg mb-4">Quick Links</h3>
            <ul className="space-y-2 text-gray-400">
              <li><a href="/" className="hover:text-green-400 transition-colors">Home</a></li>
              <li><a href="/about" className="hover:text-green-400 transition-colors">About</a></li>
              <li><a href="/detection" className="hover:text-green-400 transition-colors">Detection</a></li>
              <li><a href="/remedies" className="hover:text-green-400 transition-colors">Remedies</a></li>
            </ul>
          </div>

          <div>
            <h3 className="font-semibold text-lg mb-4">Support</h3>
            <ul className="space-y-2 text-gray-400">
              <li><a href="#" className="hover:text-green-400 transition-colors">Help Center</a></li>
              <li><a href="#" className="hover:text-green-400 transition-colors">Privacy Policy</a></li>
              <li><a href="#" className="hover:text-green-400 transition-colors">Terms of Service</a></li>
              <li><a href="#" className="hover:text-green-400 transition-colors">Contact Us</a></li>
            </ul>
          </div>

          <div>
            <h3 className="font-semibold text-lg mb-4">Follow Us</h3>
            <div className="flex space-x-4">
              <a href="#" className="w-10 h-10 bg-dark-800 rounded-full flex items-center justify-center hover:bg-green-600 transition-colors">
                <FaFacebook />
              </a>
              <a href="#" className="w-10 h-10 bg-dark-800 rounded-full flex items-center justify-center hover:bg-green-600 transition-colors">
                <FaTwitter />
              </a>
              <a href="#" className="w-10 h-10 bg-dark-800 rounded-full flex items-center justify-center hover:bg-green-600 transition-colors">
                <FaInstagram />
              </a>
              <a href="#" className="w-10 h-10 bg-dark-800 rounded-full flex items-center justify-center hover:bg-green-600 transition-colors">
                <FaYoutube />
              </a>
            </div>
            <p className="mt-4 text-gray-400 text-sm">
              📧 support@deepleaf.com
              <br />
              📞 +91 9876543210
            </p>
          </div>
        </div>

        <div className="border-t border-dark-700 mt-8 pt-8 text-center text-gray-400 text-sm">
          © 2026 DeepLeaf. All rights reserved. Made with ❤️ for a greener world.
        </div>
      </div>
    </footer>
  );
};

export default Footer;