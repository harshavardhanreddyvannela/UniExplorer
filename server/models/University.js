const mongoose = require("mongoose");

const UniversitySchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: [true, "University name is required"],
      trim: true,
    },
    location: {
      type: String,
      required: [true, "Location is required"],
    },
    ranking: {
      type: Number,
      required: true,
    },
    description: {
      type: String,
    },
    website: {
      type: String,
    },
    programs: [
      {
        type: mongoose.Schema.Types.ObjectId,
        ref: "Program",
      }
    ],
  },
  { timestamps: true }
);

module.exports = mongoose.model("University", UniversitySchema);
