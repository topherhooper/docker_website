#!/bin/bash

# Create project directories
mkdir -p llm-chat/frontend/src/components
mkdir -p llm-chat/frontend/public
mkdir -p llm-chat/backend/app/api
mkdir -p llm-chat/backend/app/core
mkdir -p llm-chat/backend/app/utils

# Create frontend files
cat > llm-chat/frontend/package.json << 'EOF'
{
  "name": "llm-chat-frontend",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "lucide-react": "^0.263.1",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.15",
    "@types/react-dom": "^18.2.7",
    "@vitejs/plugin-react": "^4.0.3",
    "autoprefixer": "^10.4.14",
    "postcss": "^8.4.27",
    "tailwindcss": "^3.3.3",
    "vite": "^4.4.5"
  }
}
EOF

cat > llm-chat/frontend/vite.config.js << 'EOF'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000
  }
})
EOF

touch llm-chat/frontend/src/components/ChatInterface.jsx
touch llm-chat/frontend/src/App.jsx
touch llm-chat/frontend/src/main.jsx

# Create backend files
touch llm-chat/backend/app/api/routes.py
touch llm-chat/backend/app/api/models.py
touch llm-chat/backend/app/core/config.py
touch llm-chat/backend/app/core/llm.py
touch llm-chat/backend/app/utils/cache.py
touch llm-chat/backend/requirements.txt
touch llm-chat/backend/main.py

# Create and make executable start scripts
cat > llm-chat/start-backend.sh << 'EOF'
#!/bin/bash
cd backend
pip install -r requirements.txt
python main.py
EOF

cat > llm-chat/start-frontend.sh << 'EOF'
#!/bin/bash
cd frontend
npm install
npm run dev
EOF

chmod +x llm-chat/start-backend.sh
chmod +x llm-chat/start-frontend.sh

echo "Project structure created successfully"