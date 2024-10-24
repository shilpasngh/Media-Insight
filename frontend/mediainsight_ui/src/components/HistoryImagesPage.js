import React from 'react';
import { useParams } from 'react-router-dom';

function HistoryImagesPage() {
  const { taskId } = useParams();

  return (
    <div>
      <h1>History Images for Task {taskId}</h1>
      {/* traverse MongoDB for the taskId, and generate a gallery of history images */}
      
      
    </div>
  );
}

export default HistoryImagesPage;
