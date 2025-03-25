const express = require("express");
const { authMiddleware } = require("../middleware/authentication");
const Review = require("../models/Review");

const router = express.Router();

// Add a review
router.post("/:universityId", authMiddleware, async (req, res) => {
  try {
    const { rating, comment } = req.body;
    if (!rating || !comment) {
      return res.status(400).json({ error: "All fields are required" });
    }

    const review = new Review({
      university: req.params.universityId,
      user: req.user.userId,
      rating,
      comment,
    });

    await review.save();
    res.json({ message: "Review added successfully", review });
  } catch (error) {
    res.status(500).json({ error: "Server error" });
  }
});

// Get reviews for a university
router.get("/:universityId", async (req, res) => {
  try {
    const reviews = await Review.find({
      university: req.params.universityId,
    }).populate("user", "name");

    res.json(reviews);
  } catch (error) {
    res.status(500).json({ error: "Server error" });
  }
});

// Delete a review (only the user who created it can delete it)
router.delete("/:reviewId", authMiddleware, async (req, res) => {
  try {
    const review = await Review.findById(req.params.reviewId);
    if (!review) return res.status(404).json({ error: "Review not found" });

    if (review.user.toString() !== req.user.userId) {
      return res.status(403).json({ error: "Unauthorized" });
    }

    await review.deleteOne();
    res.json({ message: "Review deleted successfully" });
  } catch (error) {
    res.status(500).json({ error: "Server error" });
  }
});

module.exports = router;
