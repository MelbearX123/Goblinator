import { useState } from "react";
import Textbox from "../components/textbox";

export default function Translate(){
  const [inputText, setInputText] = useState("");
  const [translatedText, setTranslatedText] = useState("");
  const [fromLang, setFromLang] = useState("Brainrot");
  const [toLang, setToLang] = useState("English");
  const [isLoading, setIsLoading] = useState(false);

  const swapLanguages = () => {
    const temp = fromLang;
    setFromLang(toLang);
    setToLang(temp);
    // Clear translations when swapping
    setTranslatedText("");
  };

  const handleTranslate = async () => {
  if (!inputText.trim()) return;
  
  setIsLoading(true);
  try {
    const API_URL = process.env.NODE_ENV === 'production' 
      ? 'https://translation-api-dusky.vercel.app'
      : 'http://localhost:3001';

    
    const response = await fetch(`${API_URL}/api/translate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: inputText,
        targetLanguage: toLang,
        fromLang: fromLang  // Include source language
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    setTranslatedText(data.translatedText);
  } catch (error) {
    console.error('Translation error:', error);
    setTranslatedText(`Translation failed: ${error.message}`);
  } finally {
    setIsLoading(false);
  }
};

  return(
    <main className="flex flex-col items-center py-32 bg-[#1e1e1e]">
      <div className="flex gap-4 items-center mb-6">
        <p className="px-4 py-2 rounded-lg min-w-[90px] text-center bg-[#000000] shadow border border-[#FF6B6B]">{fromLang}</p>
        <button 
          className="text-2xl text-white px-2 border-none focus:outline-none transition-transform duration-50 ease-in-out transform hover:cursor-pointer transform hover:scale-135 active:scale-115" 
          onClick={swapLanguages}
        >
          ⇄
        </button>
        <p className="px-4 py-2 rounded-lg min-w-[90px] text-center bg-[#000000] border border-[#FF6B6B] shadow">{toLang}</p>
      </div>
      
      <Textbox 
        inputText={inputText} 
        setInputText={setInputText}
        translatedText={translatedText}
      />
      
      <div className="flex gap-4 mb-6 items-center">
        <button 
          className="text-2xl text-white font-semibold px-4 py-2 scale-135 border-none focus:outline-none transition-transform duration-75 ease-in-out transform hover:cursor-pointer transform hover:opacity-70 transform active:scale-125 bg-[#FF6B6B] transform active:opacity-50 rounded-lg shadow opacity-90"
          onClick={handleTranslate}
          disabled={isLoading || !inputText.trim()}
        >
          {isLoading ? 'Translating...' : 'Translate'}
        </button>
      </div>
    </main>
  );
}