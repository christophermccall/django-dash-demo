import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: path.resolve(__dirname, '../static/js'), // Output to Django's static folder
    emptyOutDir: true,
    rollupOptions: {
      output: {
        entryFileNames: 'react_bundle.js', // Match the file referenced in price_page.html
      },
    },
  },
});