const express = require("express");
const {
  createUniversity,
  getUniversities,
  getUniversityById,
  updateUniversity,
  deleteUniversity,
} = require("../controllers/universityController");
const { authMiddleware, adminMiddleware } = require("../middleware/authentication");

const router = express.Router();

// CRUD Routes
router.post("/", authMiddleware, adminMiddleware, createUniversity); // ✅ Protected route for adding universities
router.get("/", getUniversities); // Get all universities
router.get("/:id", getUniversityById); // Get a single university by ID
router.put("/:id", authMiddleware, adminMiddleware, updateUniversity); // ✅ Protected update
router.delete("/:id", authMiddleware, adminMiddleware, deleteUniversity); // ✅ Protected delete


module.exports = router;