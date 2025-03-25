const express = require("express");
const { authMiddleware } = require("../middleware/authentication"); 
const User = require("../models/User");

const router = express.Router();

router.get("/profile", authMiddleware, (req, res) => {
  res.json({ message: "Welcome to your profile", userId: req.user.id });
});

// Add university to favorites
router.post("/favorites/:universityId", authMiddleware, async (req, res) => {
  try {
    const user = await User.findById(req.user.id); // 🔹 Fixed user ID extraction
    if (!user) return res.status(404).json({ error: "User not found" });

    const { universityId } = req.params;
    if (user.favorites.includes(universityId)) {
      return res.status(400).json({ error: "University already in favorites" });
    }

    user.favorites.push(universityId);
    await user.save();
    res.json({ message: "Added to favorites", favorites: user.favorites });
  } catch (error) {
    res.status(500).json({ error: "Server error" });
  }
});

// Remove university from favorites
router.delete("/favorites/:universityId", authMiddleware, async (req, res) => {
  try {
    const user = await User.findById(req.user.id); // 🔹 Fixed user ID extraction
    if (!user) return res.status(404).json({ error: "User not found" });

    user.favorites = user.favorites.filter(
      (fav) => fav.toString() !== req.params.universityId
    );
    await user.save();
    res.json({ message: "Removed from favorites", favorites: user.favorites });
  } catch (error) {
    res.status(500).json({ error: "Server error" });
  }
});

// Get user's favorite universities
router.get("/favorites", authMiddleware, async (req, res) => {
  try {
    const user = await User.findById(req.user.id).populate("favorites"); // 🔹 Fixed user ID extraction
    if (!user) return res.status(404).json({ error: "User not found" });

    res.json(user.favorites);
  } catch (error) {
    res.status(500).json({ error: "Server error" });
  }
});

module.exports = router;
