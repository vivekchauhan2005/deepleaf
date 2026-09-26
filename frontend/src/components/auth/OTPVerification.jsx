import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { FaLeaf, FaArrowLeft } from 'react-icons/fa';
import toast from 'react-hot-toast';

const OTPVerification = () => {
  const [otp, setOtp] = useState(['', '', '', '', '', '']);
  const [loading, setLoading] = useState(false);
  const [timer, setTimer] = useState(45);
  const navigate = useNavigate();

  useEffect(() => {
    const interval = setInterval(() => {
      setTimer((prev) => (prev > 0 ? prev - 1 : 0));
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  const handleChange = (index, value) => {
    if (value.length > 1) return;
    const newOtp = [...otp];
    newOtp[index] = value;
    setOtp(newOtp);
    if (value && index < 5) {
      document.getElementById(`otp-${index + 1}`).focus();
    }
  };

  const handleKeyDown = (index, e) => {
    if (e.key === 'Backspace' && !otp[index] && index > 0) {
      document.getElementById(`otp-${index - 1}`).focus();
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const otpValue = otp.join('');
    if (otpValue.length !== 6) {
      toast.error('Please enter complete 6-digit OTP');
      return;
    }
    setLoading(true);
    try {
      await new Promise(resolve => setTimeout(resolve, 1500));
      toast.success('OTP verified successfully! ✅');
      navigate('/reset-password');
    } catch (error) {
      toast.error('Invalid OTP. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleResend = () => {
    if (timer > 0) return;
    setTimer(45);
    toast.success('OTP resent to your email!');
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 via-emerald-50 to-white p-4">
      <div className="bg-white rounded-3xl shadow-2xl p-8 md:p-10 w-full max-w-md relative overflow-hidden">
        <div className="absolute -top-20 -right-20 w-40 h-40 bg-green-100 rounded-full opacity-50"></div>
        <div className="absolute -bottom-20 -left-20 w-40 h-40 bg-green-100 rounded-full opacity-50"></div>

        <div className="relative z-10">
          <Link to="/forgot-password" className="flex items-center space-x-2 text-green-600 hover:text-green-700 mb-6">
            <FaArrowLeft />
            <span>Back</span>
          </Link>

          <div className="flex items-center justify-center space-x-3 mb-6">
            <div className="w-12 h-12 bg-gradient-to-br from-green-400 to-green-600 rounded-2xl flex items-center justify-center">
              <FaLeaf className="text-white text-2xl" />
            </div>
            <span className="text-3xl font-bold gradient-text">DeepLeaf</span>
          </div>

          <h2 className="text-2xl font-bold text-center text-gray-800 mb-2">Verify Your Email 📧</h2>
          <p className="text-center text-gray-500 mb-8">Enter the 6-digit code sent to your email address</p>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="flex justify-center gap-2">
              {otp.map((digit, index) => (
                <input
                  key={index}
                  id={`otp-${index}`}
                  type="text"
                  maxLength="1"
                  value={digit}
                  onChange={(e) => handleChange(index, e.target.value)}
                  onKeyDown={(e) => handleKeyDown(index, e)}
                  className="w-12 h-14 text-center text-2xl font-bold border-2 border-gray-200 rounded-xl focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all bg-gray-50"
                />
              ))}
            </div>

            <p className="text-center text-sm text-gray-500">
              Didn't receive code?{' '}
              <button
                type="button"
                onClick={handleResend}
                disabled={timer > 0}
                className={`font-semibold ${timer > 0 ? 'text-gray-400 cursor-not-allowed' : 'text-green-600 hover:text-green-700'}`}
              >
                Resend {timer > 0 && `(${String(Math.floor(timer / 60)).padStart(2, '0')}:${String(timer % 60).padStart(2, '0')})`}
              </button>
            </p>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-xl font-semibold hover:from-green-600 hover:to-green-700 transition-all hover:scale-[1.02] disabled:opacity-70 disabled:cursor-not-allowed"
            >
              {loading ? (
                <span className="flex items-center justify-center">
                  <svg className="animate-spin h-5 w-5 mr-3 text-white" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  Verifying...
                </span>
              ) : (
                'Verify OTP'
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default OTPVerification;