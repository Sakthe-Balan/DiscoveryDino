import Header from "@/components/header";
import Filter from '@/components/filter';
import Card from "@/components/card";

export default function Home() {
  return (
    <>
      <Header />
      <div className="relative mt-4 flex flex-col md:flex-row flex-grow">
        {/* Background stickers */}
        <div className="absolute top-0 right-0 bg-orange-500 h-20 w-20 rounded-full transform rotate-45"></div>
        <div className="absolute top-0 left-4 bg-yellow-500 h-12 w-12 rounded-lg transform rotate-45"></div>
        
        {/* Filter section */}
        <div className="w-full md:w-64 md:border-r p-4 ml-5">
          <Filter />
        </div>

        {/* Main content section */}
        <div className="flex-grow p-4 ml-10 mt-8 mr-8 border-r-4 rounded-md shadow-lg bg-white border-gray-300 border-2 relative">
          
          {/* Grid of cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            <Card 
              heading="Example Heading" 
              photoUrl="https://example.com/photo.jpg" 
              description="This is an example description." 
            />
            <Card 
              heading="Example Heading" 
              photoUrl="https://example.com/photo.jpg" 
              description="This is an example description." 
            />
            <Card 
              heading="Example Heading" 
              photoUrl="https://example.com/photo.jpg" 
              description="This is an example description." 
            />
             <Card 
              heading="Example Heading" 
              photoUrl="https://example.com/photo.jpg" 
              description="This is an example description." 
            />
             <Card 
              heading="Example Heading" 
              photoUrl="https://example.com/photo.jpg" 
              description="This is an example description." 
            />
             <Card 
              heading="Example Heading" 
              photoUrl="https://example.com/photo.jpg" 
              description="This is an example description." 
            />
            {/* Add more cards here */}
            <Card 
              heading="Another Example" 
              photoUrl="https://example.com/another-photo.jpg" 
              description="This is another example description." 
            />
            <Card 
              heading="Yet Another Example" 
              photoUrl="https://example.com/yet-another-photo.jpg" 
              description="This is yet another example description." 
            />
            {/* Add more cards here */}
          </div>
        </div>
      </div>
    </>
  );
}
