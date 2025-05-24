
# Video Transcription App (Instagram Support)

## Pré-requisitos

- Node.js
- Python 3
- `instaloader` e `ffmpeg` instalados globalmente:
  ```
  pip install instaloader
  sudo apt install ffmpeg
  ```

## Variáveis de ambiente

Crie um arquivo `.env` na pasta `backend/` com sua chave da OpenAI:

```
OPENAI_API_KEY=sua-chave-aqui
```

## Executando o servidor

```bash
cd backend
npm install openai express multer dotenv
node server.js
```

## Teste

Envie um POST para:
```
POST http://localhost:3001/transcribe/instagram
Content-Type: application/json

{
  "url": "https://www.instagram.com/reel/EXEMPLO/"
}
```

## Resultado

Você receberá a transcrição do áudio extraído do vídeo do Instagram.
