const express = require("express");
const { authMiddleware, adminMiddleware } = require("../middleware/authentication");
const { getUsers, updateUserRole, deleteUser } = require("../controllers/adminController");

const router = express.Router();

// Get all users
router.get("/users", authMiddleware, adminMiddleware, getUsers);

// Update user role
router.put("/users/:id", authMiddleware, adminMiddleware, updateUserRole);

// Delete user
router.delete("/users/:id", authMiddleware, adminMiddleware, deleteUser);

module.exports = router;
