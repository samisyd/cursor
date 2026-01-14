# Gemini Chatbot with Streamlit

A conversational question-answer chatbot built with Streamlit and Google's Gemini Pro API. The chatbot automatically saves all conversations and displays them in a beautiful chat interface.

## Features

- 💬 Conversational Q&A chatbot using Gemini Pro
- 💾 Automatic chat history saving (JSON format)
- 📜 Display complete chat history in the UI
- 🗑️ Clear chat history option
- 📥 Download chat history as JSON
- 🔒 Secure API key management

## Setup

### 1. Install Dependencies

First, activate your virtual environment and install the required packages:

```bash
# Activate virtual environment (Windows)
.venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt
```

### 2. Get Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

### 3. Configure API Key

You have two options:

**Option A: Environment Variable (Recommended)**
- Create a `.env` file in the project root
- Add your API key:
  ```
  GEMINI_API_KEY=your_api_key_here
  ```

**Option B: Sidebar Input**
- Run the app and enter your API key in the sidebar

### 4. Run the Application

```bash
streamlit run chatbot.py
```

The app will open in your default web browser at `http://localhost:8501`

## Usage

1. Enter your Gemini API key (if not set in `.env`)
2. Start chatting by typing your question in the chat input
3. The chatbot will respond using Gemini Pro
4. All conversations are automatically saved to `chat_history.json`
5. Chat history persists across sessions

## Features Explained

- **Chat History**: All conversations are saved in `chat_history.json` in the project folder
- **Clear History**: Use the "Clear Chat History" button in the sidebar to reset
- **Download History**: Download your chat history as a JSON file
- **Timestamps**: Each message includes a timestamp for reference

## File Structure

```
Project1/
├── .venv/              # Virtual environment
├── chatbot.py          # Main Streamlit application
├── requirements.txt    # Python dependencies
├── chat_history.json   # Saved chat history (auto-generated)
├── .env               # API key configuration (optional)
└── README.md          # This file
```

## Requirements

- Python 3.8+
- Streamlit
- google-generativeai
- python-dotenv

## Notes

- The chat history is saved locally in JSON format
- API key is stored securely (not in code)
- The chatbot uses Gemini Pro model with optimized settings
- All conversations include timestamps
