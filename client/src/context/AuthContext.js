import { createContext, useState, useEffect } from "react";
import axios from "axios";
import { jwtDecode } from "jwt-decode";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [loading, setLoading] = useState(true);

  // Fetch user details from backend
  const fetchUser = async () => {
    try {
      const res = await axios.get("http://localhost:6969/api/auth/me", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setUser(res.data);
    } catch (error) {
      console.error("Error fetching user:", error);
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (token) {
      fetchUser();
    } else {
      setLoading(false);
    }
  }, [token]);

  const login = async (email, password) => {
    try {
      const res = await axios.post("http://localhost:6969/api/auth/login", { email, password });
      localStorage.setItem("token", res.data.token);
      setToken(res.data.token);
      await fetchUser(); // Fetch user after login
      return true;  // ✅ Indicate success
    } catch (error) {
      console.error("Login failed:", error.response?.data?.message);
      return false; // ❌ Indicate failure
    }
  };
  

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
