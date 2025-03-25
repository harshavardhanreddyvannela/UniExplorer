import React, { useContext, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  Navbar,
  NavbarBrand,
  Nav,
  NavItem,
  NavLink,
  NavbarToggler,
  Collapse,
  Dropdown,
  DropdownToggle,
  DropdownMenu,
  DropdownItem,
  Button,
} from "reactstrap";
import AuthContext from "../context/AuthContext";
import { FaUserCircle, FaUniversity, FaStar, FaSignOutAlt, FaUserShield } from "react-icons/fa";

const MyNavbar = () => {
  const { user, logout } = useContext(AuthContext);
  const [isOpen, setIsOpen] = useState(false);
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <Navbar color="dark" dark expand="md" className="px-4 shadow-sm">
      <NavbarBrand tag={Link} to="/" className="fw-bold text-light">
        🎓 University Explorer
      </NavbarBrand>

      <NavbarToggler onClick={() => setIsOpen(!isOpen)} />

      <Collapse isOpen={isOpen} navbar>
        <Nav className="ms-auto align-items-center" navbar>
          <NavItem>
            <NavLink tag={Link} to="/" className="nav-link-hover">🏠 Home</NavLink>
          </NavItem>

          {user && (
            <Dropdown isOpen={dropdownOpen} toggle={() => setDropdownOpen(!dropdownOpen)} nav inNavbar>
              <DropdownToggle nav caret className="nav-link-hover">
                🌍 Explore
              </DropdownToggle>
              <DropdownMenu end>
                <DropdownItem tag={Link} to="/universities">
                  <FaUniversity className="me-2" /> Universities
                </DropdownItem>
                <DropdownItem tag={Link} to="/favorites">
                  <FaStar className="me-2 text-warning" /> Favorites
                </DropdownItem>
              </DropdownMenu>
            </Dropdown>
          )}

          {user?.role === "admin" && (
            <NavItem>
              <NavLink tag={Link} to="/admin" className="nav-link-hover text-warning fw-bold">
                <FaUserShield className="me-1" /> Admin Panel
              </NavLink>
            </NavItem>
          )}

          {user && (
            <NavItem>
              <NavLink tag={Link} to="/profile" className="nav-link-hover">
                <FaUserCircle className="me-1" /> Profile
              </NavLink>
            </NavItem>
          )}

          {user && (
            <NavItem>
              <Button color="outline-danger" className="ms-2 btn-sm" onClick={handleLogout}>
                <FaSignOutAlt className="me-1" /> Logout
              </Button>
            </NavItem>
          )}
        </Nav>
      </Collapse>
    </Navbar>
  );
};

export default MyNavbar;
