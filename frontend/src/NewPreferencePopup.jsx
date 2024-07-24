import React, { useState } from 'react';
import './NewPreferencePopup.css';

const NewPreferencePopup = ({ newPreference, handleNewPreferenceChange, handleNewPreferenceSubmit, handleClose }) => {
  const [error, setError] = useState('');

  const validateInput = () => {
    if (newPreference.trim() === '') {
      setError('Term cannot be empty.');
      return false;
    }
    if (newPreference.length > 35) {
      setError('Term must be 35 characters or less.');
      return false;
    }
    setError('');
    return true;
  };

  const handleSubmit = (e) => {
    setError('');
    e.preventDefault();
    if (validateInput()) {
      handleNewPreferenceSubmit(e);
    }
  };

  const prefChange = (e) => {

    setError('');
    handleNewPreferenceChange(e)
  }

  return (
    <div className="popup-overlay">
      <div className="popup">
        <h3>
            Request a groupchat that finds 
            {newPreference.length === 0 ? 
                "..." : 
                ` "${newPreference.length > 35 ? newPreference.slice(0, 35) + '...' : newPreference}"`
            }
        </h3>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Enter Term"
            value={newPreference}
            onChange={prefChange}
          />
          <p className="error-message">{error}</p>
          <button type="submit">Request</button>
          <button type="button" onClick={handleClose}>Cancel</button>
        </form>
      </div>
    </div>
  );
};

export default NewPreferencePopup;
