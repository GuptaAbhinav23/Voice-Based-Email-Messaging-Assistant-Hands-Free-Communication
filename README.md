# 🎤 Voice-Based Email Messaging Assistant - Hands-Free Communication

A sophisticated **Flask-based web application** that enables users to manage their emails and messages through **voice commands** and **biometric authentication** (face recognition). This application combines cutting-edge technologies like speech recognition, face verification, and Gmail API integration to provide a truly hands-free communication experience.

---

## 📋 Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Configuration](#configuration)
- [Usage](#usage)
- [Modules Overview](#modules-overview)
- [File Descriptions](#file-descriptions)
- [API Integrations](#api-integrations)
- [Database Schema](#database-schema)
- [Future Enhancements](#future-enhancements)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## ✨ Features

### 🔐 **Biometric Authentication**
- **Face Recognition Login** - Secure login using facial recognition via DeepFace
- **User Registration** - Capture and store facial features during registration
- **Face Verification** - Real-time face verification for authentication

### 🎤 **Voice Command Processing**
- **Speech-to-Text** - Convert voice commands to text using Google Speech Recognition
- **Text-to-Speech** - Convert email content to speech for audio feedback
- **Voice-based Email Control** - Compose, send, and read emails hands-free

### 📧 **Email Management**
- **Gmail Integration** - Full integration with Google Gmail API
- **Read Emails** - Listen to email content via text-to-speech
- **Send Emails** - Compose and send emails using voice commands
- **Inbox Management** - View and organize incoming emails
- **Sent Folder** - Track sent emails and messages

### 💬 **WhatsApp Integration**
- **Web-based WhatsApp Access** - Control WhatsApp via Selenium WebDriver
- **Automated Session Management** - Persistent WhatsApp Web sessions
- **Message Broadcasting** - Send messages through WhatsApp programmatically

### 🎯 **User Dashboard**
- **Multi-platform Support** - Switch between Gmail and WhatsApp
- **Voice Command Interface** - Intuitive voice-based navigation
- **Real-time Feedback** - Audio and visual feedback for all actions

---

## 🛠️ Technology Stack

### **Backend Framework**
- **Flask** - Lightweight Python web framework
- **Flask-Session** - Server-side session management
- **SQLite3** - Lightweight database for user credentials and settings

### **Computer Vision & Biometrics**
- **OpenCV (cv2)** - Image processing and camera access
- **DeepFace** - Face recognition and verification
- **RetinaFace** - Face detection backend
- **MTCNN** - Multi-task Cascaded Convolutional Networks for face detection
- **TensorFlow & Keras** - Deep learning framework for face recognition models

### **Speech Processing**
- **SpeechRecognition** - Speech-to-text conversion using Google Speech API
- **PyAudio** - Audio I/O for microphone access
- **gTTS (Google Text-to-Speech)** - Text-to-speech conversion
- **playsound** - Audio playback functionality

### **API Integrations**
- **Google API Client** - Gmail API for email management
- **Google Auth Libraries** - OAuth2 authentication for Google services
- **Selenium** - Browser automation for WhatsApp Web integration

### **Frontend**
- **HTML5** - Semantic markup
- **CSS3** - Responsive styling with custom stylesheets
- **JavaScript** - Interactive voice interface
- **Flask Jinja2 Templates** - Dynamic template rendering

### **Additional Libraries**
- **NumPy** - Numerical computing
- **Pillow (PIL)** - Image processing and manipulation
- **python-dotenv** - Environment variable management
- **requests** - HTTP library for API calls

---

## 📁 Project Structure

```
Voice-Based-Email-Messaging-Assistant/
│
├── app.py                          # Main Flask application entry point
├── requirements.txt                # Python dependencies
├── client_secret.json              # Google OAuth credentials (confidential)
├── whatsapp_api.py                 # WhatsApp Selenium integration
├── tempCodeRunnerFile.python       # Temporary code runner file
├── command.wav                     # Sample audio file
│
├── auth/                           # Authentication Module
│   ├── google_oauth.py            # Google OAuth2 login flow
│   ├── login.py                   # User login with face verification
│   └── register.py                # User registration and face capture
│
├── biometric/                      # Biometric Authentication Module
│   ├── capture_face.py            # Face capture from webcam
│   └── verify_face.py             # Face verification using DeepFace
│
├── database/                       # Database Module
│   ├── db.py                      # Database connection and table creation
│   └── users.db                   # SQLite database (auto-created)
│
├── gmail/                          # Gmail API Integration Module
│   ├── gmail_auth.py              # Gmail authentication and token management
│   ├── inbox.py                   # Retrieve emails from inbox
│   ├── read_mail.py               # Parse and read email content
│   └── send_mail.py               # Compose and send emails
│
├── voice/                          # Voice Processing Module
│   ├── speech_to_text.py          # Convert voice to text
│   └── text_to_speech.py          # Convert text to voice
│
├── biometric/                      # Biometric Data Storage
│   └── (user face images stored here)
│
├── static/                         # Frontend Static Files
│   ├── style.css                  # Main stylesheet
│   ├── dashboard.css              # Dashboard-specific styles
│   └── voice.js                   # Voice interface JavaScript
│
├── templates/                      # HTML Templates
│   ├── layout.html                # Base layout template
│   ├── login.html                 # Login page
│   ├── register.html              # Registration page
│   ├── dashboard.html             # Main dashboard
│   ├── platforms.html             # Platform selection (Gmail/WhatsApp)
│   ├── compose.html               # Email composition interface
│   ├── sent.html                  # Sent emails view
│   ├── whatsapp.html              # WhatsApp interface
│   └── inbox.html                 # Inbox view
│
├── chrome_data/                    # Chrome Browser Session Data
│   ├── First Run
│   ├── Local State
│   └── Default/
│       └── Preferences
│
├── .git/                           # Git version control
├── .github/                        # GitHub configuration
├── .gitignore                      # Git ignore rules
├── .venv/                          # Python virtual environment
└── __pycache__/                    # Python cache files
```

---

## 🚀 Installation & Setup

### **Prerequisites**
- Python 3.8 or higher
- pip (Python package manager)
- Webcam (for biometric authentication)
- Microphone and speakers (for voice commands)
- Google account with Gmail enabled
- Google Chrome browser (for WhatsApp integration)

### **Step 1: Clone the Repository**
```bash
git clone https://github.com/GuptaAbhinav23/Voice-Based-Email-Messaging-Assistant-Hands-Free-Communication.git
cd Voice-Based-Email-Messaging-Assistant-Hands-Free-Communication
```

### **Step 2: Create Virtual Environment**
```bash
# On Windows
python -m venv .venv
.\.venv\Scripts\activate

# On macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 4: Configure Google OAuth**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Desktop application)
5. Download credentials as JSON and save as `client_secret.json` in the project root
6. Ensure the `client_secret.json` file is in the application root directory

### **Step 5: Install PyAudio (if needed)**
```bash
# On Windows (requires Visual C++ build tools)
pip install pipwin
pipwin install pyaudio

# On macOS
brew install portaudio
pip install pyaudio

# On Linux
sudo apt-get install portaudio19-dev python3-pyaudio
```

### **Step 6: Run the Application**
```bash
python app.py
```

The application will be available at `http://localhost:5000`

---

## ⚙️ Configuration

### **Environment Variables**
Create a `.env` file in the root directory (optional):
```
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
```

### **Database Configuration**
The SQLite database is automatically created on first run. No manual configuration needed.

### **Speech Recognition Settings**
Located in `voice/speech_to_text.py`:
```python
r.pause_threshold = 1.2          # Pause time between words
r.phrase_threshold = 0.3         # Minimum phrase length
r.non_speaking_duration = 0.8    # Non-speaking duration
```

### **Face Recognition Models**
- **Face Detection**: RetinaFace (fast and accurate)
- **Face Recognition**: ArcFace (high accuracy)
- **Alternative backends**: MTCNN, OpenFace, VGGFace, Facenet

---

## 📖 Usage

### **1. User Registration**
- Open the application at `http://localhost:5000`
- Click "Register"
- Enter username, email, and password
- Allow camera access to capture facial image
- Click "Register" to complete

### **2. User Login**
- Enter username
- Allow camera access for face verification
- System verifies your face against stored image
- On successful verification, redirected to dashboard

### **3. Email Management**
- **Access Gmail**: Select "Gmail" from platforms
- **Send Email**: Use voice command "send email" and follow voice prompts
- **Read Emails**: Select email from inbox to listen to content
- **Compose**: Use voice commands to compose messages

### **4. WhatsApp Integration**
- Select "WhatsApp" from platforms
- Scan QR code on first login (if needed)
- Use voice commands to send messages
- Session is automatically saved for faster access

### **5. Voice Commands**
Examples of available voice commands:
```
"Send email to [recipient]"
"Read my inbox"
"Open Gmail"
"Compose new message"
"Read email from [sender]"
"Send WhatsApp message"
```

---

## 📚 Modules Overview

### **1. Authentication Module (`auth/`)**
Handles user authentication using both traditional credentials and biometric verification.

| File | Purpose |
|------|---------|
| `google_oauth.py` | OAuth2 flow for Google account integration |
| `login.py` | Face verification and session management |
| `register.py` | User registration and face storage |

### **2. Biometric Module (`biometric/`)**
Face recognition and verification using DeepFace.

| File | Purpose |
|------|---------|
| `capture_face.py` | Capture facial images from webcam |
| `verify_face.py` | Compare faces using DeepFace models |

### **3. Database Module (`database/`)**
SQLite database management for user data.

| File | Purpose |
|------|---------|
| `db.py` | Database connection, table creation, queries |

### **4. Gmail Module (`gmail/`)**
Complete Gmail API integration for email management.

| File | Purpose |
|------|---------|
| `gmail_auth.py` | Gmail authentication and token handling |
| `inbox.py` | Retrieve emails from Gmail inbox |
| `read_mail.py` | Parse and extract email content |
| `send_mail.py` | Compose and send emails via Gmail API |

### **5. Voice Module (`voice/`)**
Speech processing and audio conversion.

| File | Purpose |
|------|---------|
| `speech_to_text.py` | Convert voice commands to text using Google Speech API |
| `text_to_speech.py` | Convert text responses to speech using gTTS |

### **6. Frontend Module (`templates/` & `static/`)**
User interface and client-side functionality.

| File | Purpose |
|------|---------|
| `voice.js` | Voice interface and command handling |
| `style.css` | Global styling |
| `dashboard.css` | Dashboard-specific styling |
| Various `.html` files | Page templates for different views |

---

## 📄 File Descriptions

### **Core Application Files**

#### `app.py` - Main Application Entry Point
- Flask application setup
- Route definitions for all pages
- Session management
- Database initialization
- Integration of all modules

**Key Routes:**
- `/` - Home page
- `/register` - Registration page
- `/login` - Login page
- `/dashboard` - Main dashboard
- `/platforms` - Platform selection
- `/gmail/*` - Gmail-related routes
- `/whatsapp/*` - WhatsApp-related routes
- `/voice/*` - Voice command processing

#### `whatsapp_api.py` - WhatsApp Integration
- Selenium WebDriver setup
- WhatsApp Web automation
- Session management and persistence
- Message sending functionality
- QR code scanning

#### `requirements.txt` - Dependency List
All Python packages required for the application with specific versions.

#### `client_secret.json` - Google OAuth Credentials
⚠️ **CONFIDENTIAL** - Do NOT share or commit to version control
Contains OAuth2 credentials for Gmail API access.

---

## 🔌 API Integrations

### **Google Gmail API**
- **Authentication**: OAuth2.0 with InstalledAppFlow
- **Scopes**: 
  - `https://www.googleapis.com/auth/gmail.readonly` - Read emails
  - `https://www.googleapis.com/auth/gmail.send` - Send emails
  - `https://www.googleapis.com/auth/gmail.modify` - Modify emails

**Key Methods:**
- `users().messages().list()` - Retrieve messages
- `users().messages().get()` - Get message details
- `users().messages().send()` - Send messages

### **Google Speech-to-Text API**
- Uses SpeechRecognition library
- Automatically routes through Google's API
- Supports multiple languages (default: en-IN for Indian English)

### **Google Text-to-Speech API**
- Uses gTTS library for speech synthesis
- Generates MP3 audio files
- Supports multiple languages and accents

### **Face Recognition API**
- **DeepFace** - Face recognition and verification
- **RetinaFace** - Face detection
- Models used: ArcFace for recognition

---

## 💾 Database Schema

### **Users Table**
```sql
CREATE TABLE users (
    username TEXT PRIMARY KEY,
    email TEXT,
    password TEXT,
    face_path TEXT,
    gmail_token TEXT
);
```

**Columns:**
- `username` - Unique user identifier
- `email` - User's email address
- `password` - Hashed password (recommended to implement in production)
- `face_path` - Path to stored facial image file
- `gmail_token` - Serialized Gmail OAuth token

---

## 🎯 Future Enhancements

### **Security Improvements**
- [ ] Implement password hashing (bcrypt/argon2)
- [ ] Add email verification
- [ ] Implement two-factor authentication (2FA)
- [ ] Add rate limiting for API calls
- [ ] Encrypt sensitive data in database

### **Feature Additions**
- [ ] Multi-language support for voice commands
- [ ] Email attachment handling
- [ ] Calendar integration
- [ ] Task/reminder management via voice
- [ ] Email search functionality
- [ ] Scheduled email sending
- [ ] Email templates library
- [ ] Spam filtering and categorization

### **Platform Integration**
- [ ] Telegram bot integration
- [ ] Slack integration
- [ ] Microsoft Outlook integration
- [ ] Zoom meeting scheduling
- [ ] Google Meet integration

### **Performance & Optimization**
- [ ] Caching mechanism for emails
- [ ] Async processing for heavy operations
- [ ] Database optimization and indexing
- [ ] Frontend performance improvements
- [ ] Implement Redis for session management

### **User Experience**
- [ ] Voice command history
- [ ] Custom voice profiles
- [ ] Accessibility improvements
- [ ] Dark mode support
- [ ] Mobile app version
- [ ] Real-time notifications

### **Testing & Documentation**
- [ ] Unit tests for all modules
- [ ] Integration tests
- [ ] API documentation (Swagger/OpenAPI)
- [ ] Video tutorials
- [ ] Deployment guides

---

## 🔧 Troubleshooting

### **Microphone Not Detected**
```bash
# Check if PyAudio is properly installed
python -c "import pyaudio; print('PyAudio installed correctly')"

# Reinstall PyAudio
pip uninstall pyaudio
pip install pyaudio
```

### **Camera Issues**
```python
# Test camera access
import cv2
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
print("Camera working" if ret else "Camera failed")
cap.release()
```

### **Gmail API Authentication Failed**
- Delete existing `token.pickle` file
- Re-authenticate with `client_secret.json`
- Ensure credentials file has correct OAuth2 scopes

### **Face Recognition Not Working**
- Ensure adequate lighting
- Face should be clearly visible
- Check if `faces/` directory has sufficient storage
- Verify DeepFace models are downloaded (first run auto-downloads)

### **Speech Recognition Not Working**
- Check internet connection (Google Speech API requires it)
- Test microphone: `python -m speech_recognition`
- Verify audio input levels in system settings
- Try different microphone if available

### **WhatsApp Session Issues**
- Delete `whatsapp_session.pkl` file to force re-login
- Clear `chrome_data/` folder for fresh session
- Ensure Chrome browser is installed
- Check Chrome version compatibility

### **Database Errors**
```python
# Reset database
import os
from database.db import DB_NAME
os.remove(DB_NAME)
# Re-run app to recreate tables
```

### **Port Already in Use**
```bash
# Change port in app.py
app.run(debug=True, port=5001)  # Use different port
```

---

## 📊 Performance Tips

1. **Speech Recognition**
   - Ensure quiet environment for better accuracy
   - Speak clearly and naturally
   - Adjust pause_threshold based on speech pace

2. **Face Recognition**
   - Ensure adequate lighting
   - Keep face at camera distance (30-60 cm)
   - Remove sunglasses and obstructions

3. **Email Performance**
   - Limit emails retrieved per request (use maxResults)
   - Implement pagination for large inboxes
   - Cache frequently accessed emails

4. **Database**
   - Add indexes on frequently queried columns
   - Regular database maintenance
   - Archive old records periodically

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure:
- Code follows PEP 8 style guidelines
- All tests pass
- Documentation is updated
- No sensitive credentials are committed

---

## ⚖️ License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💼 Author

**Abhinav Gupta**
- GitHub: [@GuptaAbhinav23](https://github.com/GuptaAbhinav23)
- Repository: [Voice-Based-Email-Messaging-Assistant](https://github.com/GuptaAbhinav23/Voice-Based-Email-Messaging-Assistant-Hands-Free-Communication)

---

## 📞 Support

For issues, questions, or suggestions:
1. Open an issue on [GitHub Issues](https://github.com/GuptaAbhinav23/Voice-Based-Email-Messaging-Assistant-Hands-Free-Communication/issues)
2. Include detailed description and steps to reproduce
3. Provide error messages and logs

---

## 🙏 Acknowledgments

- Google Cloud Platform for Gmail API
- DeepFace team for face recognition models
- SpeechRecognition library community
- Flask framework and community
- All contributors and users

---

## ⚠️ Important Security Notes

1. **Never commit `client_secret.json`** to version control
2. **Never hardcode credentials** in the code
3. **Use environment variables** for sensitive data
4. **Implement password hashing** before production deployment
5. **Use HTTPS** in production environment
6. **Regularly update dependencies** for security patches
7. **Add proper logging** without logging sensitive data
8. **Implement rate limiting** to prevent abuse

---

## 📝 Changelog

### Version 1.0.0 (Initial Release)
- User registration and login with face recognition
- Gmail integration for email management
- Voice command processing (speech-to-text)
- Text-to-speech for email content
- WhatsApp Web integration
- Multi-platform dashboard
- Real-time voice interface

---

**Last Updated**: 2026-08-18
**Status**: Active Development
**Python Version**: 3.8+
**License**: MIT

---

*For more information, visit the [GitHub repository](https://github.com/GuptaAbhinav23/Voice-Based-Email-Messaging-Assistant-Hands-Free-Communication)*
