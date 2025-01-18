FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

# Mount secrets during build
RUN --mount=type=secret,id=google_oauth \
    mkdir -p .credentials && \
    cp /run/secrets/google_oauth .credentials/frontend_google_oath.json

RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx/default.conf /etc/nginx/conf.d/default.conf
EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]