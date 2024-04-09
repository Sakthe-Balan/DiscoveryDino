"use client"
import React, { useState } from 'react';

interface CardProps {
  heading: string;
  photoUrl: string;
  description: string;
  rating: number;
  similarProducts: string[];
  contactMail: string;
  website: string;
}

const generateStars = (rating: number): string => {
  const filledStars = '★'.repeat(Math.floor(rating));
  const halfStar = rating % 1 !== 0 ? '½' : '';
  const emptyStars = '☆'.repeat(Math.floor(5 - rating));
  return filledStars + halfStar + emptyStars;
};

const Card: React.FC<CardProps> = ({
  heading,
  photoUrl,
  description,
  rating,
  similarProducts,
  contactMail,
  website,
}) => {
  const [showPopup, setShowPopup] = useState(false);

  const handleKnowMoreClick = () => {
    setShowPopup(true);
  };

  const handleClosePopup = () => {
    setShowPopup(false);
  };

  // Limiting description length for the card view
  const limitedDescription =
    description.length > 100 ? `${description.substring(0, 100)}...` : description;

  return (
    <div className="relative">
      <div className="bg-white rounded-lg p-6 max-w-sm mx-auto min-h-64 w-full md:max-w-md lg:max-w-lg shadow-xl transform transition-transform duration-300 hover:shadow-2xl hover:scale-105 border-2 border-zinc-200">
        <img src={photoUrl} alt={heading} className="w-full h-48 object-cover rounded-lg mb-4" />
        <h2 className="text-xl font-semibold mb-2">{heading}</h2>
        <p className="text-gray-600 mb-4" style={{ wordWrap: 'break-word' }}>
          {limitedDescription}
        </p>
        <button
          onClick={handleKnowMoreClick}
          className="bg-orange-500 text-white py-2 px-4 rounded-lg hover:bg-orange-600 transition-colors duration-200"
        >
          Know More
        </button>
      </div>

      {showPopup && (
  <div className="fixed top-0 bottom-0 left-0 right-0 flex justify-center items-center z-50 bg-black bg-opacity-75">
    <div className="bg-white p-8 rounded-lg max-w-3xl w-full overflow-y-auto" style={{ maxHeight: '90vh' }}>
      <div className="flex flex-col justify-between h-full">
        <div>
          <div className="flex justify-between items-start mb-6">
            <h2 className="text-3xl font-semibold">{heading}</h2>
            <button
              onClick={handleClosePopup}
              className="text-gray-500 hover:text-gray-700 focus:outline-none"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <img src={photoUrl} alt={heading} className="w-full h-80 object-cover rounded-lg mb-4" />

              <p className="text-gray-600 mb-4">
                Rating: <span className="text-orange-500">{generateStars(rating)} ({rating})</span>
              </p>
              <p className="text-gray-600 mb-4">Similar Products:</p>
              <ul className="list-disc pl-4">
                {similarProducts.map((product, index) => (
                  <li key={index}>{product}</li>
                ))}
              </ul>
              <br />
              <p className="text-gray-600 mb-4">Contact Mail: {contactMail}</p>
              <p className="text-gray-600 mb-4">Website: {website}</p>
            </div>
            <div>
              <p className="text-gray-600 mb-4">Description:</p>
              <p className="text-gray-600 mb-4" style={{ wordWrap: 'break-word' }}>
                {description}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
)}

    </div>
  );
};

export default Card;
