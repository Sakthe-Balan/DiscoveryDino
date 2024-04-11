/* eslint-disable react-hooks/exhaustive-deps */
'use client';
import Header from '@/components/header';
import Filter from '@/components/filter';
import Card from "@/components/card";
import React, { useState,useEffect} from 'react';
import { FaTimes } from 'react-icons/fa';
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
 const [eexportdata, setEexportdata]:any = useState();
 const [showExportDialog, setShowExportDialog] = useState(false);

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



 const handleExport = (exportDisplayedData: boolean) => {
  if (exportDisplayedData) {
    exportData(data);
  } else {
    const fetchssData = async () => {
      setIsLoading(true); // Start loading
      try {
         const response: any = await axios.get(`https://itnrmdjr7f.ap-south-1.awsapprunner.com/api/data?limit=0`);
     
         // The response data is already parsed as JSON
        //  console.log(response.data);
         
         // Directly use response.data since it's already an object
    
         const newData = response.data;
    
         console.log('API Response:', newData);
        console.log(newData)
         // Check if newData is an array before updating the state
         if (Array.isArray(newData)) {
          
         setEexportdata(newData);
         
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
     fetchssData();
     console.log(eexportdata);
     exportData(eexportdata)
  }
  setShowExportDialog(false);
};

const exportData = (exportedData: CardData[]) => {
  const json = JSON.stringify(exportedData);
  const blob = new Blob([json], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'data.json';
  a.click();
  URL.revokeObjectURL(url);
};



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
          {isLoading && <div className="mt-4 text-center">Loading more items...</div>}
           {/* Buttons */}
          {/* Buttons */}
          <div className="flex justify-between mt-4">
            <button onClick={() => setShowExportDialog(true)} className="bg-yellow-500 hover:bg-yellow-700 text-white font-bold py-2 px-4 rounded">
              Export as JSON
            </button>
            <button onClick={handleLoadMore} className="bg-orange-500 hover:bg-orange-700 text-white font-bold py-2 px-4 rounded">
              Load More
            </button>
          </div>
          {/* Conditional rendering of loading indicator */}
          
          {/* Load More Button */}
          {parentSelectedRatings.length === 0 && !parentSelectedCategory 
           
          }
        </div>
      </div>

      {/* Export dialog */}
{showExportDialog && (
  <div className="fixed inset-0 z-10 flex items-center justify-center bg-black bg-opacity-50">
    <div className="bg-white p-6 rounded-md shadow-md">
      <div className="flex justify-between items-center mb-4">
        <p className="text-lg font-semibold">Choose export option:</p>
        <button onClick={() => setShowExportDialog(false)} className="text-gray-600 hover:text-gray-800">
          <FaTimes />
        </button>
      </div>
      <div className="flex justify-between gap-4">
        <button onClick={() => handleExport(true)} className="bg-yellow-500 hover:bg-yellow-700 text-white font-bold py-2 px-4 rounded">
          Export displayed data
        </button>
        <button onClick={() => handleExport(false)} className="bg-yellow-500 hover:bg-yellow-700 text-white font-bold py-2 px-4 rounded">
          Export entire dataset
        </button>
      </div>
    </div>
  </div>
)}
    </>
  );
}
