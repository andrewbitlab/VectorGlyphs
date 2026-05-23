import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Vector Glyph Generator — Create SVG & PNG Glyphs Online",
  description:
    "Generate beautiful circular vector glyphs for apps, websites, logos, UI and digital products. Preview for free, download SVG or high-resolution PNG for $1. Commercial license included.",
  metadataBase: new URL("https://vectorglyphs.com"),
  openGraph: {
    title: "Vector Glyph Generator — Create SVG & PNG Glyphs Online",
    description:
      "Generate beautiful circular vector glyphs for apps, websites, logos, UI and digital products.",
    url: "https://vectorglyphs.com",
    siteName: "VectorGlyphs",
    type: "website",
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
