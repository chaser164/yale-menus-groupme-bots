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
  const [notification, setNotification] = useState('');
  const [isVisible, setIsVisible] = useState(true);
  const [isFading, setIsFading] = useState(false);

  useEffect(() => {
    fetchPreferences();
  }, []);

  useEffect(() => {
    if (!notification) {
      return;
    }

    // allow for message visibility
    setIsVisible(true);
    setIsFading(false);

    const timer1 = setTimeout(() => {
      setIsVisible(false);
      setIsFading(true);
    }, 2000); // Wait 2 seconds before starting the fade-out

    const timer2 = setTimeout(() => {
      setNotification("");
    }, 3000); // Wait 4 seconds before setting the message to an empty string

    return () => {
      clearTimeout(timer1);
      clearTimeout(timer2);
    };
  }, [notification]);

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
    setNewPreference(e.target.value.toLowerCase());
  };

  const handleNewPreferenceSubmit = async (e) => {
    e.preventDefault();
    if (newPreference.trim() === '') return;

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
        setNotification("Groupchat created!")
      } else {
        setNotification("Error generating groupchat.")
        console.error('Error generating groupchat.');
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
      <p className='info'>
        Join groupchats to get notified about when and where Yale dining is serving certain foods.
        Request the creation of new groupchats with the button below.
      </p>

      <button onClick={() => setShowPopup(true)}>Request New Groupchat</button>

      <div className="search-container">
        <input
          type="text"
          placeholder="Search Groupchats"
          value={searchTerm}
          onChange={handleSearchChange}
        />
      </div>

      <p className={`${isFading ? 'fade-out' : ''} notification ${!isVisible ? 'hidden' : ''}`}>
        {notification}
      </p>

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
