"use client"
import React from 'react';

interface CardProps {
  heading: string;
  photoUrl: string;
  description: string;
}

const Card: React.FC<CardProps> = ({ heading, photoUrl, description }) => {
  // Define the onClick handler for the "Know More" button
  const handleKnowMoreClick = () => {
    console.log('Know More clicked');
    // You can add more functionality here as needed
  };

  return (
    <div className="bg-white rounded-lg p-6 max-w-sm mx-auto min-h-64 w-full md:max-w-md lg:max-w-lg shadow-xl transform transition-transform duration-300 hover:shadow-2xl hover:scale-105"> {/* Adjusted width and added responsive classes */}
      <img src={photoUrl} alt={heading} className="w-full h-48 object-cover rounded-lg mb-4" />
      <h2 className="text-xl font-semibold mb-2">{heading}</h2>
      <p className="text-gray-600 mb-4">{description}</p>
      <button
        onClick={handleKnowMoreClick}
        className="bg-orange-500 text-white py-2 px-4 rounded-lg hover:bg-orange-600 transition-colors duration-200"
      >
        Know More
      </button>
    </div>
  );
};

export default Card;
