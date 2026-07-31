import React from 'react';
import { Link, useNavigate } from 'react-router-dom'; 
import { motion } from 'framer-motion';

// Images Imports
import heroBg from "../../assets/images/hero-bg.jpg";
import dashboardPreview from "../../assets/images/dashboard-preview.png"; 
import plant from "../../assets/images/plant.png";
import users from "../../assets/images/users.png";

// ------------------------------------------
// Animation Variants
// ------------------------------------------
const fadeUp = {
  hidden: { opacity: 0, y: 40 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.7, ease: "easeOut" } }
};

const slideLeft = {
  hidden: { opacity: 0, x: -60 },
  visible: { opacity: 1, x: 0, transition: { duration: 0.8, ease: "easeOut" } }
};

const slideRight = {
  hidden: { opacity: 0, x: 60 },
  visible: { opacity: 1, x: 0, transition: { duration: 0.8, ease: "easeOut" } }
};

const staggerContainer = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.2, delayChildren: 0.1 }
  }
};

// ------------------------------------------
// Main Home Component
// ------------------------------------------
const Home = () => {
  const navigate = useNavigate();

  // ✅ LOGIN CHECK LOGIC
  const isLoggedIn = true; // Asli project mein localStorage se check karna

  // ✅ CLICK HANDLER FUNCTION
  const handleGetStarted = () => {
    if (isLoggedIn) {
      navigate('/detection'); 
    } else {
      navigate('/login'); 
    }
  };

  return (
    <div className="w-full bg-[#03120E] text-slate-900 font-sans overflow-x-hidden selection:bg-green-200 min-h-screen relative">
      
      {/* ================= HERO SECTION ================= */}
      <section className="relative min-h-[90vh] lg:min-h-screen w-full flex items-center overflow-hidden pt-2 lg:pt-8">
        {/* Background Image */}
        <div className="absolute inset-0 z-0">
          <div 
            className="absolute inset-0 bg-cover bg-center bg-no-repeat scale-105" 
            style={{ backgroundImage: `url(${heroBg})` }}
          />
          <div className="absolute inset-0 bg-gradient-to-r from-[#0B3D2E]/90 via-[#0A241C]/80 to-[#000000]/70" />
        </div>

        <div className="container mx-auto px-5 lg:px-12 relative z-10 grid grid-cols-1 lg:grid-cols-2 gap-6 lg:gap-10 items-center py-4 lg:py-8 mt-[-10px]">
          
          {/* ================= LEFT CONTENT ================= */}
          <motion.div 
            variants={staggerContainer}
            initial="hidden"
            animate="visible"
            className="flex flex-col gap-4 lg:gap-6 max-w-2xl text-center lg:text-left items-center lg:items-start"
          >
            {/* DeepLeaf Badge */}
            <motion.div variants={fadeUp} className="inline-flex items-center gap-2 bg-white/10 backdrop-blur-md border border-white/20 px-4 py-2 rounded-full text-sm font-medium text-white shadow-sm w-fit">
              <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
              DeepLeaf AI 2.0
            </motion.div>

            {/* Main Heading */}
            <motion.h1 variants={fadeUp} className="text-4xl sm:text-5xl lg:text-7xl font-extrabold leading-tight tracking-tight text-white drop-shadow-lg">
              Smart Plant Care <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-emerald-300">Starts Here</span>
              <span className="inline-block ml-2 text-green-400">🌿</span>
            </motion.h1>

            {/* Description */}
            <motion.p variants={fadeUp} className="text-base sm:text-lg lg:text-xl text-gray-200 leading-relaxed max-w-lg drop-shadow-md">
              Identify plant diseases instantly with cutting-edge AI. Get expert, organic solutions to keep your crops healthy and maximize yield.
            </motion.p>

            {/* Buttons */}
            <motion.div variants={fadeUp} className="flex flex-wrap gap-4 pt-2 justify-center lg:justify-start">
              
              {/* HERO GET STARTED (Connected) */}
              <button 
                onClick={handleGetStarted}
                className="relative group bg-green-500 hover:bg-green-400 text-white px-8 py-3.5 rounded-full font-semibold shadow-lg shadow-green-500/30 transition-all duration-300 transform hover:-translate-y-1 hover:shadow-xl flex items-center gap-2 cursor-pointer"
              >
                Get Started
                <span className="group-hover:translate-x-1 transition-transform">→</span>
              </button>

              <Link to="/learn-more" className="bg-white/10 backdrop-blur-sm border border-white/30 hover:bg-white/20 text-white px-8 py-3.5 rounded-full font-medium transition-all duration-300 hover:shadow-md flex items-center gap-2">
                Learn More
                <span className="text-green-300">🌱</span>
              </Link>
            </motion.div>

            {/* Trusted By Users */}
            <motion.div variants={fadeUp} className="mt-4 flex items-center gap-6 justify-center lg:justify-start">
              <div className="flex -space-x-3">
                <img className="w-10 h-10 rounded-full border-2 border-slate-800" src={users} alt="User 1" />
                <img className="w-10 h-10 rounded-full border-2 border-slate-800" src={users} alt="User 2" />
                <img className="w-10 h-10 rounded-full border-2 border-slate-800" src={users} alt="User 3" />
                <div className="w-10 h-10 rounded-full border-2 border-slate-800 bg-green-500/20 flex items-center justify-center text-xs font-bold text-green-300 backdrop-blur-sm">10k+</div>
              </div>
              <div className="flex flex-col">
                <div className="flex text-yellow-400 text-sm">
                  {[...Array(5)].map((_, i) => (
                    <span key={i}>★</span>
                  ))}
                </div>
                <span className="text-sm font-medium text-gray-300">Trusted by 10,000+ Farmers</span>
              </div>
            </motion.div>
          </motion.div>

          {/* ================= RIGHT CONTENT ================= */}
          <motion.div 
            variants={slideRight}
            initial="hidden"
            animate="visible"
            className="relative flex justify-center items-center h-full min-h-[350px] lg:min-h-[600px]"
          >
            {/* Premium Dark Green Blur Circle */}
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[220px] sm:w-[350px] lg:w-[550px] h-[220px] sm:h-[350px] lg:h-[550px] bg-green-500/10 rounded-full blur-3xl z-0" />

            {/* Plant Image */}
            <img 
              src={plant} 
              alt="Plant" 
              className="absolute -bottom-10 right-0 lg:-right-10 h-[200px] sm:h-[280px] lg:h-[450px] object-contain z-10 drop-shadow-2xl opacity-90"
            />

            {/* Image Container */}
            <motion.div 
              animate={{ y: [0, -8, 0] }}
              transition={{ duration: 6, repeat: Infinity, ease: "easeInOut" }}
              className="relative z-20 w-[320px] sm:w-[400px] lg:w-[560px] aspect-[4/3] bg-slate-800/50 backdrop-blur-xl rounded-3xl shadow-2xl shadow-black/40 border border-white/10 overflow-hidden flex items-center justify-center flex-shrink-0 p-2"
            >
              <img 
                src={dashboardPreview} 
                alt="DeepLeaf Dashboard Preview" 
                className="w-full h-full object-cover rounded-2xl shadow-inner"
              />
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* ================= STATS SECTION ================= */}
      <section className="py-16 lg:py-24 bg-white/10 backdrop-blur-md border-y border-white/5">
        <div className="container mx-auto px-6 lg:px-12">
          <motion.div 
            initial="hidden" 
            whileInView="visible" 
            viewport={{ once: true, margin: "-100px" }}
            variants={staggerContainer}
            className="grid grid-cols-2 lg:grid-cols-4 gap-6 lg:gap-8"
          >
            {[
              { num: "10K+", label: "Happy Users", icon: "👨‍🌾" },
              { num: "50K+", label: "Diseases Detected", icon: "🔬" },
              { num: "98.7%", label: "AI Accuracy", icon: "🎯" },
              { num: "24/7", label: "Expert Support", icon: "🛠️" }
            ].map((stat, index) => (
              <motion.div 
                key={index}
                variants={fadeUp}
                whileHover={{ y: -8, boxShadow: "0 20px 40px -12px rgba(0,0,0,0.1)" }}
                className="bg-white/20 backdrop-blur-md border border-white/10 rounded-2xl p-6 lg:p-8 text-center transition-all duration-300 flex flex-col items-center shadow-sm text-white"
              >
                <span className="text-3xl lg:text-4xl mb-2">{stat.icon}</span>
                <h3 className="text-2xl lg:text-4xl font-extrabold">{stat.num}</h3>
                <p className="text-gray-300 text-sm lg:text-base mt-1 font-medium">{stat.label}</p>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* ================= FEATURES SECTION ================= */}
      <section className="py-20 lg:py-32 bg-white/5 backdrop-blur-sm">
        <div className="container mx-auto px-6 lg:px-12">
          <motion.div 
            initial="hidden" 
            whileInView="visible" 
            viewport={{ once: true }}
            variants={fadeUp}
            className="text-center max-w-3xl mx-auto mb-16"
          >
            <span className="text-green-400 font-semibold tracking-wide uppercase text-sm bg-green-500/10 backdrop-blur-sm px-3 py-1 rounded-full border border-green-500/20">Why DeepLeaf</span>
            <h2 className="text-4xl lg:text-5xl font-extrabold text-white mt-4 mb-6">Everything You Need for <span className="text-green-400">Healthy Plants</span></h2>
            <p className="text-gray-300 text-lg">Powered by advanced computer vision, we provide instant, accurate diagnostics and natural remedies right to your phone.</p>
          </motion.div>

          <motion.div 
            initial="hidden" 
            whileInView="visible" 
            viewport={{ once: true }}
            variants={staggerContainer}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
          >
            {[
              { icon: "🤖", title: "AI Disease Detection", desc: "State-of-the-art AI identifies over 50 plant diseases with 98.7% accuracy in under 3 seconds." },
              { icon: "⚡", title: "Instant Results", desc: "No more waiting for lab reports. Get diagnosis and confidence scores instantly in the field." },
              { icon: "🌱", title: "Natural Remedies", desc: "Receive eco-friendly, organic treatment plans tailored to the specific disease detected." },
              { icon: "📈", title: "Crop History Tracking", desc: "Monitor your plant's health over time and get alerts for recurring issues in your farm." },
              { icon: "📱", title: "Offline Capable", desc: "Our lightweight model works offline, ensuring you get help even in remote farming areas." },
              { icon: "🌍", title: "Farmer Community", desc: "Connect with local experts and other farmers to share best practices and solutions." }
            ].map((feature, index) => (
              <motion.div
                key={index}
                variants={slideLeft}
                whileHover={{ y: -12, boxShadow: "0 25px 50px -12px rgba(0,255,0,0.15)" }}
                className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/5 shadow-sm hover:border-green-400/50 transition-all duration-300 relative overflow-hidden group"
              >
                <div className="absolute inset-0 bg-gradient-to-br from-green-500/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                <div className="relative z-10">
                  <div className="w-14 h-14 bg-green-500/20 backdrop-blur-sm rounded-2xl flex items-center justify-center text-3xl mb-6 group-hover:bg-green-500 group-hover:text-white transition-colors duration-300 text-green-400">
                    {feature.icon}
                  </div>
                  <h3 className="text-xl font-bold text-white mb-3">{feature.title}</h3>
                  <p className="text-gray-300 leading-relaxed text-sm lg:text-base">{feature.desc}</p>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* ================= HOW IT WORKS SECTION ================= */}
      <section className="py-20 lg:py-32 bg-white/5 backdrop-blur-sm">
        <div className="container mx-auto px-6 lg:px-12">
          <motion.div 
            initial="hidden" 
            whileInView="visible" 
            viewport={{ once: true }}
            variants={fadeUp}
            className="text-center max-w-2xl mx-auto mb-16"
          >
            <h2 className="text-4xl lg:text-5xl font-extrabold text-white mb-4">How It Works</h2>
            <p className="text-gray-300 text-lg">Get your plants diagnosed in three simple steps, no matter where you are.</p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 lg:gap-12 relative">
            
            <div className="hidden md:block absolute top-1/3 left-[15%] w-[70%] h-0.5 border-t border-dashed border-green-500/30 -z-10" />
            <div className="hidden md:block absolute top-1/3 left-[15%] w-[70%] h-0.5 border-t border-dashed border-green-500/30 -z-10 transform translate-x-full" />

            {[
              { step: "1", title: "Capture", desc: "Use your smartphone to take a clear, high-resolution photo of the infected plant leaf." },
              { step: "2", title: "Analyze", desc: "Our AI engine processes the image, analyzing leaf textures and patterns against our vast dataset." },
              { step: "3", title: "Grow", desc: "Receive the diagnosis, confidence score, and step-by-step organic remedies to save your plant." }
            ].map((item, index) => (
              <motion.div
                key={index}
                initial="hidden"
                whileInView="visible"
                viewport={{ once: true, margin: "-50px" }}
                variants={fadeUp}
                transition={{ delay: index * 0.15 }}
                whileHover={{ scale: 1.02 }}
                className="flex flex-col items-center text-center p-8 rounded-3xl bg-white/10 backdrop-blur-md border border-white/5 hover:shadow-xl transition-all duration-300"
              >
                <div className="w-16 h-16 rounded-full bg-green-500 text-white text-2xl font-bold flex items-center justify-center shadow-lg shadow-green-500/30 mb-6">
                  {item.step}
                </div>
                <h3 className="text-xl font-bold text-white mb-3">{item.title}</h3>
                <p className="text-gray-300 leading-relaxed">{item.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* ================= CTA SECTION ================= */}
      <section className="relative overflow-hidden py-24 lg:py-32 bg-gradient-to-br from-green-600 to-emerald-600 text-white">
        <motion.div 
          animate={{ x: [0, 50, 0], y: [0, -30, 0] }}
          transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
          className="absolute top-10 left-10 w-64 h-64 bg-white/5 rounded-full blur-2xl"
        />
        <motion.div 
          animate={{ x: [0, -40, 0], y: [0, 40, 0] }}
          transition={{ duration: 15, repeat: Infinity, ease: "linear", delay: 2 }}
          className="absolute bottom-20 right-10 w-80 h-80 bg-white/10 rounded-full blur-3xl"
        />

        <div className="container mx-auto px-6 lg:px-12 relative z-10 text-center">
          <motion.div 
            initial={{ scale: 0.9, opacity: 0 }}
            whileInView={{ scale: 1, opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="max-w-4xl mx-auto"
          >
            <h2 className="text-4xl lg:text-6xl font-extrabold leading-tight mb-6">
              Ready to protect your crops <br /> with the power of AI?
            </h2>
            <p className="text-green-100 text-lg lg:text-xl mb-10 max-w-2xl mx-auto opacity-90">
              Join 10,000+ farmers who have already saved their harvest using DeepLeaf. Start scanning today.
            </p>
            
            <div className="flex flex-wrap justify-center gap-4">
              <button 
                onClick={handleGetStarted} 
                className="bg-white text-green-700 hover:bg-slate-50 px-10 py-4 rounded-full font-bold shadow-xl shadow-black/20 hover:shadow-2xl hover:-translate-y-1 transition-all duration-300 cursor-pointer"
              >
                Get Started
              </button>
              
              <Link to="/contact" className="border border-white/30 hover:bg-white/10 text-white px-10 py-4 rounded-full font-semibold transition-all duration-300 backdrop-blur-sm">
                Contact Sales
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* ================= FOOTER REMOVED ================= */}
      {/* Poore footer ka code yahan se hata diya gaya hai */}
      
    </div>
  );
};

export default Home;