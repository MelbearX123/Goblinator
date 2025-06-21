export default function Textbox({ inputText, setInputText }) {
  return(
    <div className="flex flex-col md:flex-row gap-6 max-w-5xl w-full px-6 pb-12">
      <div className="flex-1 bg-white p-4 rounded-xl shadow">
        <textarea className="w-full h-48 resize-none outline-none text-lg" placeholder="Enter text" value={inputText} onChange={(e)=>setInputText(e.target.value)}/>
      </div>

      <div className="flex-1 flex-shrink-0 bg-white p-4 rounded-xl shadow">
        <p className="text-gray-400 italic">
          {inputText ? `(Translation Preview): ${inputText}` : "Translation appears here"}
        </p>
      </div>
    </div>
  );
}