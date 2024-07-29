import { useState } from 'react';
import './NewPreferencePopup.css';

const NewPreferencePopup = ({ newPreference, handleNewPreferenceChange, handleNewPreferenceSubmit, handleClose }) => {
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

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

  const handleSubmit = async (e) => {
    console.log("here!!!")
    e.preventDefault();
    setIsLoading(true);
    setError('');
    if (validateInput()) {
      await handleNewPreferenceSubmit(e);
    }
    setIsLoading(false);
  };

  const prefChange = (e) => {

    setError('');
    handleNewPreferenceChange(e)
  }

  return (
    <div className="popup-overlay">
      <div className="popup">
        <h3>
            Request a groupchat that sends alerts when
            {newPreference.length === 0 ? 
                "..." : 
                ` "${newPreference.length > 35 ? newPreference.slice(0, 35) + '...' : newPreference}" `
            }
            is present in a Yale dining menu.
        </h3>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Enter Term"
            value={newPreference}
            onChange={prefChange}
          />
          <p className="error-message">{error}</p>
          <button type="submit" disabled={isLoading}>Request</button>
          <button type="button" onClick={handleClose} disabled={isLoading}>Cancel</button>
        </form>
      </div>
    </div>
  );
};

export default NewPreferencePopup;
