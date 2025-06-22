export default async function handler(req, res) {
  console.log('Function started, method:', req.method);
  
  // Add CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  // Handle preflight
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method === 'POST') {
    try {
      console.log('Request body:', req.body);
      
      const { text, targetLanguage } = req.body;
      
      // Quick test response first
      const result = {
        translatedText: `Test translation of: ${text} to ${targetLanguage}`,
        success: true,
        timestamp: new Date().toISOString()
      };
      
      console.log('Sending response:', result);
      res.status(200).json(result);
      
    } catch (error) {
      console.error('Error:', error);
      res.status(500).json({ 
        error: error.message,
        success: false 
      });
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}