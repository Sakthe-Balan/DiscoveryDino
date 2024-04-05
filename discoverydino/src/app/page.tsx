import Image from "next/image";
import Header from "@/components/header";
import Filter from '@/components/filter';
import Card from "@/components/card";


export default function Home() {
 return (
    <div className="flex flex-col ">
      <Header />
      <div className="flex flex-col md:flex-row ">
        <div className="w-full md:w-64 md:border-r  p-4">
          <Filter /> {/* Updated to use the correct component name */}
        </div>
        <main className="flex-grow p-4 ">
          {/* Main content goes here */}
        </main>
      </div>
    </div>
 );
}
