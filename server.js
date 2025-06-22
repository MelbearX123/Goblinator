import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import OpenAI from 'openai';

// Load environment variables
dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

// Check if API key is loaded
console.log('API Key loaded:', process.env.OPENAI_API_KEY ? 'Yes' : 'No');
console.log('API Key starts with:', process.env.OPENAI_API_KEY?.substring(0, 7) + '...');

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

app.post('/api/translate', async (req, res) => {
  console.log('\n=== NEW TRANSLATION REQUEST ===');
  console.log('Request body:', req.body);
  
  try {
    const { text, fromLang, toLang } = req.body;
    
    if (!text || !text.trim()) {
      console.log('Error: No text provided');
      return res.status(400).json({ error: 'Text is required' });
    }
    
    console.log(`Translating: "${text}"`);
    console.log(`From: ${fromLang} To: ${toLang}`);
    
    const systemMessage = fromLang === "Brainrot" 
      ? "You are a brainrot to English translator. You should translate the phrase into plain English."
      : "You are an English to brainrot translator. You should translate the phrase into brainrot slang.";

    console.log('System message:', systemMessage);
    console.log('About to call OpenAI API...');

    const completion = await openai.chat.completions.create({
      messages: [
        { role: "system", content: systemMessage },
        { role: "user", content: text }
      ],
      model: "ft:gpt-4.1-nano-2025-04-14:personal:brainrot-translate:Bl8MOsFc", // Using standard model first
      store: false,
      temperature: 1.00,
      max_tokens: 2048,
      top_p: 1.00
    });
    
    console.log('OpenAI API call successful');
    console.log('Response:', completion.choices[0].message.content);
    
    res.json({ translation: completion.choices[0].message.content });
    
  } catch (error) {
    console.error('\n=== ERROR DETAILS ===');
    console.error('Error name:', error.name);
    console.error('Error message:', error.message);
    console.error('Error code:', error.code);
    console.error('Error status:', error.status);
    console.error('Full error:', error);
    console.error('========================\n');
    
    res.status(500).json({ 
      error: 'Translation failed',
      details: error.message,
      code: error.code
    });
  }
});

// Add a test endpoint
app.get('/api/test', (req, res) => {
  res.json({ message: 'Server is working!' });
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`Test the server: http://localhost:${PORT}/api/test`);
});