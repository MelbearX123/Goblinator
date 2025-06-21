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
    <main className="flex flex-col items-center py-8 bg-gray-100 min-h-screen">
      <div className="flex gap-4 items-center mb-6">
        <p className="px-4 py-2 rounded-lg min-w-[90px] text-center bg-white shadow">{fromLang}</p>
        <button className="text-2xl px-2 border-none focus:outline-none transition-transform duration-75 ease-in-out transform hover:scale-110 active:scale-125" onClick={swapLanguages}>
          ⇄
        </button>
        <a className="px-4 py-2 rounded-lg min-w-[90px] text-center bg-white shadow">{toLang}</a>
      </div>
      
      <Textbox inputText={inputText} setInputText={setInputText} />
    </main>
  );
}