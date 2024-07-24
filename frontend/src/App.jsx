import { useState, useEffect } from 'react';
import Pref from './Pref';
import NewPreferencePopup from './NewPreferencePopup';
import './App.css';
import './Pref.css';

const App = () => {
  const [preferences, setPreferences] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [newPreference, setNewPreference] = useState('');
  const [showPopup, setShowPopup] = useState(false);

  useEffect(() => {
    fetchPreferences();
  }, []);

  const fetchPreferences = async () => {
    try {
      const response = await fetch('https://yalefoodfinder.com/api/prefs/');
      const data = await response.json();
      setPreferences(data);
    } catch (error) {
      console.error('Error fetching preferences:', error);
    }
  };

  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
  };

  const handleNewPreferenceChange = (e) => {
    setNewPreference(e.target.value);
  };

  const handleNewPreferenceSubmit = async (e) => {
    e.preventDefault();
    if (newPreference.trim() === '') return;

    const confirmationMessage = `Are you sure you want to request the creation of a food finder groupchat for "${newPreference}"?`;
    if (!window.confirm(confirmationMessage)) return;

    try {
      const response = await fetch('https://yalefoodfinder.com/api/prefs/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ pref_string: newPreference }),
      });

      if (response.ok) {
        fetchPreferences(); // Refresh the list
        setNewPreference(''); // Clear the input field
        setShowPopup(false); // Close the popup
      } else {
        console.error('Error adding new preference');
      }
    } catch (error) {
      console.error('Error adding new preference:', error);
    }
  };

  const filteredPreferences = preferences.filter((pref) =>
    pref.pref_string.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="App">
      <h1>Yale Food Finder</h1>

      <div className="search-container">
        <input
          type="text"
          placeholder="Search Groupchats"
          value={searchTerm}
          onChange={handleSearchChange}
        />
      </div>

      <button onClick={() => setShowPopup(true)}>Request New Groupchat</button>

      <div className="preferences-list">
        {filteredPreferences.map((pref, index) => (
          <Pref key={index} pref_string={pref.pref_string} groupchat_url={pref.groupchat_url} />
        ))}
      </div>

      {showPopup && (
        <NewPreferencePopup
          newPreference={newPreference}
          handleNewPreferenceChange={handleNewPreferenceChange}
          handleNewPreferenceSubmit={handleNewPreferenceSubmit}
          handleClose={() => setShowPopup(false)}
        />
      )}
    </div>
  );
};

export default App;
