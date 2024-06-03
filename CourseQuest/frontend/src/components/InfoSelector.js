import React from 'react';

const InfoSelector = ({ profileData, selectedInfo, setSelectedInfo }) => {
  const handleChange = (key, value) => {
    setSelectedInfo({ ...selectedInfo, [key]: value });
  };

  return (
    <div>
      <h3>Select Information to Include</h3>
      {Object.keys(profileData).map((key) => (
        <div key={key}>
          <label>
            {key}
            <input
              type="checkbox"
              checked={selectedInfo[key] || false}
              onChange={(e) => handleChange(key, e.target.checked)}
            />
          </label>
        </div>
      ))}
    </div>
  );
};

export default InfoSelector;
