# StatVision

StatCast is an AI-powered web app that provides MLB stats and generates videos from YouTube URLs. It fetches player data such as Exit Velocity, Hit Distance, and more, then generates a video based on the input, allowing playback and download options.

## Features
- Fetch MLB player data from YouTube videos.
- Display key stats: Exit Velocity, Hit Distance, Launch Angle, and more.
- Generate and play videos directly in the app.
- Option to download the generated video.
- Sleek, MLB-inspired design with smooth animations.
- Mobile-responsive and user-friendly interface.

## Tech Stack
- FastAPI (Backend)
- HTML, CSS, JavaScript (Frontend)
- API endpoints: `/audio/url-to-speech/` and `/audio/url-to-video/`

## Prerequisites
Before running the app, you need to authenticate with the Google Gemini API. Follow these steps:

1. **Install Google Cloud CLI**  
   To interact with Google APIs, you'll need to install the Google Cloud CLI. You can do this by following the instructions in the official [Google Cloud CLI documentation](https://cloud.google.com/sdk/docs/install).

2. **Set up Google Gemini API**  
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Enable the **Google Gemini API** for your project.
   - Generate and download the API credentials (JSON file) for authentication.

3. **Authenticate with the API**  
   Once you've set up the API and downloaded your credentials, authenticate your CLI with the following command:
   ```bash
   gcloud auth activate-service-account --key-file=path-to-your-credentials-file.json

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/statcast.git
   ```
2. Navigate to the project folder:
   ```bash
   cd statcast
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

## Usage
1. Enter a YouTube URL in the input field.
2. Wait as the app fetches stats and generates the video.
3. Once the video is ready, it will be displayed with playback controls and a download option.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- FastAPI for the backend.
- Google Gemini API for providing advanced data insights.
- The MLB community for inspiring the design and data.
```
