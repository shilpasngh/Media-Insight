import React, { useState, useEffect } from 'react';
import './App.css'; // Include CSS for overlay

function App() {
  const [summaryInput, setSummaryInput] = useState('');
  const [summary, setSummary] = useState('');
  const [summaryTaskId, setSummaryTaskId] = useState(null);
  
  const [inputText, setInputText] = useState('');
  const [imageUrl, setImageUrl] = useState(null);
  const [text2imageLoading, setText2imageLoading] = useState(false);
  const [captionLoading, setCaptionLoading] = useState(false);
  const [summaryLoading, setSummaryLoading] = useState(false);
  const [taskId, setTaskId] = useState(null);
  const [manualTaskId, setManualTaskId] = useState('');
  const [selectedImage, setSelectedImage] = useState(null); // For image upload
  const [caption, setCaption] = useState(''); // For generated caption
  const [captionTaskId, setCaptionTaskId] = useState(null); // Task ID for caption generation
  const [imageSrc, setImageSrc] = useState(null); // For displaying the uploaded image

  const [copySuccess, setCopySuccess] = useState(false);

  const handleCopy = async(text) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopySuccess(true);
      setTimeout(() => setCopySuccess(false), 2000);
    } catch (err) {
      console.error('Failed to copy text: ', err);
    }
  }

  const handleSummarySubmit = async (e) => {
    e.preventDefault();
    setSummaryLoading(true);
    setSummary('');
  
      // Make an API request to send the text input to the server
      try {
        const response = await fetch('/api/v1/summarize-text', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ 'prompt': summaryInput }),
        });
        const data = await response.json();
        setSummaryTaskId(data.task_id);
      } catch (error) {
        console.error('Error submitting text:', error);
        setSummaryLoading(false);
      }
    };
  

  const handleText2imageSubmit = async (e) => {
    e.preventDefault();
    setText2imageLoading(true);
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
    setManualTaskId(data.task_id); // Set the task ID for manual fetch
  };

  const handleManualFetch = async (e) => {
    e.preventDefault();
    setText2imageLoading(true);
    setImageUrl(null);

    try {
      const response = await fetch(`/api/v1/generate-image/${manualTaskId}`);
      const data = await response.json();

      if (data.data.image !== undefined) {
        setImageUrl(data.data.image);
      } else {
        console.error('Image not found for the given task ID');
        alert('Task ID not found');
      }
    } catch (error) {
      console.error('Error fetching image:', error);
      alert('Error fetching image');
    }

    setText2imageLoading(false);
  };

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImageSrc(reader.result); // Set the image source to the file data
      };
      reader.readAsDataURL(file); // Read the file as a data URL
    }

    setSelectedImage(file);
    setCaption(''); // Clear previous caption
  };

  const handleCaptionSubmit = async (e) => {
    e.preventDefault();
    if (!selectedImage) return;

    setCaptionLoading(true);
    setCaption(''); // Clear previous caption

    // Prepare form data to send the image to the server
    const formData = new FormData();
    formData.append('image', selectedImage);

    // Make an API request to upload the image and generate a caption
    const response = await fetch('/api/v1/generate-description', {
      method: 'POST',
      body: formData,
    });
    const data = await response.json();

    // The server returns a task ID for polling
    setCaptionTaskId(data.task_id);
  };

  // Poll the server continuously until the summary is ready
  useEffect(() => {
    if (!summaryTaskId) return;

    const interval = setInterval(async () => {
      console.log(`Polling summary for task ID ${summaryTaskId}`);
      const response = await fetch(`/api/v1/summarize-text/${summaryTaskId}`);
      const data = await response.json();

      if (data.data && data.data.summary !== undefined) {
        setSummary(data.data.summary);
        setSummaryLoading(false);
        clearInterval(interval);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [summaryTaskId]);

  // Poll the server continuously until the caption is ready
  useEffect(() => {
    if (!captionTaskId) {
      console.log('No caption task id set yet');
      return;
    }

    const interval = setInterval(async () => {
      console.log(`Polling caption for task ID ${captionTaskId}`);
      const response = await fetch(`/api/v1/generate-description/${captionTaskId}`);
      const data = await response.json();

      if (data.data && data.data.caption !== undefined && data.data.caption !== "") {
        setCaption(data.data.caption);
        setCaptionLoading(false);
        clearInterval(interval); // Stop polling when the caption is ready
        console.log(`Caption ready: ${data.data.caption}`);
      }
    }, 1000); // Poll every second

    return () => clearInterval(interval);
  }, [captionTaskId]);

  // Poll the server continuously until the image is ready
  useEffect(() => {
    if (!taskId) {
      console.log('No task id set yet');
      return;
    }

    const interval = setInterval(async () => {
      console.log(`Polling ${taskId}`);
      const response = await fetch(`/api/v1/generate-image/${taskId}`);
      const data = await response.json();

      if (data.data.image !== undefined) {
        setImageUrl(data.data.image);
        setText2imageLoading(false);
        clearInterval(interval); // Stop polling when the image is ready
        console.log(`Image ready ${data.data.image}`);
      }
    }, 1000); // Poll every second

    return () => clearInterval(interval);
  }, [taskId]);

  return (
    <div className="App">
      <div className="header">
        <h1>MediaInsight</h1>
      </div>
      <div class="container">
        {/* Text to Image Section */}
        <div className="feature-card">
          {text2imageLoading && (
            <div className="overlay">
              <div className="spinner"></div>
              <p>Processing... Please wait.</p>
            </div>
          )}
          <h2>Text to Image Generator</h2>
          <div className="input-area">
            <form onSubmit={handleText2imageSubmit}>
              <textarea
                type="text"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder="Enter text to generate image"
                required
                disabled={text2imageLoading} // Disable input when loading
                rows={3}
                cols={60}
                className="text-input"
              />
              <button className="button-primary" type="submit" disabled={text2imageLoading}>
                {text2imageLoading ? 'Generating...' : 'Generate Image'}
              </button>
            </form>
          </div>

          <h2>Fetch Image by Task ID</h2>
          <div className="input-area">
            <form onSubmit={handleManualFetch}>
              <input
                className="manual-taskid-input" 
                type="text"
                value={manualTaskId}
                onChange={(e) => setManualTaskId(e.target.value)}
                placeholder="Enter task ID"
                required
                disabled={text2imageLoading}
              />
              <button className="button-primary" type="submit" disabled={text2imageLoading}>
                Fetch Image
              </button>
            </form>
          </div>

          {imageUrl && (
            <div className="result-area">
            <img src={imageUrl} alt="Generated" className="generated-image" />
            </div>
          )}
        </div>
      
        {/* Image Caption Section */}
        <div className="feature-card">
          {captionLoading && (
            <div className="overlay">
              <div className="spinner"></div>
              <p>Processing... Please wait.</p>
            </div>
          )}
          <h2>Image Caption Generator</h2>
          <div className="input-area">
            <form onSubmit={handleCaptionSubmit}>
              <div className="file-upload-container"> 
                <input
                  type="file"
                  id="file-upload"
                  accept="image/*"
                  onChange={handleImageUpload}
                  className="file-input"
                  required
                  disabled={captionLoading}
                />
                <label htmlFor="file-upload" className="file-upload-label">
                  <div className="upload-content">
                    <span className="upload-icon">📁</span>
                    <span className="upload-text">Choose File or Drag & Drop</span>
                  </div>
                </label>
              </div>
              <button className="button-primary" type="submit" disabled={captionLoading}>
                {captionLoading ? 'Generating...' : 'Generate Caption'}
              </button>
            </form>
          </div>
          {imageSrc && (
            <div className="result-area">
              <img src={imageSrc} alt="Selected" className="preview-image" />
              {caption && <p className="caption-text">{caption}</p>}
            </div>
          )}
        </div>  

        {/* Summary Generator Section */}
        <div className="feature-card">
          {summaryLoading && (
            <div className="overlay">
              <div className="spinner"></div>
              <p>Processing... Please wait.</p>
            </div>
          )}
          <h2>Summary Generator</h2>
          <div className="input-area">
            <form onSubmit={handleSummarySubmit}>
              <textarea
                value={summaryInput}
                onChange={(e) => setSummaryInput(e.target.value)}
                placeholder="Enter text to summarize"
                required
                disabled={summaryLoading}
                className="text-input"
              />
              <button className="button-primary" type="submit" disabled={summaryLoading}>
                {summaryLoading ? 'Generating...' : 'Generate Summary'}
              </button>
            </form>
          </div>
          {summary && (
            <div className="result-area">
              <p className="summary-text">{summary}</p>
            </div>
          )}
          <button className="copy-button" onClick={() => handleCopy(summary)}>
            {copySuccess ? 'Copied!' : 'Copy'}
          </button>
        </div>  
      </div>
    </div>
  );
}

export default App;
