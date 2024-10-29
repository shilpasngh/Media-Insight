import React, { useState, useEffect } from 'react';
import './App.css'; // Include CSS for overlay

function App() {
  const [inputText, setInputText] = useState('');
  const [imageUrl, setImageUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [taskId, setTaskId] = useState(null);
  const [manualTaskId, setManualTaskId] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setImageUrl(null); // Clear previous image

    // Make an API request to send the text input to the server
    const response = await fetch('/api/v1/generate-image', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 'text': inputText }),
    });
    const data = await response.json();

    // The server returns a task ID for polling
    setTaskId(data.task_id);
  };

  const handleManualFetch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setImageUrl(null);

    try {
      const response = await fetch(`/api/v1/generate-image/${manualTaskId}`);
      const data = await response.json();

      if (data.data.image !== undefined) {
        setImageUrl(data.data.image);
      } else {
        console.error('Image not found for the given task ID');
        // You might want to add some user feedback here
      }
    } catch (error) {
      console.error('Error fetching image:', error);
      // You might want to add some user feedback here
    }

    setLoading(false);
  };

  // Poll the server continuously until the image is ready
  useEffect(() => {
    if (!taskId) {
      console.log('no task id set yet');
      return;
    }

    const interval = setInterval(async () => {
      console.log(`polling ${taskId}`);
      const response = await fetch(`/api/v1/generate-image/${taskId}`);
      const data = await response.json();

      if (data.data.image !== undefined) {
        setImageUrl(data.data.image);
        setLoading(false);
        clearInterval(interval); // Stop polling when the image is ready
        console.log(`image ready ${data.data.image}`);
      }
    }, 1000); // Poll every second

    return () => clearInterval(interval);
  }, [taskId]);

  return (
    <div className="App">
      {loading && (
        <div className="overlay">
          <div className="spinner"></div>
          <p>Generating Image... Please wait.</p>
        </div>
      )}
      <h1>Text to Image Generator</h1>
      <form onSubmit={handleSubmit}>
        <textarea
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Enter text to generate image"
          required
          disabled={loading} // Disable input when loading
          rows={3}
          cols={60}
          className="large-input"
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Generating...' : 'Generate Image'}
        </button>
      </form>
      
      <h2>Fetch Image by Task ID</h2>
      <form onSubmit={handleManualFetch}>
        <input
          type="text"
          value={manualTaskId}
          onChange={(e) => setManualTaskId(e.target.value)}
          placeholder="Enter task ID"
          required
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          Fetch Image
        </button>
      </form>
      
      {imageUrl && <img src={imageUrl} alt="Generated" />}
    </div>
  );
}

export default App;
