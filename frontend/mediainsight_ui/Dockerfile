# Use the official Node.js image as a base image
FROM node:20-alpine

# Set the working directory
WORKDIR /usr/src/app

# Copy the package.json and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the application code
COPY public /usr/src/app/public
COPY src /usr/src/app/src


# Expose the port that React runs on
EXPOSE 3000

# Start the React application
CMD ["npm", "start"]
