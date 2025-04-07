# AI Personal Email Assistant

Hello guys, I have built a project which is - 
**An AI-powered personal email assistant** capable of reading a user's
Gmail/IMAP inbox, understanding email context, storing emails in a database, and
interacting with external tools (web search, Slack, calendar) to assist with email actions.
The assistant should be able to automatically draft or send replies, forward information,
and schedule events based on email content.

## Technology Stack Used
* Frontend -> **Next.js**
* Backend -> **Flask & Ngrok**
* Database -> **Postgresql**
* LLM Model -> **Mistral**
* Building LLM -> **Google Colab**

In this project, I have used Next.js for building the frontend. The frontend is simple as it is serving the purpose of only interface so nothing fancy UI/UX is applied :).</br>
For backend I have used Flask  as it is a project related to AI. It's easy to work with python by using flask! </br>
For database I have used Postgresql due its compatibilty with AI models! </br>
Most importantly, I have used Google Colab to train the LLM as my pc can't comprehend the large models ;)P</br>
Because I am using google colab I had to run 3 servers in order to maintain the proper flow of the data over the APIS:
1. Flask server on the Vscode (local)
2. Flask server on the Google Colab
3. Ngrok tunne which acted as a bridge between Vscode and Colab

## Architecture
[architecture diagram.pdf](https://github.com/user-attachments/files/19640301/architecture.diagram.pdf)

![architecture diagram](https://github.com/user-attachments/assets/0469d26f-eb10-4835-a37b-925b83e6e455)


The architecture is kinda complex but not that difficult to interpret. The browser is showing a simple interface of a chat with AI. It is getting the code of the UI from the client folder which made by Next.js.
The client is getting responses of the AI-model(LLM) from the server which is connected with the google colab - on which the LLM is trained. There are 3 servers running, one is on the local that is vscode, second 
is on the google colab and the third is the Ngrok which is connecting vscode with colab - LLM with the server! </br>
Both servers on local and on colab are connected to the databse, only difference is that colab is getting data from the databse via Ngrok! Further, the local server is using Gmail API - to read/send emails, Slack API - to send alerts on channels, 
Calendar API - to schedule meetings on the calendar and lastly Google Web Search API - which is used to answer question which are not found in the emails!

## Instructions To set up Gmail API
1. Go to Google Cloud Console.

2. Create a new project and enable the Gmail API.

3. Set up the OAuth consent screen and add yourself as a test user.

4. Create OAuth 2.0 Credentials (choose "Desktop App") and download credentials.json.

5. Place credentials.json in your server directory.

6. Install required packages:
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
7. Run your script to generate token.json (it will open a browser to authenticate your Google account).

## Instructions to set up Slack API
1. Go to Slack API: Your Apps.

2. Click "Create New App" → Choose "From Scratch".

3. Give it a name and select your workspace.

4. Under OAuth & Permissions, add the required scopes (e.g., chat:write, channels:read).

5. Install the app to your workspace and copy your Bot User OAuth Token.

6.Add the token to your environment (e.g., .env file):
SLACK_BOT_TOKEN=xoxb-your-token

7.Use slack_sdk to send messages:
pip install slack-sdk

## Instructions to set up Calendar API
1. Go to Google Cloud Console.
2. Create/select your project and enable the Google Calendar API.

## Instructions to set up Google Web Search API
1. Go to Google Programmable Search Engine.

2. Create a new search engine (choose to search the entire web or specific sites).

3. Note down the Search Engine ID (CX).

4. Go to Google Cloud Console → Create a new project and enable Custom Search API.

5. Create an API key under Credentials.

6. Add both to your environment:
GOOGLE_API_KEY=your-api-key
GOOGLE_CSE_ID=your-search-engine-id

## Simplified Overall Explanation

The AI is first getting the emails from the gmail account with the help of **Gmail API** and then storing it in the **Postgresql**. This happens when the local server starts running. Then this data is converted 
into csv file and feeded to the LLM model on the colab with the help of **Ngrok**. Then LLM with RAG is used to answer user's question based on the emails! If LLM is not able to answer question from the emails or the 
question is not based on the emails then it will fetch the answer from the web. If the response contains anything about meetings and if the meetings details are given in the email then it will automatically schdeule the 
meeting on google calendar and will send the confirmation email to the sender of the meeting email asserting about the meeting. If the response contains any emails which are marked urgent or important then it will send an alert to the slack channel.
This is how the AI is working.


## Challenges Encountered

Writing the overall explanation I realised it has very few functionalities but implementing them was difficult. Especially, when you have to implement code on colab and vscode! </br>
</br>
The main challenge was to keep the vscode and colab linked together. Had to restart all the servers again and again even when a small change was made!</br>
</br>
Another challenge was connecting with Gmail API and writing code for reading and sending emails via your personal apps. I read many blogs and watched 2-3 videos in order to build the code for it. This was one of the most time consuming task
because we are not sending the message manualy but our LLM model is going to send it so it had to be programmed with specific instructions.
</br>
</br>
Another challenge was that LLM implementaion. Tried 4-5 different models but they were getting too much off the shore! Finally, read about Mistral model on some blog post and then went to thier website and they had
already given simple and most efficient code to use their model. The model was so perfect that right off the bat it started answering the questions based on the email's vector database.</br>
</br> 
But the challenge with LLM was not completed yet! As the model is free it kept getting rate limit reach error. So had to take Chatgpt's help in order to solve the issue. It provided timer before each repsonse to avoid getting rate limit error.
</br>
</br>
The overall challenge is that I am still new with machine learning! and implementing all this seemed very difficult at first. But eventually, completing small small task one by one I was able to build and complete this project!

## Setup and Usage

In order to run this project, I think u just have to clone this repository then get all the API credentials and download all the dependencies. Run the colab file on google colab and start client and server on the vscode.
Also, you will need to install Ngrok on the local machine and you will be able to use this AI with your Email Account!
