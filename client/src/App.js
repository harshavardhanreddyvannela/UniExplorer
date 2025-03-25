import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Universities from "./pages/Universities";
import Favorites from "./pages/Favorites";
import Profile from "./pages/Profile";
import UniversityDetails from "./pages/UniversityDetails"; // Ensure it's in pages/
import Login from "./pages/Login";
import Register from "./pages/Register";
import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute"; // Import ProtectedRoute
import AdminDashboard from "./pages/admin/AdminDashboard";
import UniversityList from "./pages/admin/UniversityList";
import ProgramList from "./pages/admin/ProgramList";
import UserList from "./pages/admin/UserList"; // ✅ Import UserList

const App = () => {
  return (
   <AuthProvider>
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route element={<ProtectedRoute/>}>
        <Route path="/universities" element={<Universities />} />
        <Route path="/universities/:id" element={<UniversityDetails />} /> {/* Add this */}
        <Route path="/favorites" element={<Favorites />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/admin/universities" element={<UniversityList />} />
        <Route path="/admin/programs" element={<ProgramList />} />
        <Route path="/admin/users" element={<UserList />} /> {/* ✅ Add UserList */}
        </Route>
      </Routes>
    </Router>
   </AuthProvider>
  );
};

export default App;
