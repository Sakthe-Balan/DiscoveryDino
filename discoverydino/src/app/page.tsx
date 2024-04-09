"use client"
import Header from "@/components/header";
import Filter from '@/components/filter';
import Card from "@/components/card";
import React, { useState,useEffect} from 'react';
import axios from 'axios';
interface CardData {
  heading: string;
  photoUrl: string;
  description: string;
  rating: number;
  similarProducts: string[];
  contactMail: string;
  website: string;
 }


export default function Home() {

  // Provide initial data as part of the state
  const initialData: CardData[] = [
    {
      heading: "Example Heading 1",
      photoUrl: "https://example.com/photo1.jpg",
      description: "Description for the first card...",
      rating: 4.5,
      similarProducts: ['Product 1', 'Product 2', 'Product 3'],
      contactMail: "example1@example.com",
      website: "https://example1.com"
    },
    {
      heading: "Example Heading 2",
      photoUrl: "https://example.com/photo2.jpg",
      description: "Description for the second card...",
      rating: 4.0,
      similarProducts: ['Product 4', 'Product 5', 'Product 6'],
      contactMail: "example2@example.com",
      website: "https://example2.com"
    },{
      heading: "Example Heading 2",
      photoUrl: "https://example.com/photo2.jpg",
      description: "Description for the second card...",
      rating: 4.0,
      similarProducts: ['Product 4', 'Product 5', 'Product 6'],
      contactMail: "example2@example.com",
      website: "https://example2.com"
    },{
      heading: "Example Heading 2",
      photoUrl: "https://example.com/photo2.jpg",
      description: "Description for the second card...",
      rating: 4.0,
      similarProducts: ['Product 4', 'Product 5', 'Product 6'],
      contactMail: "example2@example.com",
      website: "https://example2.com"
    },{
      heading: "Example Heading 2",
      photoUrl: "https://example.com/photo2.jpg",
      description: "Description for the second card...",
      rating: 4.0,
      similarProducts: ['Product 4', 'Product 5', 'Product 6'],
      contactMail: "example2@example.com",
      website: "https://example2.com"
    },{
      heading: "Example Heading 2",
      photoUrl: "https://example.com/photo2.jpg",
      description: "Description for the second card...",
      rating: 4.0,
      similarProducts: ['Product 4', 'Product 5', 'Product 6'],
      contactMail: "example2@example.com",
      website: "https://example2.com"
    },{
      heading: "Example Heading 2",
      photoUrl: "https://example.com/photo2.jpg",
      description: "Description for the second card...",
      rating: 4.0,
      similarProducts: ['Product 4', 'Product 5', 'Product 6'],
      contactMail: "example2@example.com",
      website: "https://example2.com"
    },{
      heading: "Example Heading 2",
      photoUrl: "https://example.com/photo2.jpg",
      description: "Description for the second card...",
      rating: 4.0,
      similarProducts: ['Product 4', 'Product 5', 'Product 6'],
      contactMail: "example2@example.com",
      website: "https://example2.com"
    },{
      heading: "Example Heading 2",
      photoUrl: "https://example.com/photo2.jpg",
      description: "Description for the second card...",
      rating: 4.0,
      similarProducts: ['Product 4', 'Product 5', 'Product 6'],
      contactMail: "example2@example.com",
      website: "https://example2.com"
    },{
      heading: "Example Heading 2",
      photoUrl: "https://example.com/photo2.jpg",
      description: "Description for the second card...",
      rating: 4.0,
      similarProducts: ['Product 4', 'Product 5', 'Product 6'],
      contactMail: "example2@example.com",
      website: "https://example2.com"
    },{
      heading: "Example Heading 2",
      photoUrl: "https://example.com/photo2.jpg",
      description: "Description for the second card...",
      rating: 4.0,
      similarProducts: ['Product 4', 'Product 5', 'Product 6'],
      contactMail: "example2@example.com",
      website: "https://example2.com"
    },{
      heading: "Example Heading 2",
      photoUrl: "https://example.com/photo2.jpg",
      description: "Description for the second card...",
      rating: 4.0,
      similarProducts: ['Product 4', 'Product 5', 'Product 6'],
      contactMail: "example2@example.com",
      website: "https://example2.com"
    },{
      heading: "Example Heading 2",
      photoUrl: "https://example.com/photo2.jpg",
      description: "Description for the second card...",
      rating: 4.0,
      similarProducts: ['Product 4', 'Product 5', 'Product 6'],
      contactMail: "example2@example.com",
      website: "https://example2.com"
    },{
      heading: "Example Heading 2",
      photoUrl: "https://example.com/photo2.jpg",
      description: "Description for the second card...",
      rating: 4.0,
      similarProducts: ['Product 4', 'Product 5', 'Product 6'],
      contactMail: "example2@example.com",
      website: "https://example2.com"
    },{
      heading: "Example Heading 2",
      photoUrl: "https://example.com/photo2.jpg",
      description: "Description for the second card...",
      rating: 4.0,
      similarProducts: ['Product 4', 'Product 5', 'Product 6'],
      contactMail: "example2@example.com",
      website: "https://example2.com"
    },{
      heading: "Example Heading 2",
      photoUrl: "https://example.com/photo2.jpg",
      description: "Description for the second card...",
      rating: 4.0,
      similarProducts: ['Product 4', 'Product 5', 'Product 6'],
      contactMail: "example2@example.com",
      website: "https://example2.com"
    },{
      heading: "Example Heading 2",
      photoUrl: "https://example.com/photo2.jpg",
      description: "Description for the second card...",
      rating: 4.0,
      similarProducts: ['Product 4', 'Product 5', 'Product 6'],
      contactMail: "example2@example.com",
      website: "https://example2.com"
    },{
      heading: "Example Heading 2",
      photoUrl: "https://example.com/photo2.jpg",
      description: "Description for the second card...",
      rating: 4.0,
      similarProducts: ['Product 4', 'Product 5', 'Product 6'],
      contactMail: "example2@example.com",
      website: "https://example2.com"
    },{
      heading: "Example Heading 2",
      photoUrl: "https://example.com/photo2.jpg",
      description: "Description for the second card...",
      rating: 4.0,
      similarProducts: ['Product 4', 'Product 5', 'Product 6'],
      contactMail: "example2@example.com",
      website: "https://example2.com"
    },
    // Add more objects for more cards
 ];

 const [data, setData] = useState<CardData[]>(initialData);
 const [itemsToDisplay, setItemsToDisplay] = useState<number>(10);
 const [isLoading, setIsLoading] = useState(false);


 const fetchData = async () => {
  setIsLoading(true); // Start loading
  try {
     const response: any = await axios.get(`http://localhost:8000/api/data?limit=${itemsToDisplay}`);
 
     // The response data is already parsed as JSON
     console.log(response.data);
     
     // Directly use response.data since it's already an object

     const newData = JSON.parse(response.data);
     console.log('API Response:', newData);
   
     // Check if newData is an array before updating the state
     if (Array.isArray(newData)) {
       setData(prevData => [...prevData, ...newData]);
       setItemsToDisplay(prevItems => prevItems + 10);
     }
     else {
     console.log("out");}
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
        <div className="w-full md:w-64 md:border-r p-4 sm:mr-2 md:mr-20 ">
          <Filter />
        </div>

        {/* Main content section */}
        <div className="flex-grow p-4 ml-20 mt-8 mr-8 border-r-4 rounded-md shadow-lg bg-white border-gray-300 border-2 relative">
          
          {/* Grid of cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
          {data.map((item, index) => (
              <Card 
                key={index} // It's important to provide a unique key for each child in a list
                heading={item.heading} 
                photoUrl={item.photoUrl} 
                description={item.description} 
                rating={item.rating}
                similarProducts={item.similarProducts}
                contactMail={item.contactMail}
                website={item.website}
              />
            ))}
          </div>
           {/* Conditional rendering of loading indicator */}
          {isLoading && <div className="mt-4 text-center">Loading more items...</div>}
           {/* Load More Button */}
           <button onClick={handleLoadMore} className="mt-4 bg-orange-500 hover:bg-orange-700 text-white font-bold py-2 px-4 rounded">
            Load More
          </button>
        </div>
      </div>
    </>
  );
}
