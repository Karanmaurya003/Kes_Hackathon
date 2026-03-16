/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./pages/**/*.{js,jsx}", "./components/**/*.{js,jsx}"],
  theme: {
    extend: {
      fontFamily: {
        display: ["'Space Grotesk'", "system-ui", "sans-serif"],
        body: ["'DM Sans'", "system-ui", "sans-serif"],
      },
      colors: {
        ink: "#0f1a24",
        sand: "#f7f3ee",
        ocean: "#0f4c5c",
        flare: "#f25c54",
        moss: "#5f9d61",
        sun: "#f6bd60",
      },
      backgroundImage: {
        "hero-gradient": "radial-gradient(circle at top, #f6bd60 0%, #f7f3ee 45%, #dbe7e4 100%)",
      },
      boxShadow: {
        glow: "0 20px 60px rgba(15, 76, 92, 0.18)",
      },
    },
  },
  plugins: [],
};
