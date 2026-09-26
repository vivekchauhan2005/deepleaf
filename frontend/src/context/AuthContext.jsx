import React, { createContext, useState, useContext, useEffect } from 'react';
import toast from 'react-hot-toast';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const storedUser = localStorage.getItem('user');

    if (token && storedUser) {
      setUser(JSON.parse(storedUser));
    }

    setLoading(false);
  }, []);

  // ================= LOGIN =================
  const login = async (email, password) => {
    try {
      const response = await fetch("http://localhost:8000/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Login failed");
      }

      localStorage.setItem("token", data.access_token);

      const userData = {
        email,
        token: data.access_token,
      };

      localStorage.setItem("user", JSON.stringify(userData));

      setUser(userData);

      toast.success("Welcome Back! 🌿");

      return {
        success: true,
        data,
      };
    } catch (error) {
      toast.error(error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  };

  // ================= REGISTER (Aapke diye gaye code ke hisaab se) =================
  const register = async (username, email, password) => {
    try {
      const response = await fetch("http://localhost:8000/auth/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username,
          email,
          password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Registration failed");
      }

      toast.success("Account Created Successfully 🎉");

      return {
        success: true,
        data,
      };
    } catch (error) {
      toast.error(error.message);

      return {
        success: false,
        error: error.message,
      };
    }
  };

  // ================= LOGOUT =================
  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");

    setUser(null);

    toast.success("Logged out Successfully");
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};