import React from 'react';

const GeneratedImage = ({ imageUrl }) => (
  <div>
    {imageUrl && <img src={`http://localhost:8000/${imageUrl}`} alt="Generated Background" />}
  </div>
);

export default GeneratedImage;
