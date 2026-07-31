import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AuthProvider } from './context/AuthContext';

// Auth Pages
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import ForgotPassword from './components/auth/ForgotPassword';
import OTPVerification from './components/auth/OTPVerification';
import ResetPassword from './components/auth/ResetPassword';

// Main Pages
import Home from './components/pages/Home';
import Dashboard from './components/user/Dashboard';
import Detection from './components/user/Detection';
import PredictionResult from './components/user/PredictionResult';
import History from './components/user/History';
import Remedies from './components/user/Remedies';
import Profile from './components/user/Profile';
import Settings from './components/user/Settings';
import About from './components/pages/About';

// Layout
import Navbar from './components/common/Navbar';
import Footer from './components/common/Footer';

const MainLayout = ({ children }) => (
  <div className="min-h-screen flex flex-col">
    <Navbar />
    <main className="flex-grow">{children}</main>
    <Footer />
  </div>
);

function App() {
  return (
    <AuthProvider>
      <Router>
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: '#ffffff',
              color: '#1e293b',
              borderRadius: '12px',
              boxShadow: '0 10px 40px rgba(0,0,0,0.1)',
              padding: '16px',
            },
            success: {
              iconTheme: { primary: '#22c55e', secondary: '#ffffff' },
            },
            error: {
              iconTheme: { primary: '#ef4444', secondary: '#ffffff' },
            },
          }}
        />

        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<MainLayout><Home /></MainLayout>} />
          <Route path="/about" element={<MainLayout><About /></MainLayout>} />

          {/* Auth Routes (No Navbar/Footer) */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          <Route path="/verify-otp" element={<OTPVerification />} />
          <Route path="/reset-password" element={<ResetPassword />} />

          {/* Protected User Routes */}
          <Route path="/dashboard" element={<MainLayout><Dashboard /></MainLayout>} />
          <Route path="/detection" element={<MainLayout><Detection /></MainLayout>} />
          <Route path="/result" element={<MainLayout><PredictionResult /></MainLayout>} />
          <Route path="/history" element={<MainLayout><History /></MainLayout>} />
          <Route path="/remedies" element={<MainLayout><Remedies /></MainLayout>} />
          <Route path="/profile" element={<MainLayout><Profile /></MainLayout>} />
          <Route path="/settings" element={<MainLayout><Settings /></MainLayout>} />

          {/* 404 */}
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;