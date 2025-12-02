/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class",
  content: ["./templates/**/*.html"],
  theme: {
    extend: {
      colors: {
        light: {
          header: {
            bg: "#9333EA",
            text: "#FFFFFF",
          },
          main: {
            bg: "#F9FAFB",
          },
          text: {
            primary: "#111827",
            secondary: "#4B5563",
          },
          card: {
            bg: "#FFFFFF",
            shadow: "rgba(0, 0, 0, 0.1)",
          },
          button: {
            primary: {
              bg: "#9333EA",
              text: "#FFFFFF",
              hover: "#7E22CE",
            },
            secondary: {
              bg: "#F3E8FF",
              text: "#7E22CE",
              hover: "#E9D5FF",
            },
            footer: {
              bg: "#F3F4F6",
              text: "#4B5563",
            },
          },
        },
        dark: {
          header: {
            bg: "#7E22CE",
            text: "#FFFFFF",
          },
          main: {
            bg: "#111827",
          },
          text: {
            primary: "#F3F4F6",
            secondary: "#9CA3AF",
          },
          card: {
            bg: "#1F2937",
            shadow: "rgba(0, 0, 0, 0.3)",
          },
          button: {
            primary: {
              bg: "#9333EA",
              text: "#FFFFFF",
              hover: "#A855F7",
            },
            secondary: {
              bg: "#374151",
              text: "#E5E7EB",
              hover: "#4B5563",
            },
          },
          footer: {
            bg: "#1F2937",
            text: "#9CA3AF",
          },
        },
      },
    },
  },
  plugins: [],
};
