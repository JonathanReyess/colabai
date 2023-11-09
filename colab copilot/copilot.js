// import the required dependencies
require("dotenv").config(); 
const fs = require('fs');
const OpenAI = require("openai"); //openai npm package
const readline = require("readline").createInterface({ //prompt the user for input in our terminal
  input: process.stdin,
  output: process.stdout,
});

// create a OpenAI connection by getting our key from our env
const secretKey = process.env.OPENAI_API_KEY;
const openai = new OpenAI({
  apiKey: secretKey,
});

async function askQuestion(question) { 
    return new Promise((resolve, reject) => {
      readline.question(question, (answer) => {
        resolve(answer);
      });
    });
  }
  
  async function main() {
    try {
      //Upload a file with an "assistants" purpose
      const file = await openai.files.create({
      file: fs.createReadStream("data/Beer_recipe_orignal.json"),
      purpose: "assistants",
      });

  /*async function main() {
    try {
      //Upload a file with an "assistants" purpose
      const path = require('path');
      const filePath = path.join(__dirname, 'data/all_modules.pdf');

      if (fs.existsSync(filePath)) {
        const file = await openai.files.create({
          file: fs.createReadStream(filePath),
          purpose: "assistants",
        });
      } else {
        console.error(`File not found: ${filePath}`);
      }*/    

      const assistant = await openai.beta.assistants.create({
        name: "Co-Lab Co-Pilot",
        instructions:
          "You are a personal assistant that helps students taking pathways courses with information relevant to their class.",
        tools: [{ "type": "retrieval"}], //provide the assistant with tools, such as documents 
        //make api call through the codeinterpreter, use weather data as testing 
        //i'm here for my shift and logs you in, office hours helper, figure out how retrieval works 
        model: "gpt-3.5-turbo-1106",
        file_ids: [file.id]
      });
  
      // Log the first greeting
      console.log(
        "\nHey, I'm your Co-Lab Co-Pilot! Ask me some questions!\n"
      );
  
      // Create a thread
      const thread = await openai.beta.threads.create(); //keeping track of context over time
  
      // Use keepAsking as state management for keep asking questions
      let keepAsking = true; 
      while (keepAsking) {
        const userQuestion = await askQuestion("\nHow can I help you?");
  
        // Pass in the user question into the existing thread
        await openai.beta.threads.messages.create(
          thread.id, 
          { //thread id is how we tell openai that we already have an exisiting thread and wish to use it as context
          role: "user", //user is providing some information 
          content: userQuestion, //this is what the user input as a question in the terminal 
        });
  
        // Use runs to wait for the assistant response and then retrieve it, this is openai executing whatever we've asked the assitant to do
        const run = await openai.beta.threads.runs.create(thread.id, {
          assistant_id: assistant.id,
        });
        // with assitants we have to setup a polling mechanism, we're setting run status as a function of openai.beta.threads.runs
        let runStatus = await openai.beta.threads.runs.retrieve(
          thread.id, //current thread we have 
          run.id //current run we're waiting for
        ); //trying to get status of a run to see if it is completed or running
  
        // Polling mechanism to see if runStatus is completed
        let maxRetries = 10; // maximum number of retries to prevent an infinite loop
        let retryCount = 0;
        
        while (runStatus.status !== "completed" && retryCount < maxRetries) {
          try {
            await new Promise((resolve) => setTimeout(resolve, 2000)); // wait for two seconds
            runStatus = await openai.beta.threads.runs.retrieve(thread.id, run.id); // check again until completed
          } catch (error) {
            console.error("Error while polling for completion:", error);
            break;
          }
          
          retryCount++;
        }
        
        if (runStatus.status !== "completed") {
          console.error("Task did not complete within the maximum number of retries.");
          console.log("\nTask did not complete. Please try again.\n");
    
        } else {
            console.log("\nTask completed successfully\n");
        }
        
  
        // get the last assistant message from the messages array we have, which contains all the questions and answers that we've had
        const messages = await openai.beta.threads.messages.list(thread.id);
  
        // find the last message for the current run
        const lastMessageForRun = messages.data
          .filter(
            (message) => message.run_id === run.id && message.role === "assistant" //we only want the most recent message from the assistant
          )
          .pop();
  
        // If an assistant message is found, console.log() it, this is the answer.
        if (lastMessageForRun) {
          console.log(`${lastMessageForRun.content[0].text.value} \n`);
        }
  
        // Ask if the user wants to ask another question and update keepAsking state
        const continueAsking = await askQuestion(
          "Do you have any other questions? (yes/no) "
        );
        keepAsking = continueAsking.toLowerCase() === "yes"; // we will loop everything again, we will now have all context available to us in the thread
  
        // If the keepAsking state is falsy show an ending message and terminate the code
        if (!keepAsking) {
          console.log("Alrighty then, I hope you learned something!\n");
        }
      }
  
      // close the readline
      readline.close();
    } catch (error) {
      console.error(error);
    }
  }
  
  // Call the main function
  main();