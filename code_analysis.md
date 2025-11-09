# Package.json:

```json
"lint": "cd server && yarn lint && cd ../frontend && yarn lint && cd ../collector && yarn lint”
```
Possui 3 subprojetos: frontend, server e collector (monorepo modular)

```json
"dev:server": "cd server && yarn dev",
"dev:collector": "cd collector && yarn dev",
"dev:frontend": "cd frontend && yarn dev",
```
Cada um pode ser executado separadamente.

```json
"prisma:generate": "cd server && npx prisma generate",
"prisma:migrate": "cd server && npx prisma migrate dev --name init",
"prisma:seed": "cd server && npx prisma db seed",
"prisma:setup": "yarn prisma:generate && yarn prisma:migrate && yarn prisma:seed",
"prisma:reset": "truncate -s 0 server/storage/anythingllm.db && yarn prisma:migrate",
```
Usa Prisma ORM, então o banco é relacional.

```json
"generate:cloudformation": "node cloud-deployments/aws/cloudformation/generate.mjs",
"generate::gcp_deployment": "node cloud-deployments/gcp/deployment/generate.mjs",
```
Infraestrutura em múltiplas nuvens (AWS e GCP).

```json
"concurrently": "^9.1.2",
```
Múltiplos serviços rodando em paralelo.

# Frontend/package.json

```json
"@mintplex-labs/piper-tts-web": "^1.0.4",
"onnxruntime-web": "^1.18.0",
"react-speech-recognition": "^3.10.0"
```
Indica que o frontend processa parte da IA (speech-recognition = suporte a voz).

```json
"start": "vite --open"
```
Usa o Vite como servidor, SPA (Single Page Application).

# Server/package.json

```json
"dependencies": {
  "@prisma/client": "5.3.1",
  "prisma": "5.3.1",
  "mysql2": "^3.9.8",
  "pg": "^8.11.5",
  "mssql": "^10.0.2"
}
```
Usa Prisma ORM e suporta MySQL, SQL Server e PostgreSQL.

```json
"langchain": "0.1.36",
"@langchain/openai": "0.0.28",
"@langchain/anthropic": "0.1.16",
"openai": "4.95.1",
"cohere-ai": "^7.19.0",
"ollama": "^0.5.10",
"@aws-sdk/client-bedrock-runtime": "^3.775.0",
"@xenova/transformers": "^2.14.0"
```
Suporta múltiplas LLMs e pode rodar modelos locais e em nuvem.

# Collector/package.json

```json
"pdf-parse": "^1.1.1",
"epub2": "^3.0.2",
"mammoth": "^1.6.0",
"officeparser": "^4.0.5",
"node-xlsx": "^0.24.0",
"mbox-parser": "^1.0.1",
"html-to-text": "^9.0.5",
"node-html-parser": "^6.1.13"
```
Capaz de ler e converter diferentes formatos de entrada.

```json
"@xenova/transformers": "^2.14.0"
```
Pode pré-processar textos localmente e depois enviar ao servidor.

```json
"fluent-ffmpeg": "^2.1.2",
"tesseract.js": "^6.0.0",
"sharp": "^0.33.5",
"wavefile": "^11.0.0",
"youtubei.js": "^9.1.0"
```
Capaz de extrair imagem, som e vídeo e transformá-los em texto para IA entender.

```json
"devDependencies": {
  "nodemon": "^2.0.22",
  "prettier": "^2.4.1",
  "cross-env": "^7.0.3"
}
```
Possui ferramentas básicas de desenvolvimento, sugerindo que é um serviço auxiliar.

# Docker/dockerfile

```json
FROM base AS build-arm64
RUN echo "Preparing build of AnythingLLM image for arm64 architecture"
...
FROM base AS build-amd64
RUN echo "Preparing build of AnythingLLM image for non-ARM architecture"
```
Compativel com as arquiteturas ARM64 e AMD64.

```json
RUN groupadd -g "$ARG_GID" anythingllm && \
    useradd -u "$ARG_UID" -m -d /app -s /bin/bash -g anythingllm anythingllm && \
    mkdir -p /app/frontend/ /app/server/ /app/collector/
```
Mais uma evidência de que a arquitetura possui 3 camadas (frontend, server e collector).

```json
COPY --from=frontend-build /app/frontend/dist /app/server/public
```
O front e o back são servidos pelo mesmo servidor (monólito distribuído).

