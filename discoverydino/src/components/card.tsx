/* eslint-disable @next/next/no-img-element */
'use client';
import React, { useEffect, useRef, useState } from 'react';

interface Review {
  content: string;
}

interface CardProps {
  heading: string;
  photoUrl: string;
  description: string;
  rating: number;
  similarProducts: string[];
  contactMail: string;
  website: string;
  category: string[];
  additionalInfo?: string; // Make additionalInfo optional
  reviews: Review[];
}

const generateStars = (rating: number): string => {
  const filledStars = '★'.repeat(Math.floor(rating));
  const halfStar = rating % 1 !== 0 ? '½' : '';
  const emptyStars = '☆'.repeat(Math.floor(5 - rating));
  return filledStars + halfStar + emptyStars;
};

const truncateUrl = (url: string, maxLength: number): string => {
  return url.length > maxLength ? `${url.substring(0, maxLength)}...` : url;
};

const Card: React.FC<CardProps> = ({
  heading,
  photoUrl,
  description,
  rating,
  similarProducts,
  contactMail,
  website,
  category,
  additionalInfo,
  reviews,
}) => {
  const [expanded, setExpanded] = useState(false);
  // const [showMoreInfo, setShowMoreInfo] = useState(false);
  const [showPopup, setShowPopup] = useState(false);
  const popupRef = useRef<HTMLDivElement>(null);

  const handleKnowMoreClick = () => {
    setShowPopup(true);
  };

  const handleClosePopup = () => {
    console.log('Closing');
    setShowPopup(!showPopup);
  };

  const handleToggleMoreInfo = () => {
    setShowPopup(!showPopup);
  };

  const toggleExpand = () => {
    setExpanded(!expanded);
  };

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        popupRef.current &&
        !popupRef.current.contains(event.target as Node)
      ) {
        setShowPopup(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);
  // Limiting description length for the card view
  const limitedDescription =
    description.length > 100
      ? `${description.substring(0, 100)}...`
      : description;

  const truncatedWebsite = truncateUrl(website, 30); // Truncate website URL to 30 characters
  const limitedAdditionalInfo = expanded
    ? additionalInfo
    : additionalInfo?.slice(0, 200) || '';

  return (
    <div className="relative cursor-pointer" onClick={handleKnowMoreClick}>
      <div className="bg-white rounded-lg p-4 max-w-sm mx-auto h-full w-full md:max-w-md lg:max-w-lg shadow-xl transform transition-transform duration-300 hover:shadow-2xl hover:scale-105 border-2 border-zinc-200">
        <div className="flex items-center">
          <img
            src={photoUrl}
            alt={heading}
            className=" object-contain w-14 h-14 border-2  rounded-lg mr-2"
          />
          <h2 className="text-xl font-semibold text-balance">{heading}</h2>
        </div>
        <p
          className="text-gray-600 text-sm my-2"
          style={{ wordWrap: 'break-word' }}
        >
          {limitedDescription}
        </p>
        <div className="w-full my-2">
          {category &&
            category.length > 0 &&
            category.map((cat, index) => (
              <button
                key={index}
                className="bg-gray-200 text-gray-700 py-1 px-1 rounded-md text-xs mr-2 gap-1"
                onClick={() => {}}
              >
                {cat}
              </button>
            ))}
        </div>
        <div className="flex justify-between">
          {/* <button
            onClick={handleKnowMoreClick}
            className="bg-white text-zinc-800 py-2 px-4 rounded-lg text-sm hover:bg-orange-400 transition-colors duration-200 border-orange-300 border"
          >
            Know More
          </button> */}
          {/* <button
            onClick={handleKnowMoreClick}
            className="bg-orange-400 text-white py-2 px-4 rounded-full text-sm hover:bg-orange-600 transition-colors duration-200"
          >
            Contact
          </button> */}
        </div>
      </div>

      {showPopup && (
        <div className="fixed top-0 bottom-0 left-0 right-0 flex justify-center items-center z-50 bg-black bg-opacity-75">
          <div
            ref={popupRef}
            className="bg-white p-8 rounded-lg max-w-3xl w-full overflow-y-auto"
            style={{ maxHeight: '90vh' }}
          >
            <div className="flex flex-col justify-between h-full">
              <div>
                <div className="flex justify-between items-start mb-6">
                  <h2 className="text-3xl font-semibold">{heading}</h2>
                  {/* <button
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
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M6 18L18 6M6 6l12 12"
                      />
                    </svg>
                  </button> */}
                </div>
                <div className="flex space-x-2">
                  <div>
                    <img
                      src={photoUrl}
                      alt={heading}
                      className="w-40 h-40 object-contain rounded-lg mb-4 border-2"
                    />
                  </div>
                  <div>
                    <p className="text-gray-600 mb-4">
                      Rating:{' '}
                      <span className="text-orange-500">
                        {generateStars(rating)} ({rating})
                      </span>
                    </p>
                    {/* <p className="text-gray-600 mb-4">Similar Products:</p>
                    <ul className="list-disc pl-4">
                      {similarProducts.map((product, index) => (
                        <li key={index}>{product}</li>
                      ))}
                    </ul> */}
                    <p className="text-gray-600">Categories:</p>
                    <div className="w-full my-2">
                      {category &&
                        category.length > 0 &&
                        category.map((cat, index) => (
                          <button
                            key={index}
                            className="bg-gray-200 text-gray-700 py-1 px-1 rounded-md text-xs mr-2 gap-1"
                            onClick={() => {}}
                          >
                            {cat}
                          </button>
                        ))}
                    </div>
                    {/* <br /> */}
                    {/* <p className="text-gray-600 mb-4">
                      Contact Mail: {contactMail}
                    </p> */}
                    <div className="flex gap-2">
                      <p className="text-gray-600 mb-4">Website: </p>
                      <a
                        href={website} // Set the 'href' attribute to the website URL
                        target="_blank" // Open the link in a new tab/window
                        rel="noopener noreferrer" // Recommended security attributes for external links
                        className="text-gray-600 mb-4 underline hover:text-blue-600 focus:text-blue-600 transition-colors duration-200"
                      >
                        {' '}
                        {truncatedWebsite}
                      </a>
                    </div>
                  </div>
                </div>

                <div>
                  <p className="text-gray-500 text-sm mb-4">
                    {additionalInfo && (
                      <div>
                        <p className="text-gray-600 text-xl mt-4 mb-2">
                          Additional Information:
                        </p>
                        <p className="text-gray-500 text-sm mb-4">
                          {expanded
                            ? additionalInfo
                            : additionalInfo.slice(0, 200)}
                          {additionalInfo.length > 200 && (
                            <span
                              className="text-blue-600 cursor-pointer"
                              onClick={toggleExpand}
                            >
                              {expanded ? ' Know Less' : ' Know More'}
                            </span>
                          )}
                        </p>
                      </div>
                    )}
                  </p>
                </div>
                {/* Render Reviews if available */}
                {reviews.length > 0 && (
                  <div>
                    <p className="text-gray-600 text-xl mt-4 mb-2">Reviews:</p>
                    <ul className="text-gray-500 text-sm list-disc pl-4 space-y-2">
                      {reviews.map((review, index) => (
                        <li key={index}>{review.content}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Card;
