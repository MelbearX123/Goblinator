import OpenAI from "openai";
import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

app.post('/api/translate', async (req, res) => {
  try {
    const { text, fromLang, toLang } = req.body;
    
    const systemMessage = fromLang === "Brainrot" 
      ? "You are a brainrot to English translator. Translate the phrase into plain English."
      : "You are an English to brainrot translator. Translate the phrase into brainrot slang.";

    const completion = await openai.chat.completions.create({
      messages: [
        { role: "system", content: systemMessage },
        { role: "user", content: text }
      ],
      model: "ft:gpt-4o-mini-2024-07-18:personal:brainrot-translate:Bl8MOsFc",
      store: false,
    });
    
    res.json({ translation: completion.choices[0].message.content });
  } catch (error) {
    console.error('Translation error:', error);
    res.status(500).json({ error: 'Translation failed' });
  }
});

app.listen(3001, () => {
  console.log('Server running on port 3001');
});