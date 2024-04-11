'use client';
import React, { useState, useEffect } from 'react';

interface Category {
  name: string;
}

interface FilterProps {
  selectedRatings: number[];
  setSelectedRatings: React.Dispatch<React.SetStateAction<number[]>>;
  selectedCategory: string | null;
  setSelectedCategory: React.Dispatch<React.SetStateAction<string | null>>;
}

const Filter: React.FC<FilterProps> = ({
  selectedRatings,
  setSelectedRatings,
  selectedCategory,
  setSelectedCategory,
}) => {
  // const [selectedRatings, setSelectedRatings] = useState<number[]>([]);
  // const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [showAllCategories, setShowAllCategories] = useState<boolean>(false);
  const [isFilterVisible, setIsFilterVisible] = useState<boolean>(false);
  const [isMobileView, setIsMobileView] = useState<boolean>(false);

  useEffect(() => {
    const handleResize = () => {
      setIsMobileView(window.innerWidth <= 768); // Assuming 768px as the breakpoint for mobile view
      setIsFilterVisible(window.innerWidth >= 768); // Adjust this value based on your breakpoint
    };

    window.addEventListener('resize', handleResize);
    handleResize(); // Initial check

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  const categories: Category[] = [
    { name: 'Sales Tools' },
    { name: 'Marketing' },
    { name: 'Analytics Tools & Software' },
    { name: 'Artificial Intelligence' },
    { name: 'AR/VR' },
    { name: 'B2B Marketplaces' },
    { name: 'Business Services' },
    { name: 'CAD & PLM' },
    { name: 'Collaboration & Productivity' },
    { name: 'Commerce' },
    { name: 'Content Management' },
    { name: 'Converged Infrastructure' },
    { name: 'Customer Service' },
    { name: 'Data Privacy' },
    { name: 'Design' },
    { name: 'Development' },
    { name: 'Digital Advertising Tech' },
    { name: 'Ecosystem Service Providers' },
    { name: 'ERP' },
    { name: 'Governance, Risk & Compliance' },
    { name: 'Greentech' },
    { name: 'Hosting' },
    { name: 'HR' },
    { name: 'IoT Management' },
    { name: 'IT Infrastructure' },
    { name: 'IT Management' },
    { name: 'Marketing Services' },
    { name: 'Marketplace Apps' },
    { name: 'Office' },
    { name: 'Other Services' },
    { name: 'Professional Services' },
    { name: 'Routers' },
    { name: 'Security' },
  ];

  const handleRatingChange = (rating: number) => {
    setSelectedRatings((prev) => {
      if (prev.includes(rating)) {
        console.log(`Deselected rating: ${rating}`);
        return [];
      } else {
        console.log(`Selected rating: ${rating}`);
        return [rating];
      }
    });
  };

  const handleCategoryChange = (categoryName: string) => {
    setSelectedCategory((prevCategory) => {
      if (prevCategory === categoryName) {
        console.log(`Deselected category: ${categoryName}`);
        return null;
      } else {
        console.log(`Selected category: ${categoryName}`);
        return prevCategory === categoryName ? null : categoryName;
      }
    });
  };

  const toggleShowCategories = () => {
    setShowAllCategories((prev) => !prev);
  };

  const renderStar = (index: number, rating: number) => {
    if (index < rating) {
      return (
        <span
          key={index}
          className="text-orange-500 text-lg cursor-pointer"
          onClick={() => handleRatingChange(rating)}
        >
          ★
        </span>
      );
    } else {
      return (
        <span
          key={index}
          className="text-gray-400 text-lg cursor-pointer"
          onClick={() => handleRatingChange(rating)}
        >
          ☆
        </span>
      );
    }
  };

  const visibleCategories = showAllCategories
    ? categories
    : categories.slice(0, 3);

  return (
    <div className="relative">
      {isMobileView && (
        <button
          className="absolute top-0 right-0 mt-4 mr-5 bg-orange-500 text-white px-4 py-2 rounded-md"
          onClick={() => setIsFilterVisible((prev) => !prev)}
        >
          {isFilterVisible ? '' : 'Show Filter'}
        </button>
      )}
      {isFilterVisible && (
        <div
          className="absolute top-full mt-4 left-4 bg-white p-4 pt-1 rounded-lg shadow-md z-10 border-2"
          style={{ width: '250px' }}
        >
          <h2 className="text-lg font-semibold mb-4 text-center py-2 rounded-md">
            Filter
          </h2>
          {isMobileView && (
            <button
              className="absolute top-0 right-0 mt-2 mr-2 bg-orange-500 text-white px-2 py-1 rounded-md"
              onClick={() => setIsFilterVisible(false)}
            >
              ✕
            </button>
          )}
          <div className="mb-4">
            <h3 className="text-sm font-medium mb-2 border-b-2 border-gray-200 pb-2">
              Based on Star Rating
            </h3>
            <div className="flex flex-col space-y-2">
              {[1, 2, 3, 4, 5].map((rating) => (
                <label key={rating} className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    checked={selectedRatings.includes(rating)}
                    onChange={() => handleRatingChange(rating)}
                    className="form-checkbox h-4 w-4 rounded-full text-orange-500 bg-orange-100"
                  />
                  <span className="text-sm">
                    {[...Array(5)].map((_, index) => renderStar(index, rating))}
                  </span>
                </label>
              ))}
            </div>
          </div>
          <div>
            <h3 className="text-sm font-medium mb-2 border-b-2 border-gray-200 pb-2">
              Categories
            </h3>
            <div className="flex flex-col space-y-2">
              {visibleCategories.map((category) => (
                <label
                  key={category.name}
                  className="flex items-center space-x-2"
                >
                  <input
                    type="checkbox"
                    checked={selectedCategory === category.name}
                    onChange={() => handleCategoryChange(category.name)}
                    className="form-checkbox h-4 w-4 rounded-md text-orange-500 bg-orange-100"
                  />
                  <span className="text-sm">{category.name}</span>
                </label>
              ))}
            </div>
            {categories.length > 4 && (
              <button
                className="text-orange-500 text-sm mt-2"
                onClick={toggleShowCategories}
              >
                {showAllCategories
                  ? 'Show less categories'
                  : 'Show more categories'}
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default Filter;
