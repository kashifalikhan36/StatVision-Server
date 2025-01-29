# Blessi-AI-Server

## Introduction
*Blessi-AI* is a powerful, multilingual voice assistant that communicates in a human-friendly manner across different moods such as happy, sad, laughing, and angry. More than just a voice assistant, Blessi-AI can remember what you tell her and remind you whenever you need. She can also send emails in any language, perform web scraping to gather relevant information, and provide comprehensive responses based on what she learns.

## Demo Video
Check out the demo of Blessi-AI in action!

[![Blessi-AI Demo](https://img.youtube.com/vi/OyDJ7AkI3zU/0.jpg)](https://www.youtube.com/watch?v=OyDJ7AkI3zU)

## Blessi-AI GUI Application
Blessi-AI also comes with a graphical user interface (GUI) that enhances the user experience. You can run and interact with the application seamlessly.

For more details and to access the GUI app, visit the following repository:

[Blessi-AI GUI App](https://github.com/kashifalikhan36/Bless-AI)

## Live Hosted Version
You can access the live version of Blessi-AI at the following link:

[Blessi-AI Live](https://blessi.xyz)

## Features
- **Multilingual Support**: Speaks fluently in any language of your choice.
- **Mood Variability**: Adapts to various emotional states, making interactions more engaging (e.g., happy, sad, laughing).
- **Memory Capability**: Remembers user inputs and can remind you upon request.
- **Email Functionality**: Composes and sends emails in any language through voice commands.
- **Web Scraping**: Finds and analyzes relevant data from the web to provide useful insights.
- **Easy Integration**: Simple setup using Python and Azure services.

## How to Use Blessi-AI
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/Blessi-AI.git
   cd Blessi-AI
2. **Set up your credentials: Open blessi.py and enter your Azure and email credentials:**:
   ```bash
   mail_password = 'your_mail_password'
   mail_sender_email = 'your_email@example.com'
  
   api_key = 'your_openai_api_key'
   azure_model_endpoint = 'your_azure_model_endpoint'
   api_version = 'your_api_version'
  
   speech_subscription = 'your_speech_subscription'
   speech_model_region = 'your_speech_model_region's

3. **Run the API server locally: Open your terminal and run:**:
   ```bash
   uvicorn app:app --host 127.0.0.1 --port 8000 --reload
4. **(Optional) Set up for HTTPS on a virtual server:**:
- Generate a certificate for your custom domain.
- Place keyfile.pem in the local directory of Blessi-AI.
- Run the server with HTTPS support:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 443 --ssl-certfile yoursslcertificate.pem

## Requirements
- Python 3.x
- Microsoft Azure account for generating the required credentials.
- Dependencies listed in requirements.txt

## Customization
- Modify speech.py to customize the language, tone, or features.
- You can connect your own model by just Fine-tuning llm on azure

## Disclaimer
- Blessi-AI should be used responsibly, and user-provided credentials should be kept secure. Ensure compliance with data privacy laws and do not share your credentials publicly.

## License
- MIT License. See the LICENSE file for more information.

## Contributions
- We welcome contributions! Feel free to submit issues, contribute new features, or improve the existing code.
- Adjust the user interface and server configurations to fit your project requirements.
