import OpenAI from "openai";
require("dotenv").config();

const openai = new OpenAI(process.env.OPENAI_API_KEY);

async function main() {
  const completion = await openai.chat.completions.create({
    messages: [{ role: "system", content: "You are a brainrot to English translator. You should translate the phrase into plain English." }],
    model: "ft:gpt-4.1-nano-2025-04-14:personal:brainrot-translate:Bl8MOsFc",
    store: false, // Does not store conversation history
  });

  console.log(completion.choices[0]);
}

main();