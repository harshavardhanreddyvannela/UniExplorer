const express = require("express");
const { authMiddleware, adminMiddleware } = require("../middleware/authentication");
const {
  createProgram,
  getPrograms,
  getProgramById,
  updateProgram,
  deleteProgram,
} = require("../controllers/programController");

const router = express.Router();

// Routes
router.post("/", authMiddleware, adminMiddleware, createProgram); // Create a program (Admin only)
router.get("/", getPrograms); // Get all programs
router.get("/:id", getProgramById); // Get a specific program
router.put("/:id", authMiddleware, adminMiddleware, updateProgram); // Update a program (Admin only)
router.delete("/:id", authMiddleware, adminMiddleware, deleteProgram); // Delete a program (Admin only)

module.exports = router;