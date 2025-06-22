// app/api/translate/route.js (App Router)
export async function POST(request) {
  console.log('API route hit!'); // Add logging
  
  try {
    const body = await request.json();
    console.log('Request body:', body);
    
    // Your translation logic
    return Response.json({ 
      translatedText: "Test response",
      success: true 
    });
  } catch (error) {
    console.error('API Error:', error);
    return Response.json({ 
      error: error.message 
    }, { status: 500 });
  }
}

// Handle GET requests too for testing
export async function GET() {
  return Response.json({ message: 'Translate API is working' });
}