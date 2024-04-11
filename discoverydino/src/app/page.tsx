/* eslint-disable react-hooks/exhaustive-deps */
'use client';
import Header from '@/components/header';
import Filter from '@/components/filter';
import Card from '@/components/card';
import React, { useState, useEffect } from 'react';
import axios from 'axios';
interface CardData {
  _id: string;
  productName: string;
  photoUrl: string;
  description: string;
  rating: number;
  similarProducts: string[];
  contactMail: string;
  website: string;
  category: string[];
  additionalInfo: string;
  scarpedLink: string;
  reviews?: any[];
}

export default function Home() {
  // Provide initial data as part of the state
  const initialData: CardData[] = [];

  const [data, setData] = useState<CardData[]>(initialData);
  const [itemsToDisplay, setItemsToDisplay] = useState<number>(9);
  const [isLoading, setIsLoading] = useState(false);

  const [parentSelectedRatings, setParentSelectedRatings] = useState<number[]>(
    []
  );
  const [parentSelectedCategory, setParentSelectedCategory] = useState<
    string | null
  >(null);

  useEffect(() => {
    // Define a function to fetch filtered products based on selected ratings and category
    const fetchFilteredProducts = async () => {
      if (parentSelectedRatings.length === 0 && !parentSelectedCategory) {
        try {
          const response = await axios.get(
            `${process.env.NEXT_PUBLIC_SERVER_URL}/api/data?limit=9`
          );
          const newData = response.data;

          console.log('API Response:', newData);

          // Check if newData is an array before updating the state
          if (Array.isArray(newData)) {
            // setData((prevData) => {
            //   const existingIds = new Set(prevData.map((item) => item._id));
            //   const filteredNewData = newData.filter(
            //     (item) => !existingIds.has(item._id)
            //   );
            //   return [...prevData, ...filteredNewData];
            // });
            setData(newData);
            setItemsToDisplay(18);
            // setItemsToDisplay((prevItems) => prevItems + 9);
          }
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      } else {
        // Construct API URL based on selected ratings and category
        const queryParams = new URLSearchParams({
          collection: 'filtered_products',
        });

        if (parentSelectedRatings.length > 0) {
          queryParams.set('rating', parentSelectedRatings.join(','));
        }

        if (parentSelectedCategory) {
          queryParams.set('category', parentSelectedCategory);
        }

        const apiUrl = `${
          process.env.NEXT_PUBLIC_SERVER_URL
        }/api/filter?${queryParams.toString()}`;

        try {
          const response = await axios.get(apiUrl);
          const data = await response.data;
          setData(data.results);
          // Update state with filtered products
          console.log(data.results);
          // setData(data.results); // Assuming 'results' is the key containing filtered products
        } catch (error) {
          console.error('Error fetching filtered products:', error);
        }
      }
    };
    // Call fetchFilteredProducts whenever selected ratings or category change
    fetchFilteredProducts();
  }, [parentSelectedRatings, parentSelectedCategory]);

  const fetchData = async () => {
    setIsLoading(true); // Start loading
    try {
      console.log(`${process.env.NEXT_PUBLIC_SERVER_URL}`);

      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_SERVER_URL}/api/data?limit=${itemsToDisplay}`
      );

      // The response data is already parsed as JSON
      //  console.log(response.data);

      // Directly use response.data since it's already an object

      const newData = response.data;

      console.log('API Response:', newData);

      // Check if newData is an array before updating the state
      if (Array.isArray(newData)) {
        setData((prevData) => {
          const existingIds = new Set(prevData.map((item) => item._id));
          const filteredNewData = newData.filter(
            (item) => !existingIds.has(item._id)
          );
          return [...prevData, ...filteredNewData];
        });
        setItemsToDisplay((prevItems) => prevItems + 9);
      } else {
        console.log('out');
      }
    } catch (error) {
      console.error('Error fetching data:', error);
      // Optionally, handle the error case, such as showing an error message to the user
    } finally {
      setIsLoading(false); // End loading
    }
  };

  useEffect(() => {
    fetchData();
  }, []); // Empty dependency array means this effect runs once on mount

  const handleLoadMore = () => {
    fetchData();
  };

  return (
    <>
      <Header />
      <div className="relative mt-4 flex flex-col md:flex-row flex-grow">
        {/* Background stickers */}
        <div className="absolute top-0 right-0 bg-orange-500 h-20 w-20 rounded-full transform rotate-45"></div>
        <div className="absolute top-2 left-6 bg-yellow-500 h-12 w-12 rounded-lg transform rotate-45"></div>

        {/* Filter section */}
        <div className="w-full md:w-[20%] md:border-r sm:mr-2">
          <Filter
            selectedRatings={parentSelectedRatings}
            setSelectedRatings={setParentSelectedRatings}
            selectedCategory={parentSelectedCategory}
            setSelectedCategory={setParentSelectedCategory}
          />
        </div>

        {/* Main content section */}
        <div className="md:w-[80%] flex-grow p-4 mt-4 mx-4 border-r-4 rounded-md shadow-lg bg-white border-gray-300  relative">
          {/* Grid of cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            {data.map((item, index) => (
              <Card
                key={index} // It's important to provide a unique key for each child in a list
                heading={item.productName}
                photoUrl={item.photoUrl}
                description={item.description}
                rating={item.rating}
                similarProducts={item.similarProducts}
                contactMail={item.contactMail}
                website={item.website}
                category={item.category}
                additionalInfo={item.additionalInfo}
              />
            ))}
          </div>
          {/* Conditional rendering of loading indicator */}
          {isLoading && (
            <div className="mt-4 text-center">Loading more items...</div>
          )}
          {/* Load More Button */}
          {parentSelectedRatings.length === 0 && !parentSelectedCategory && (
            <button
              onClick={handleLoadMore}
              className="mt-4 bg-orange-500 hover:bg-orange-700 text-white font-bold py-2 px-4 rounded w-full"
            >
              Load More
            </button>
          )}
        </div>
      </div>
    </>
  );
}
