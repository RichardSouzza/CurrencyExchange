'use client';

import { useRouter } from 'next/navigation';
import Image from 'next/image';

export default function Hero() {
  const router = useRouter();

  return (
    <section className='flex justify-between min-h-96 px-20'>
      <div className='flex justify-center items-center'>
        <div className='flex flex-col justify-center gap-3 basis-7/12'>
          <div className='flex flex-wrap text-4xl font-semibold'>
            <h2 className='text-nowrap'>
              Your source for&nbsp;
            </h2>
            <h2 className='text-nowrap'>
              daily currency rates
            </h2>
          </div>
          <p>
            CurrencyPulse API offers reliable, daily updated exchange rates and conversion services.
            Built on open-source principles, our platform ensures transparency and ease of integration for developers and organizations alike.
          </p>
          <button className='max-w-36 my-2 py-1.5 rounded-3xl bg-sky-500 text-white font-medium cursor-pointer hover:bg-sky-700 duration-300' onClick={() => router.push('/exchange')}>Get Started</button>
        </div>  
      </div>

      <div className='flex justify-center items-center'>
        <Image src='/images/gradient-international-trade.png' alt='International Trade' width={720} height={720} /> {/* Image by Freepik */}
      </div>
    </section>
  );
};