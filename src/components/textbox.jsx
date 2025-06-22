export default function Textbox({ inputText, setInputText, translatedText }) {
  return(
    <div className="flex flex-col md:flex-row gap-12 max-w-5xl w-full px-6 pb-12">
      <div className="flex-1 resize-none bg-black border-2 border-[#FF6B6B] shadow-[0_0_10px_2px_rgba(255,107,107,0.7)] transition-shadow duration-120 hover:shadow-[0_0_12px_4px_rgba(255,107,107,0.8)] p-4 rounded-xl shadow">
        <textarea 
          className="w-full h-48 resize-none flex-shrink-0 min-w-[350px] max-w-[400px] outline-none text-white text-lg" 
          placeholder="Enter text" 
          value={inputText} 
          onChange={(e) => setInputText(e.target.value)}
        />
      </div>

      <div className="flex-1 flex-shrink-0 bg-black border-2 border-[#FF6B6B] shadow-[0_0_10px_2px_rgba(255,107,107,0.7)] transition-shadow duration-120 hover:shadow-[0_0_12px_4px_rgba(255,107,107,0.8)] p-4 rounded-xl shadow">
        <p className="text-white flex-shrink-0 min-w-[350px] max-w-[400px] italic break-words overflow-auto resize-none">
          {translatedText || "Translation appears here"}
        </p>
      </div>
    </div>
  );
}