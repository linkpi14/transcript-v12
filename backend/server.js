
const express = require('express');
const multer = require('multer');
const { execFile } = require('child_process');
const path = require('path');
const fs = require('fs');
const OpenAI = require('openai');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 3001;

app.use(express.json());

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// Rota principal: Instagram
app.post('/transcribe/instagram', async (req, res) => {
  const { url } = req.body;
  if (!url) return res.status(400).json({ error: 'Instagram URL is required.' });

  const outputDir = path.join(__dirname, 'tmp');
  fs.mkdirSync(outputDir, { recursive: true });

  execFile('python3', ['microservice/download_instagram.py', url, outputDir], async (err, stdout, stderr) => {
    if (err) {
      console.error('Erro no script:', stderr);
      return res.status(500).json({ error: 'Erro ao processar o vídeo do Instagram.' });
    }

    const mp3Path = stdout.toString().trim();
    try {
      const transcription = await openai.audio.transcriptions.create({
        file: fs.createReadStream(mp3Path),
        model: 'whisper-1',
        response_format: 'text',
      });

      return res.json({ transcription });
    } catch (error) {
      console.error('Erro ao enviar para Whisper:', error);
      return res.status(500).json({ error: 'Erro ao transcrever áudio.' });
    }
  });
});

app.listen(port, () => {
  console.log(`Servidor rodando em http://localhost:${port}`);
});
