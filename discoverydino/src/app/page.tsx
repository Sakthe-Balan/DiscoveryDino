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
        <div className="absolute top-2 left-6 bg-yellow-500 h-12 w-12 rounded-lg transform rotate-45"></div>
        
        {/* Filter section */}
        <div className="w-full md:w-64 md:border-r p-4 sm:mr-2 md:mr-20 ">
          <Filter />
        </div>

        {/* Main content section */}
        <div className="flex-grow p-4 ml-20 mt-8 mr-8 border-r-4 rounded-md shadow-lg bg-white border-gray-300 border-2 relative">
          
          {/* Grid of cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            <Card 
              heading="Example Heading" 
              photoUrl="https://example.com/photo.jpg" 
              description="Since 1999, millions of people have expressed themselves on Blogger. From detailed posts about almost every apple variety you could ever imagine to a blog dedicated to the art of blogging itself, the ability to easily share, publish and express oneself on the web is at the core of Blogger’s mission. As the web constantly evolves" 
              rating={4.5}
              similarProducts={['Product 1', 'Product 2', 'Product 3']}
              contactMail="example@example.com"
              website="https://example.com"
            />
                        <Card 
              heading="Example Heading" 
              photoUrl="https://example.com/photo.jpg" 
              description="Since 1999, millions of people have expressed themselves on Blogger. From detailed posts about almost every apple variety you could ever imagine to a blog dedicated to the art of blogging itself, the ability to easily share, publish and express oneself on the web is at the core of Blogger’s mission. As the web constantly evolves" 
              rating={4.5}
              similarProducts={['Product 1', 'Product 2', 'Product 3']}
              contactMail="example@example.com"
              website="https://example.com"
            />
                        <Card 
              heading="Example Heading" 
              photoUrl="https://example.com/photo.jpg" 
              description="Since 1999, millions of people have expressed themselves on Blogger. From detailed posts about almost every apple variety you could ever imagine to a blog dedicated to the art of blogging itself, the ability to easily share, publish and express oneself on the web is at the core of Blogger’s mission. As the web constantly evolves" 
              rating={4.5}
              similarProducts={['Product 1', 'Product 2', 'Product 3']}
              contactMail="example@example.com"
              website="https://example.com"
            />
                        <Card 
              heading="Example Heading" 
              photoUrl="https://example.com/photo.jpg" 
              description="Since 1999, millions of people have expressed themselves on Blogger. From detailed posts about almost every apple variety you could ever imagine to a blog dedicated to the art of blogging itself, the ability to easily share, publish and express oneself on the web is at the core of Blogger’s mission. As the web constantly evolves" 
              rating={4.5}
              similarProducts={['Product 1', 'Product 2', 'Product 3']}
              contactMail="example@example.com"
              website="https://example.com"
            />
                        <Card 
              heading="Example Heading" 
              photoUrl="https://example.com/photo.jpg" 
              description="Since 1999, millions of people have expressed themselves on Blogger. From detailed posts about almost every apple variety you could ever imagine to a blog dedicated to the art of blogging itself, the ability to easily share, publish and express oneself on the web is at the core of Blogger’s mission. As the web constantly evolves" 
              rating={4.5}
              similarProducts={['Product 1', 'Product 2', 'Product 3']}
              contactMail="example@example.com"
              website="https://example.com"
            />
                        <Card 
              heading="Example Heading" 
              photoUrl="https://example.com/photo.jpg" 
              description="Since 1999, millions of people have expressed themselves on Blogger. From detailed posts about almost every apple variety you could ever imagine to a blog dedicated to the art of blogging itself, the ability to easily share, publish and express oneself on the web is at the core of Blogger’s mission. As the web constantly evolves" 
              rating={4.5}
              similarProducts={['Product 1', 'Product 2', 'Product 3']}
              contactMail="example@example.com"
              website="https://example.com"
            />
                        
            {/* Add more cards here */}
          </div>
        </div>
      </div>
    </>
  );
}
