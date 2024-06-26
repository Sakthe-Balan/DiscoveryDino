// components/Header.tsx
import { useState } from 'react';
import Image from 'next/image';
import logo from '../../public/logo.jpg'; // Adjust the path to your logo
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';

interface HeaderProps {
  setSearch: (value: string | null) => void;
}

export default function Header({ setSearch }: HeaderProps) {
  const [inputValue, setInputValue] = useState('');

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  const handleSearchClick = () => {
    setSearch(inputValue);
  };

  return (
    <header
      className="bg-white shadow-lg py-4 px-6 md:px-4 lg:px-4"
      style={{ borderBottom: '4px solid #f55c08' }}
    >
      <div className=" mx-auto flex justify-between items-center">
        <a href="/" className="flex items-center">
          <div className="rounded-full overflow-hidden border border-orange-500">
            <Image
              src={logo}
              alt="Logo"
              width={60}
              height={60}
              className="transition-transform duration-300 hover:scale-110"
            />
          </div>
          <div className="ml-4">
            <h1 className="text-gray-800 text-2xl font-semibold">
              Discovery Dino
            </h1>
            <p className="text-gray-600">Always Stay Ahead!</p>
          </div>
        </a>
        <div className="flex w-[50%] items-center space-x-2">
          {/* <Select>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Database" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="filtered_products">Filtered</SelectItem>
              <SelectItem value="g2_products">G2 Catalogue</SelectItem>
              <SelectItem value="scraped_products">Scrapped</SelectItem>
            </SelectContent>
          </Select> */}
          <Input
            type="text"
            placeholder="Search for the latest products"
            value={inputValue}
            onChange={handleInputChange}
          />
          <Button type="submit" onClick={handleSearchClick}>
            Search
          </Button>
        </div>
        <nav className="flex items-center">
          <ul className="flex space-x-6">
            <li>
              <a
                href="https://www.g2.com/"
                className="text-gray-600 hover:text-orange-500 transition-colors duration-300"
              >
                Visit G2
              </a>
            </li>
            {/* Add more navigation items as needed */}
          </ul>
        </nav>
      </div>
    </header>
  );
}
