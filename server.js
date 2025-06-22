import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import OpenAI from 'openai';

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

app.post('/api/translate', async (req, res) => {
  console.log('=== Translation Request ===');
  console.log('Request body:', req.body);
  
  try {
    const { text, fromLang, toLang } = req.body;
    
    if (!text || !text.trim()) {
      console.log('No text provided');
      return res.status(400).json({ error: 'Text is required' });
    }
    
    const systemMessage = fromLang === "Brainrot" 
      ? "You are a brainrot to English translator. You should translate the phrase into plain English."
      : "You are an English to brainrot translator. You should translate the phrase into brainrot slang.";

    console.log('Calling OpenAI...');
    
    const completion = await openai.chat.completions.create({
      messages: [
        { role: "system", content: systemMessage },
        { role: "user", content: text }
      ],
      model: "ft:gpt-4o-mini-2024-07-18:personal:brainrot-translate:Bl8MOsFc",
      temperature: 0,
      max_tokens: 150,
      store: false,
    });
    
    const translation = completion.choices[0].message.content;
    console.log('Translation result:', translation);
    
    // Make sure we're sending a proper JSON response
    const responseData = { translation: translation };
    console.log('Sending response:', responseData);
    
    res.json(responseData);
    
  } catch (error) {
    console.error('=== ERROR ===');
    console.error('Error:', error);
    console.error('Error message:', error.message);
    console.error('=============');
    
    // Make sure we always send a JSON response, even on error
    if (!res.headersSent) {
      res.status(500).json({ 
        error: 'Translation failed',
        details: error.message 
      });
    }
  }
});

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ status: 'Server is running' });
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});