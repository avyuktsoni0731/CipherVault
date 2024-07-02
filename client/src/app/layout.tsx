import type { Metadata } from "next";
import { Inter, Montserrat } from "next/font/google";
import { Providers } from "./providers";
import Authprovider from "../components/authprovider/authprovider";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });
const montserrat = Montserrat({
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "CryptoDrive",
  // description: "Generated by create next app",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={montserrat.className}>
        <Providers>
          <Authprovider>{children}</Authprovider>
        </Providers>
      </body>
    </html>
  );
}
