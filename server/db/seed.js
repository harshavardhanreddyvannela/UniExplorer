require('dotenv').config();
const connectDB = require('./connect');
const University = require('../models/University');
const Program = require('../models/Program');
const User = require('../models/User');
const Review = require('../models/Review');
const mongoose = require('mongoose');

// Sample data - Expanded to 35 universities
const universities = [
  // Original universities
  {
    name: 'Harvard University',
    location: 'Cambridge, MA, USA',
    ranking: 1,
    description: 'Founded in 1636, Harvard is America\'s oldest university and a prestigious Ivy League institution.',
    website: 'https://www.harvard.edu'
  },
  {
    name: 'Stanford University',
    location: 'Stanford, CA, USA',
    ranking: 2,
    description: 'Stanford is known for its entrepreneurial spirit and close ties to Silicon Valley.',
    website: 'https://www.stanford.edu'
  },
  {
    name: 'Massachusetts Institute of Technology',
    location: 'Cambridge, MA, USA',
    ranking: 3,
    description: 'MIT is a world leader in science and technology education and research.',
    website: 'https://www.mit.edu'
  },
  {
    name: 'University of Oxford',
    location: 'Oxford, UK',
    ranking: 4,
    description: 'Oxford is the oldest university in the English-speaking world with teaching dating back to 1096.',
    website: 'https://www.ox.ac.uk'
  },
  {
    name: 'University of Cambridge',
    location: 'Cambridge, UK',
    ranking: 5,
    description: 'Cambridge is renowned for its excellence in teaching and research across academic disciplines.',
    website: 'https://www.cam.ac.uk'
  },
  // Additional universities
  {
    name: 'California Institute of Technology',
    location: 'Pasadena, CA, USA',
    ranking: 6,
    description: 'Caltech is known for its strong focus on science and engineering education.',
    website: 'https://www.caltech.edu'
  },
  {
    name: 'Princeton University',
    location: 'Princeton, NJ, USA',
    ranking: 7,
    description: 'Princeton is an Ivy League university known for exceptional research and teaching.',
    website: 'https://www.princeton.edu'
  },
  {
    name: 'ETH Zurich',
    location: 'Zurich, Switzerland',
    ranking: 8,
    description: 'ETH Zurich is a science, technology, engineering and mathematics university.',
    website: 'https://ethz.ch'
  },
  {
    name: 'Imperial College London',
    location: 'London, UK',
    ranking: 9,
    description: 'Imperial College London specializes in science, engineering, medicine and business.',
    website: 'https://www.imperial.ac.uk'
  },
  {
    name: 'University of Chicago',
    location: 'Chicago, IL, USA',
    ranking: 10,
    description: 'UChicago is known for its rigorous academic culture and influential academic programs.',
    website: 'https://www.uchicago.edu'
  },
  {
    name: 'National University of Singapore',
    location: 'Singapore',
    ranking: 11,
    description: 'NUS is the oldest and largest university in Singapore with a global approach to education.',
    website: 'https://www.nus.edu.sg'
  },
  {
    name: 'Yale University',
    location: 'New Haven, CT, USA',
    ranking: 12,
    description: 'Yale is an Ivy League university known for excellence in teaching and research.',
    website: 'https://www.yale.edu'
  },
  {
    name: 'University of Tokyo',
    location: 'Tokyo, Japan',
    ranking: 13,
    description: 'The University of Tokyo is Japan\'s leading higher education institution.',
    website: 'https://www.u-tokyo.ac.jp'
  },
  {
    name: 'University of Toronto',
    location: 'Toronto, Canada',
    ranking: 14,
    description: 'U of T is Canada\'s top university with a rich history of innovation and research.',
    website: 'https://www.utoronto.ca'
  },
  {
    name: 'Tsinghua University',
    location: 'Beijing, China',
    ranking: 15,
    description: 'Tsinghua is one of China\'s most prestigious universities with strengths in engineering.',
    website: 'https://www.tsinghua.edu.cn'
  },
  {
    name: 'University of Pennsylvania',
    location: 'Philadelphia, PA, USA',
    ranking: 16,
    description: 'UPenn blends intellectual rigor with a practical approach in its education.',
    website: 'https://www.upenn.edu'
  },
  {
    name: 'Columbia University',
    location: 'New York, NY, USA',
    ranking: 17,
    description: 'Columbia is one of the world\'s most important centers of research.',
    website: 'https://www.columbia.edu'
  },
  {
    name: 'University of California, Berkeley',
    location: 'Berkeley, CA, USA',
    ranking: 18,
    description: 'Berkeley is known for both its academic excellence and its political activism.',
    website: 'https://www.berkeley.edu'
  },
  {
    name: 'Cornell University',
    location: 'Ithaca, NY, USA',
    ranking: 19,
    description: 'Cornell is known for its broadly diverse and academically comprehensive programs.',
    website: 'https://www.cornell.edu'
  },
  {
    name: 'Australian National University',
    location: 'Canberra, Australia',
    ranking: 20,
    description: 'ANU is Australia\'s leading university with a focus on research excellence.',
    website: 'https://www.anu.edu.au'
  },
  {
    name: 'University College London',
    location: 'London, UK',
    ranking: 21,
    description: 'UCL is London\'s leading multidisciplinary university with a global reputation.',
    website: 'https://www.ucl.ac.uk'
  },
  {
    name: 'University of Michigan',
    location: 'Ann Arbor, MI, USA',
    ranking: 22,
    description: 'Michigan is one of the largest research universities in the United States.',
    website: 'https://umich.edu'
  },
  {
    name: 'Peking University',
    location: 'Beijing, China',
    ranking: 23,
    description: 'PKU is one of the oldest and most prestigious universities in China.',
    website: 'https://www.pku.edu.cn'
  },
  {
    name: 'Seoul National University',
    location: 'Seoul, South Korea',
    ranking: 24,
    description: 'SNU is considered the most prestigious university in South Korea.',
    website: 'https://www.snu.ac.kr'
  },
  {
    name: 'University of California, Los Angeles',
    location: 'Los Angeles, CA, USA',
    ranking: 25,
    description: 'UCLA is known for its academic excellence and highly competitive admissions.',
    website: 'https://www.ucla.edu'
  },
  {
    name: 'Indian Institute of Technology Bombay',
    location: 'Mumbai, India',
    ranking: 26,
    description: 'IIT Bombay is India\'s premier engineering institution known for technical education.',
    website: 'https://www.iitb.ac.in'
  },
  {
    name: 'University of Edinburgh',
    location: 'Edinburgh, UK',
    ranking: 27,
    description: 'Edinburgh is one of the world\'s top universities with a rich history of innovation.',
    website: 'https://www.ed.ac.uk'
  },
  {
    name: 'McGill University',
    location: 'Montreal, Canada',
    ranking: 28,
    description: 'McGill is consistently ranked as the top university in Canada with a global focus.',
    website: 'https://www.mcgill.ca'
  },
  {
    name: 'Technical University of Munich',
    location: 'Munich, Germany',
    ranking: 29,
    description: 'TUM is Germany\'s top-ranked technical university with cutting-edge research.',
    website: 'https://www.tum.de'
  },
  {
    name: 'University of Hong Kong',
    location: 'Hong Kong',
    ranking: 30,
    description: 'HKU is the oldest tertiary institution in Hong Kong with an international outlook.',
    website: 'https://www.hku.hk'
  },
  {
    name: 'University of Melbourne',
    location: 'Melbourne, Australia',
    ranking: 31,
    description: 'Melbourne is Australia\'s second oldest university and highly regarded worldwide.',
    website: 'https://www.unimelb.edu.au'
  },
  {
    name: 'Northwestern University',
    location: 'Evanston, IL, USA',
    ranking: 32,
    description: 'Northwestern is known for its research output and interdisciplinary approach.',
    website: 'https://www.northwestern.edu'
  },
  {
    name: 'University of British Columbia',
    location: 'Vancouver, Canada',
    ranking: 33,
    description: 'UBC is a global center for research and teaching with a beautiful campus.',
    website: 'https://www.ubc.ca'
  },
  {
    name: 'Nanyang Technological University',
    location: 'Singapore',
    ranking: 34,
    description: 'NTU Singapore is known for excellence in engineering and technology education.',
    website: 'https://www.ntu.edu.sg'
  },
  {
    name: 'London School of Economics and Political Science',
    location: 'London, UK',
    ranking: 35,
    description: 'LSE specializes in social sciences and is renowned for its academic excellence.',
    website: 'https://www.lse.ac.uk'
  }
];

