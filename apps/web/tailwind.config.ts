import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        canvas: "#08090a",
        panel: "#0f1011",
        surface: "#191a1b",
        line: "rgba(255,255,255,0.08)",
        glyph: "#9d9788",
        brand: "#5e6ad2",
      },
      boxShadow: {
        glow: "0 0 80px rgba(113,112,255,0.18)",
      },
    },
  },
  plugins: [],
};

export default config;
