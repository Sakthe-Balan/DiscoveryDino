/* eslint-disable react-hooks/exhaustive-deps */
'use client';
import Header from '@/components/header';
import Filter from '@/components/filter';
import Card from '@/components/card';
import React, { useState, useEffect } from 'react';
import { FaTimes, FaTable, FaThLarge } from 'react-icons/fa';
import axios from 'axios';
import { FaRedoAlt } from 'react-icons/fa';
import { FaAlignLeft } from 'react-icons/fa';
import { FaFilter } from 'react-icons/fa';
import { DataTable } from './DataTable';
import { ColumnDef } from '@tanstack/react-table';

interface Review {
  content: string;
}
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
  reviews: Review[];
}
interface cc {
  productName: string;
  photoUrl: string;
  description: string;
  rating: number;
}
// export const columns = [
//   {
//     accessorKey: "photoUrl",
//     header: "Image",
//  },
//   {
//      accessorKey: "productName",
//      header: "Product Name",
//   },

//   {
//      accessorKey: "description",
//      header: "Description",
//   },
//   {
//      accessorKey: "rating",
//      header: "Rating",
//   },
//   ];

export default function Home() {
  // Provide initial data as part of the state
  const initialData: CardData[] = [];

  const [data, setData] = useState<CardData[]>(initialData);
  const [itemsToDisplay, setItemsToDisplay] = useState<number>(9);
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingOverAll, setIsLoadingOverAll] = useState(false);
  const [eexportdata, setEexportdata]: any = useState();
  const [showExportDialog, setShowExportDialog] = useState(false);
  const [parentSelectedRatings, setParentSelectedRatings] = useState<number[]>(
    []
  );
  const [toggle, setToggle]: any = useState('cards');
  const [parentSelectedCategory, setParentSelectedCategory] = useState<
    string | null
  >(null);
  const [search, setSearch] = useState<string | null>(null);

  useEffect(() => {
    const fetchSearchData = async () => {
      if (search != null) {
        // console.log(`Searching data ${search}`);
        try {
          // setParentSelectedCategory(null);
          // setParentSelectedRatings([]);
          setIsLoadingOverAll(true);
          const apiUrl = `${process.env.NEXT_PUBLIC_SERVER_URL}/api/search?collection=filtered_products&searchString=${search}`;
          const response = await fetch(apiUrl);

          if (response.ok) {
            const result = await response.json();
            setData(result.results);
          } else {
            // Handle non-successful response (e.g., show error message)
            console.error('Failed to fetch data:', response.statusText);
          }
          setIsLoadingOverAll(false);
        } catch (error) {
          // Handle fetch error (e.g., network error)
          console.error('Error fetching data:', error);
        }
      }
    };

    fetchSearchData();
  }, [search]);

  useEffect(() => {
    // Define a function to fetch filtered products based on selected ratings and category
    const fetchFilteredProducts = async () => {
      if (parentSelectedRatings.length === 0 && !parentSelectedCategory) {
        try {
          setIsLoadingOverAll(true);
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
          setIsLoadingOverAll(false);
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      } else {
        setIsLoadingOverAll(true);
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
          setIsLoadingOverAll(false);
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
      // setIsLoadingOverAll(true);
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
        // setItemsToDisplay((prevItems) => prevItems + 9);
      }
      // setIsLoadingOverAll(false);
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
          const response: any = await axios.get(
            `${process.env.NEXT_PUBLIC_SERVER_URL}/api/data?limit=0`
          );

          // The response data is already parsed as JSON
          //  console.log(response.data);

          // Directly use response.data since it's already an object

          const newData = response.data;

          console.log('API Response:', newData);
          console.log(newData);
          // Check if newData is an array before updating the state
          if (Array.isArray(newData)) {
            setEexportdata(newData);
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
      fetchssData();
      console.log(eexportdata);
      exportData(eexportdata);
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
    setItemsToDisplay((prevItems) => prevItems + 9);
  };

  return (
    <>
      <Header setSearch={setSearch} />

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
        {/* <span className="">
          <div className="bg-gray-200 w-half h-10 rounded border-r-4 flex items-center pl-4 justify-items-end"></div>
        </span> */}
        {/* Main content section */}
        <div className="md:w-[77%] mt-4">
          <div className="md:w-full flex items-center justify-between mx-4 p-2 border-r-4 rounded-md shadow-lg bg-white border-gray-300 relative mb-2">
            <div>Products Found {data.length}</div>
            <div className="flex gap-2">
              <div
                className={
                  'text-orange-500 transform' +
                  (toggle === 'cards' ? ' scale-150 text-orange-700' : '')
                }
                onClick={() => {
                  setToggle('cards');
                }}
              >
                <FaTable className="h-4 w-4 hover:scale-125" />
              </div>
              <div
                className={
                  'text-orange-600 transform' +
                  (toggle === 'tables' ? ' scale-150 text-orange-700' : '')
                }
                onClick={() => {
                  setToggle('tables');
                }}
              >
                <FaAlignLeft className="h-4 w-4 hover:scale-125" />
              </div>
            </div>
          </div>
          <div className="md:w-full flex-grow p-4  mx-4 border-r-4 rounded-md shadow-lg bg-white border-gray-300  relative">
            {isLoadingOverAll && (
              <div className="absolute w-full h-full bg-white flex justify-center pt-[20%] top-0 left-0 z-50">
                <div className="animate-spin  w-14 h-14 ">
                  <FaRedoAlt className="w-14 h-14 text-slate-400" />
                </div>
              </div>
            )}
            {/* Grid of cards */}
            {toggle === 'cards' && (
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
                    reviews={item.reviews}
                  />
                ))}
              </div>
            )}
            {toggle === 'tables' && (
              <>
                <DataTable
                  columns={[
                    {
                      accessorKey: 'photoUrl',
                      header: 'Image',
                    },
                    {
                      accessorKey: 'productName',
                      header: 'Product Name',
                    },

                    {
                      accessorKey: 'description',
                      header: 'Description',
                    },
                    {
                      accessorKey: 'rating',
                      header: 'Rating',
                    },
                  ]}
                  data={data.map((item) => ({
                    productName: item.productName,
                    photoUrl: item.photoUrl,
                    description: item.description,
                    rating: item.rating,
                  }))}
                />
              </>
            )}
            {/* Conditional rendering of loading indicator */}
            {isLoading && (
              <div className="mt-4 text-center">
                <div className="flex space-x-2 justify-center items-center">
                  <FaRedoAlt className="animate-spin" />{' '}
                  <div className="text-lg">Loading More Products</div>
                </div>
              </div>
            )}
            {/* Buttons */}
            {/* Buttons */}
            <div className="flex justify-between mt-4">
              <button
                onClick={() => setShowExportDialog(true)}
                className="mt-4 bg-orange-500 hover:bg-orange-700 text-white font-bold py-2 px-4 rounded"
              >
                Export as JSON
              </button>
              {parentSelectedRatings.length === 0 &&
                !parentSelectedCategory &&
                search == null && (
                  <button
                    onClick={handleLoadMore}
                    className="mt-4 bg-orange-500 hover:bg-orange-700 text-white font-bold py-2 px-4 rounded"
                  >
                    Load More
                  </button>
                )}
            </div>
          </div>
        </div>
      </div>

      {/* Export dialog */}
      {showExportDialog && (
        <div className="fixed inset-0 z-10 flex items-center justify-center bg-black bg-opacity-50">
          <div className="bg-white p-6 rounded-md shadow-md">
            <div className="flex justify-between items-center mb-4">
              <p className="text-lg font-semibold">Choose export option:</p>
              <button
                onClick={() => setShowExportDialog(false)}
                className="text-gray-600 hover:text-gray-800"
              >
                <FaTimes />
              </button>
            </div>
            <div className="flex justify-between gap-4">
              <button
                onClick={() => handleExport(true)}
                className="bg-yellow-500 hover:bg-yellow-700 text-white font-bold py-2 px-4 rounded"
              >
                Export displayed data
              </button>
              <button
                onClick={() => handleExport(false)}
                className="bg-yellow-500 hover:bg-yellow-700 text-white font-bold py-2 px-4 rounded"
              >
                Export entire dataset
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
