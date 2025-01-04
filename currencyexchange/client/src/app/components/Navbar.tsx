"use client";

import { useRouter } from "next/navigation";
import Image from "next/image";

export default function Navbar() {
  const router = useRouter();

  return (
    <nav className="flex justify-between w-full pl-16 pr-20 py-4">
      <div className="flex items-center gap-3 px-4 py-2 cursor-pointer" onClick={() => router.push('/')}>
        <Image src="/assets/icons/currency-exchange.png" alt="Icon" width={32} height={32} className="pb-1" /> {/* Icon by Pixel Perfect */}
        <h1 className="text-lg font-medium">CurrencyExchange</h1>
      </div>

      <div className="flex items-center gap-3">
        <a className="px-3 py-4 hover:text-sky-500 duration-500" href="/docs">API</a>
        <a className="px-3 py-4 hover:text-sky-500 duration-500" href="/charts">Charts</a>
        <a className="px-3 py-4 hover:text-sky-500 duration-500" href="/about">About</a>
        <button className="w-32 py-1 border-2 border-slate-300 rounded-3xl hover:border-sky-500 hover:bg-sky-500 hover:text-white hover:font-medium duration-500" onClick={() => router.push('/exchange')}>Get Started</button>
      </div>
    </nav>
  );
};