const users = [
  {
    name: 'Admin User',
    email: 'admin@example.com',
    password: 'password123',
    role: 'admin'
  },
  {
    name: 'Regular User',
    email: 'user@example.com',
    password: 'password123',
    role: 'user'
  }
];

// Comprehensive program list with various fields of study
const programTemplates = [
  // STEM Programs
  { name: 'Computer Science', duration: '4 years', degreeType: 'BSc' },
  { name: 'Computer Science', duration: '2 years', degreeType: 'MSc' },
  { name: 'Computer Science', duration: '4-5 years', degreeType: 'PhD' },
  { name: 'Software Engineering', duration: '4 years', degreeType: 'BSc' },
  { name: 'Data Science', duration: '2 years', degreeType: 'MSc' },
  { name: 'Artificial Intelligence', duration: '2 years', degreeType: 'MSc' },
  { name: 'Cybersecurity', duration: '2 years', degreeType: 'MSc' },
  { name: 'Mechanical Engineering', duration: '4 years', degreeType: 'BEng' },
  { name: 'Electrical Engineering', duration: '4 years', degreeType: 'BEng' },
  { name: 'Civil Engineering', duration: '4 years', degreeType: 'BEng' },
  { name: 'Aerospace Engineering', duration: '4 years', degreeType: 'BEng' },
  { name: 'Biomedical Engineering', duration: '4 years', degreeType: 'BEng' },
  { name: 'Chemical Engineering', duration: '4 years', degreeType: 'BEng' },
  { name: 'Quantum Computing', duration: '2 years', degreeType: 'MSc' },
  { name: 'Physics', duration: '3 years', degreeType: 'BSc' },
  { name: 'Mathematics', duration: '3 years', degreeType: 'BSc' },
  { name: 'Statistics', duration: '3 years', degreeType: 'BSc' },
  
  // Business Programs
  { name: 'Business Administration', duration: '4 years', degreeType: 'BBA' },
  { name: 'Business Administration', duration: '2 years', degreeType: 'MBA' },
  { name: 'Finance', duration: '3 years', degreeType: 'BSc' },
  { name: 'Marketing', duration: '3 years', degreeType: 'BSc' },
  { name: 'Entrepreneurship', duration: '1 year', degreeType: 'MSc' },
  { name: 'International Business', duration: '1 year', degreeType: 'MSc' },
  { name: 'Accounting', duration: '3 years', degreeType: 'BSc' },
  { name: 'Economics', duration: '3 years', degreeType: 'BSc' },
  { name: 'Economics', duration: '2 years', degreeType: 'MSc' },
  
  // Healthcare Programs
  { name: 'Medicine', duration: '5-6 years', degreeType: 'MD' },
  { name: 'Nursing', duration: '4 years', degreeType: 'BSN' },
  { name: 'Pharmacy', duration: '4 years', degreeType: 'PharmD' },
  { name: 'Public Health', duration: '2 years', degreeType: 'MPH' },
  { name: 'Dentistry', duration: '5 years', degreeType: 'DDS' },
  { name: 'Psychology', duration: '3 years', degreeType: 'BSc' },
  { name: 'Neuroscience', duration: '4 years', degreeType: 'BSc' },
  
  // Arts and Humanities
  { name: 'English Literature', duration: '3 years', degreeType: 'BA' },
  { name: 'History', duration: '3 years', degreeType: 'BA' },
  { name: 'Philosophy', duration: '3 years', degreeType: 'BA' },
  { name: 'Linguistics', duration: '3 years', degreeType: 'BA' },
  { name: 'Fine Arts', duration: '4 years', degreeType: 'BFA' },
  { name: 'Music', duration: '4 years', degreeType: 'BMus' },
  { name: 'Film Studies', duration: '3 years', degreeType: 'BA' },
  
  // Social Sciences
  { name: 'Political Science', duration: '3 years', degreeType: 'BA' },
  { name: 'International Relations', duration: '3 years', degreeType: 'BA' },
  { name: 'Sociology', duration: '3 years', degreeType: 'BA' },
  { name: 'Anthropology', duration: '3 years', degreeType: 'BA' },
  { name: 'Geography', duration: '3 years', degreeType: 'BSc' },
  { name: 'Urban Planning', duration: '2 years', degreeType: 'MSc' },
  
  // Law and Policy
  { name: 'Law', duration: '3 years', degreeType: 'LLB' },
  { name: 'International Law', duration: '1 year', degreeType: 'LLM' },
  { name: 'Public Policy', duration: '2 years', degreeType: 'MPP' },
  
  // Environmental Studies
  { name: 'Environmental Science', duration: '3 years', degreeType: 'BSc' },
  { name: 'Sustainability', duration: '2 years', degreeType: 'MSc' },
  { name: 'Marine Biology', duration: '3 years', degreeType: 'BSc' },
  
  // Education
  { name: 'Education', duration: '4 years', degreeType: 'BEd' },
  { name: 'Educational Leadership', duration: '2 years', degreeType: 'MEd' }
];

