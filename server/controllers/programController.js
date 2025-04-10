const University = require("../models/University");
const Program = require("../models/Program");


// ✅ Create a new program
const createProgram = async (req, res) => {
    try {
      const { name, duration, degreeType, university } = req.body;
  
      if (!name || !duration || !degreeType || !university) {
        return res.status(400).json({ error: "All fields are required" });
      }
  
      // Ensure the university exists
      const universityExists = await University.findById(university);
      if (!universityExists) {
        return res.status(404).json({ error: "University not found" });
      }
  
      // Create the program
      const newProgram = await Program.create({ name, duration, degreeType, university });
  
      // Add program to the university's programs array
      universityExists.programs.push(newProgram._id);
      await universityExists.save();
  
      res.status(201).json(newProgram);
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: "Server error" });
    }
  };
  
  

// ✅ Get all programs
const getPrograms = async (req, res) => {
  try {
    let query = {};

    // Search by program name
    if (req.query.name) {
      query.name = { $regex: req.query.name, $options: "i" };
    }

    // Filter by degree type
    if (req.query.degreeType) {
      query.degreeType = req.query.degreeType;
    }

    // Filter by university ID
    if (req.query.university) {
      query.university = req.query.university;
    }

    // Sorting (default: name ascending)
    let sortOption = { name: 1 };
    if (req.query.sortBy) {
      const sortField = req.query.sortBy;
      const sortOrder = req.query.order === "desc" ? -1 : 1;
      sortOption = { [sortField]: sortOrder };
    }

    // Pagination - modified to return all results by default
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 1000; // Increased from 10 to 1000
    const skip = (page - 1) * limit;

    // Fetch programs
    const programs = await Program.find(query)
      .populate("university")
      .sort(sortOption)
      .skip(skip)
      .limit(limit);

    // Total count for pagination metadata
    const total = await Program.countDocuments(query);

    res.json({
      total,
      page,
      totalPages: Math.ceil(total / limit),
      programs,
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Server error" });
  }
};



// ✅ Get a single program by ID
const getProgramById = async (req, res) => {
  try {
    const program = await Program.findById(req.params.id).populate("university");
    if (!program) return res.status(404).json({ error: "Program not found" });
    res.json(program);
  } catch (error) {
    res.status(500).json({ error: "Server error" });
  }
};

// ✅ Update a program
const updateProgram = async (req, res) => {
  try {
    const program = await Program.findByIdAndUpdate(req.params.id, req.body, { new: true });
    if (!program) return res.status(404).json({ error: "Program not found" });
    res.json(program);
  } catch (error) {
    res.status(500).json({ error: "Server error" });
  }
};

// ✅ Delete a program
const deleteProgram = async (req, res) => {
    try {
      const { id } = req.params;
  
      const program = await Program.findById(id);
      if (!program) {
        return res.status(404).json({ error: "Program not found" });
      }
  
      // Remove the program from the university's programs array
      await University.findByIdAndUpdate(program.university, {
        $pull: { programs: id },
      });
  
      // Delete the program
      await Program.findByIdAndDelete(id);
  
      res.json({ message: "Program deleted successfully" });
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: "Server error" });
    }
  };

module.exports = { createProgram, getPrograms, getProgramById, updateProgram, deleteProgram };
