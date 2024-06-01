import React, { useState } from 'react';
import ProfileInput from './ProfileInput';
import InfoSelector from './InfoSelector';
import GeneratedImage from './GeneratedImage';
import axios from 'axios';

const App = () => {
  const [profileData, setProfileData] = useState(null);
  const [selectedInfo, setSelectedInfo] = useState({});
  const [imageUrl, setImageUrl] = useState('');

  const generateImage = async () => {
    console.log('Generating image')
    const response = await axios.post('http://localhost:8000/generate/', {
      linkedin_url: 'placeholder', // Adjust as needed
      selected_info: selectedInfo
    });
    setImageUrl(response.data.image);
  };

  return (
    <div>
      <h1>LinkedIn Background Generator</h1>
      <ProfileInput setProfileData={setProfileData} />
      {profileData && (
        <>
          <InfoSelector
            profileData={profileData}
            selectedInfo={selectedInfo}
            setSelectedInfo={setSelectedInfo}
          />
          <button onClick={generateImage}>Generate Image</button>
        </>
      )}
      <GeneratedImage imageUrl={imageUrl} />
    </div>
  );
};

export default App;
