# Multistage build compiling with bun
FROM oven/bun:latest AS base

WORKDIR /app

COPY package.json bun.lock ./

RUN bun install --frozen-lockfile

COPY . .

RUN bun run build

FROM oven/bun:latest AS runner

WORKDIR /app

# Copy only the necessary files for running the application
COPY --from=base /app/.next ./.next
COPY --from=base /app/node_modules ./node_modules
COPY --from=base /app/package.json ./package.json

EXPOSE 3000

CMD ["bun", "run", "start"]

