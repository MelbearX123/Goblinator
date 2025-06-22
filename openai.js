import OpenAI from "openai";
require("dotenv").config();

const openai = new OpenAI({
  api_key: process.env.OPENAI_API_KEY,
});

async function translate() {

  try{
    const completion = await openai.chat.completions.create({
      messages: [{ role: "system", content: "You are a brainrot to English translator. You should translate the phrase into plain English." }],
      model: "ft:gpt-4.1-nano-2025-04-14:personal:brainrot-translate:Bl8MOsFc", //Custom fine-tuned model
      store: false, //Does not store conversation history
    });
    
    //Log the results
    console.log('Translation Result: ', completion.choices[0]);
    return completion.choices[0];
  }
  catch (error) {
    console.error('Error:', error.message);
    throw error;
  }



}