// Function to seed data
const seedDatabase = async () => {
  try {
    // Connect to MongoDB
    await connectDB();
    
    // Clear existing data
    await University.deleteMany({});
    await Program.deleteMany({});
    await User.deleteMany({});
    await Review.deleteMany({});
    
    console.log('✅ Database cleared');
    
    // Insert users
    const createdUsers = await User.create(users);
    console.log(`✅ ${createdUsers.length} users created`);
    
    // Insert universities
    const createdUniversities = await University.create(universities);
    console.log(`✅ ${createdUniversities.length} universities created`);
    
    // Create programs for each university
    const allPrograms = [];
    
    // Assign a variable number of programs to each university
    for (const university of createdUniversities) {
      // Select a random number of programs for each university (between 3-8)
      const numPrograms = Math.floor(Math.random() * 6) + 3;
      
      // Randomly select programs from the template list
      const shuffledPrograms = [...programTemplates]
        .sort(() => 0.5 - Math.random())
        .slice(0, numPrograms);
      
      const uniPrograms = shuffledPrograms.map(program => ({
        ...program,
        university: university._id
      }));
      
      allPrograms.push(...uniPrograms);
      
      // Add programs to university
      const createdPrograms = await Program.create(uniPrograms);
      await University.findByIdAndUpdate(
        university._id,
        { $push: { programs: { $each: createdPrograms.map(p => p._id) } } }
      );
    }
    
    console.log(`✅ ${allPrograms.length} programs created across ${createdUniversities.length} universities`);
    
    // Create reviews
    const reviews = [];
    for (const university of createdUniversities) {
      for (const user of createdUsers) {
        reviews.push({
          university: university._id,
          user: user._id,
          rating: Math.floor(Math.random() * 5) + 1,
          comment: `This is a review for ${university.name} by ${user.name}`
        });
      }
    }
    
    const createdReviews = await Review.create(reviews);
    console.log(`✅ ${createdReviews.length} reviews created`);
    
    console.log('✅ Database seeded successfully!');
    process.exit(0);
  } catch (error) {
    console.error('❌ Error seeding database:', error);
    process.exit(1);
  }
};

// Run the seed function
seedDatabase();