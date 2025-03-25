const mongoose = require("mongoose");

const ProgramSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: [true, "Program name is required"],
      trim: true,
    },
    duration: {
      type: String, // Example: "4 years"
      required: [true, "Duration is required"],
    },
    degreeType: {
      type: String, // Example: "Bachelor", "Master", "PhD"
      required: [true, "Degree type is required"],
    },
    university: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "University", // Linking to universities
      required: [true, "University is required"],
    },
  },
  { timestamps: true }
);

module.exports = mongoose.model("Program", ProgramSchema);
