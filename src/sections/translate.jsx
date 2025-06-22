import { useState } from "react";
import Textbox from "../components/textbox";

const LANGUAGES = ["English", "Brainrot"];


export default function Translate(){
  const [inputText, setInputText] = useState("");
  const [fromLang, setFromLang] = useState("English");
  const [toLang, setToLang] = useState("Brainrot");

  const swapLanguages =()=> {
    const temp = fromLang;
    setFromLang(toLang);
    setToLang(temp);
  };

  return(
    <main className="flex flex-col items-center py-32 bg-[#1e1e1e]">
      <div className="flex gap-4 items-center mb-6">
        <p className="px-4 py-2 rounded-lg min-w-[90px] text-center bg-[#000000] shadow border-1 border-[#FF6B6B]">{fromLang}</p>
        <button className="text-2xl text-white copx-2 border-none focus:outline-none transition-transform duration-50 ease-in-out transform hover:scale-135 active:scale-115" onClick={swapLanguages}>
          ⇄
        </button>
        <a className="px-4 py-2 rounded-lg min-w-[90px] text-center bg-[#000000] border-1 border-[#FF6B6B] shadow">{toLang}</a>
      </div>
      
      <Textbox inputText={inputText} setInputText={setInputText} />
    </main>
  );
}