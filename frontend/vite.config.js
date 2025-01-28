import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
	plugins: [react()],
	server: {
		port: 5173, // Ensure this is set
		open: true, // Opens browser on start
	},
});
