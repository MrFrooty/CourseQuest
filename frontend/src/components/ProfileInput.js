import React, { useState } from 'react';
import axios from 'axios';

const ProfileInput = ({ setProfileData }) => {
  const [url, setUrl] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await axios.post('http://localhost:8000/scrape/', { linkedin_url: url });
    setProfileData(response.data.data);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="Enter LinkedIn profile URL"
      />
      <button type="submit">Scrape Profile</button>
    </form>
  );
};

export default ProfileInput;
