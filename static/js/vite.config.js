import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: path.resolve(__dirname, '../static/js'), // Ensure this matches Django's expected path
    emptyOutDir: true,
    rollupOptions: {
      output: {
        entryFileNames: 'react_bundle.js',
      },
    },
  },
});

