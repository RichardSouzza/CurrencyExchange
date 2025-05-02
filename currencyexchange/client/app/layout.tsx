import type { Metadata } from 'next';
import { Providers } from './providers';
import { Montserrat } from 'next/font/google';
import Navbar from './components/Navbar';
import './globals.css';

const montserrat = Montserrat({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'CurrencyExchange',
  description: '',
  icons: [{
    rel: 'icon',
    type: 'image/x-icon',
    url: '/icons/currency-exchange.png', // Icon by Pixel Perfect
  }],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang='en' suppressHydrationWarning>
      <body>
        <Providers>
          <div id='root' className={`flex flex-col min-h-screen ${montserrat.className} bg-slate-100`}>
            <Navbar />
            {children}
          </div>
        </Providers>
      </body>
    </html>
  );
};
