import React, { useState } from 'react';
import axios from 'axios';

function ImageUploader() {
    const [file, setFile] = useState(null);
    const [caption, setCaption] = useState('');
    const [loading, setLoading] = useState(false);
    const [previewUrl, setPreviewUrl] = useState(null);

    const handleFileChange = (event) => {
        const selectedFile = event.target.files[0];
        setFile(selectedFile);
        setCaption(''); // Clear caption when a new file is selected

        // Create a URL for the selected file to preview the image
        if (selectedFile) {
            setPreviewUrl(URL.createObjectURL(selectedFile));
        }
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!file) return;

        setLoading(true);
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post('http://localhost:5000/generate-caption', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            setCaption(response.data.caption);
        } catch (error) {
            console.error("Error uploading file:", error);
            setCaption('Error generating description');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ textAlign: 'center', padding: '20px' }}>
            <h2>Image Description Generator</h2>
            <form onSubmit={handleSubmit}>
                <input type="file" onChange={handleFileChange} accept="image/*" />
                <button type="submit" disabled={loading}>
                    {loading ? 'Generating Description...' : 'Upload and Generate Image Description'}
                </button>
            </form>

            {previewUrl && (
                <div style={{ marginTop: '20px' }}>
                    <h3>Uploaded Image:</h3>
                    <img src={previewUrl} alt="Preview" style={{ maxWidth: '100%', maxHeight: '400px' }} />
                </div>
            )}

            {caption && (
                <div style={{ marginTop: '20px' }}>
                    <h3>Generated Description:</h3>
                    <p>{caption}</p>
                </div>
            )}
        </div>
    );
}

export default ImageUploader;
