import React from 'react';
import './Pref.css';

const Pref = ({ pref_string, groupchat_url }) => {
  return (
    <div className="pref-card">
      <span className="pref-text">{pref_string}</span>
      <a href={groupchat_url} target="_blank" rel="noopener noreferrer" className="pref-link">Join Groupchat</a>
    </div>
  );
};

export default Pref;
