### Image Caption Generator

This project is a web application that generates captions for uploaded images using a machine learning model. It includes:

A Flask backend that processes images and generates captions using a pre-trained BLIP model.
A React frontend that provides a user interface for uploading images and displaying captions.

### Project Structure

Image_Caption_Generator/
│
├── frontend/ # React frontend
│ ├── node_modules/ # Node dependencies
│ ├── public/ # Public assets (HTML, etc.)
│ ├── src/ # React components and code
│ ├── .gitignore # Files to ignore in version control
│ ├── package.json # Node.js dependencies for React app
│ ├── package-lock.json # Lock file for Node.js dependencies
│ └── README.md # Frontend instructions
│
├── app.py # Flask backend code
├── requirements.txt # Python dependencies for Flask backend
└── README.md # Main project instructions

### Prerequisites

Python 3.8+
Node.js and npm

### Setup Instructions

Step 1: Set Up the Backend (Flask)

1. Install Python dependencies:

   - Open a terminal in the project root directory (where app.py is located) and run:
     pip install -r requirements.txt

2. Run the Flask server:
   - Start the Flask backend server by running:
     python app.py

Step 2: Set Up the Frontend (React)

1. Create a React App:

   - Navigate to your project folder in the terminal.
   - Use the following command to create a React app named frontend
     npx create-react-app frontend
     cd frontend
     npm install
     npm start

   This will start the React frontend on http://localhost:3000

### Accessing the Application

- Open a browser and go to http://localhost:3000.
- Use the interface to upload an image and view the generated caption.

### Testing the Backend with Curl Command

curl -X POST -F "file=@path_to_your_image" http://localhost:5000/generate-caption
