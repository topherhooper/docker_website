# Frontend Development

## Project Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/docker_website.git
    cd docker_website/frontend
    ```

2. Install dependencies:
    ```sh
    npm install
    ```

3. Start the development server:
    ```sh
    npm run dev
    ```
4. Deployment
    * Configure environment variables
    * Run deployment script
```bash
./deploy.sh
```


## Project Structure

- `src/` - Contains the source code for the frontend
  - `components/` - React components (Chatbot, ChatInput, ChatMessage)
  - `main.jsx` - Application entry point
  - `index.css` - Global styles (Tailwind CSS)
- `package.json` - Project dependencies and scripts
- `vite.config.js` - Vite configuration
- `tailwind.config.js` - Tailwind CSS configuration
- `postcss.config.js` - PostCSS configuration

## Available Scripts

- `npm run dev` - Starts the development server using Vite
- `npm run build` - Builds the app for production
- `npm run preview` - Locally preview production build

## Development

The development server will run on http://localhost:5173 with hot module replacement enabled.

## Technology Stack

- React 18.2.0
- Vite 4.4.5
- Tailwind CSS 3.3.3
- Lucide React 0.263.1

## Contributing

1. Fork the repository at `https://github.com/yourusername/docker_website`
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add: your feature description'`)
5. Push to the branch (`git push origin feature/your-feature-name`)
6. Open a pull request

## License

Copyright (c) 2023 Your Name

This project is licensed under the MIT License. See the LICENSE file for details.
