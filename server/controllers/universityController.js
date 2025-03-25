const University = require("../models/University");

// Create a new university
const createUniversity = async (req, res) => {
  try {
    console.log("Received Data:", req.body); // Debugging log

    const { name, location, ranking, description, website, programs } = req.body;

    // Fix the validation check
    if (!name || !location || ranking === undefined || ranking === null) {
      return res.status(400).json({ error: "All fields are required" });
    }

    const newUniversity = new University({
      name,
      location,
      ranking,
      description,
      website,
      programs,
    });

    await newUniversity.save();
    res.status(201).json(newUniversity);
  } catch (error) {
    console.error("Error creating university:", error);
    res.status(500).json({ error: "Server error" });
  }
};

// Get all universities
const getUniversities = async (req, res) => {
  try {
    let query = {};

    // Search by name
    if (req.query.name) {
      query.name = { $regex: req.query.name, $options: "i" };
    }

    // Filter by location
    if (req.query.location) {
      query.location = { $regex: req.query.location, $options: "i" };
    }

    // Filter by ranking
    if (req.query.minRanking) {
      const minRanking = Number(req.query.minRanking); // Ensure it's a Number
      if (!isNaN(minRanking)) {
        query.ranking = { $gte: minRanking };
      }
    }

    // Sorting (default: ranking ascending)
    let sortOption = { ranking: 1 }; // Default sorting by ranking ASC
    if (req.query.sortBy) {
      const sortField = req.query.sortBy;
      const sortOrder = req.query.order === "desc" ? -1 : 1;
      sortOption = { [sortField]: sortOrder };
    }

    // Pagination
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 10;
    const skip = (page - 1) * limit;

    // Aggregation pipeline
    const pipeline = [
      { $match: query },
      {
        $lookup: {
          from: "programs",
          localField: "programs",
          foreignField: "_id",
          as: "programs",
        },
      },
      {
        $match: req.query.program
          ? { "programs.name": { $regex: req.query.program, $options: "i" } }
          : {},
      },
      { $sort: sortOption },
      { $skip: skip },
      { $limit: limit },
    ];

    // Fetch universities
    const universities = await University.aggregate(pipeline);

    // Total count for pagination metadata
    const total = await University.countDocuments(query);

    res.json({
      total,
      page,
      totalPages: Math.ceil(total / limit),
      universities,
    });
  } catch (error) {
    console.error("Error fetching universities:", error);
    res.status(500).json({ error: "Server error" });
  }
};

// Get a single university by ID
const getUniversityById = async (req, res) => {
  try {
    const university = await University.findById(req.params.id).populate("programs");
    if (!university) return res.status(404).json({ error: "University not found" });
    res.status(200).json(university);
  } catch (error) {
    res.status(500).json({ error: "Server error" });
  }
};

// Update a university
const updateUniversity = async (req, res) => {
  try {
    const updatedUniversity = await University.findByIdAndUpdate(req.params.id, req.body, { new: true });
    if (!updatedUniversity) return res.status(404).json({ error: "University not found" });
    res.status(200).json(updatedUniversity);
  } catch (error) {
    res.status(500).json({ error: "Server error" });
  }
};

// Delete a university
const deleteUniversity = async (req, res) => {
  try {
    const deletedUniversity = await University.findByIdAndDelete(req.params.id);
    if (!deletedUniversity) return res.status(404).json({ error: "University not found" });
    res.status(200).json({ message: "University deleted successfully" });
  } catch (error) {
    res.status(500).json({ error: "Server error" });
  }
};

module.exports = {
  createUniversity,
  getUniversities,
  getUniversityById,
  updateUniversity,
  deleteUniversity,
};
