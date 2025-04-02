import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: path.resolve(__dirname, '../static/frontend'),  // Output to Django's static folder, under 'frontend'
    emptyOutDir: true,  // Ensure that the output directory is cleared before the new build
    rollupOptions: {
      output: {
        entryFileNames: 'react_bundle.js.jsx',  // Name the output file as 'main.jsx', which is more typical
      },
    },
  },
});
