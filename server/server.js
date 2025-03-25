require("dotenv").config();
const express = require("express");
const cors = require("cors");
const helmet = require("helmet");
const rateLimit = require("express-rate-limit");
const connectDB = require("./db/connect");

const app = express();

// Middleware
app.use(express.json());
app.use(cors());
app.use(helmet()); // Security headers

// Rate limiter (limits API requests)
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per window
});
app.use(limiter);

// Test Route
app.get("/", (req, res) => {
  res.json({ message: "Welcome to University Explorer API!" });
});

// Import Routes
const authRoutes = require("./routes/auth");
const userRoutes = require("./routes/user"); // ✅ Import user routes
const universityRoutes = require("./routes/universities");
const programRoutes = require("./routes/programs"); // Import program routes
const reviewRoutes = require("./routes/reviews"); // Import review routes
const adminRoutes = require("./routes/admin");


// Use Routes
app.use("/api/auth", authRoutes);
app.use("/api/user", userRoutes); // ✅ Add user routes
app.use("/api/universities", universityRoutes);
app.use("/api/programs", programRoutes); // Use program routes
app.use("/api/reviews", reviewRoutes);
app.use("/api/admin", adminRoutes);

// Start server
const PORT = process.env.PORT || 6969;

const startServer = async () => {
  try {
    await connectDB();
    app.listen(PORT, () => console.log(`🚀 Server running on port ${PORT}`));
  } catch (error) {
    console.error("❌ Server failed to start:", error);
  }
};

startServer();
