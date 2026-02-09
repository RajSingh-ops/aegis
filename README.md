# AEGIS - Multimodal Regulatory Auditor

**AEGIS** (Advanced Evaluation and Governance Intelligence System) is a real-time AI-powered regulatory auditor built on the Sentinel Architecture using Django, Channels, and Google Gemini.

## 🎯 What It Does

AEGIS monitors multimodal inputs (video, audio, text) to detect safety violations and ensure regulatory compliance in real-time. Perfect for:
- 🏥 Surgical safety monitoring
- 🏭 Manufacturing compliance
- 🔬 Laboratory protocol enforcement
- 🏗️ Critical infrastructure oversight

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip
- Google Gemini API Key

### Installation

```bash
# Navigate to project directory
cd geminihackethon

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (REQUIRED)
# Create a file named .env in the project root with:
# GEMINI_API_KEY=your_api_key_here
# GEMINI_MODEL=gemini-2.0-flash-exp
# DEBUG=True
# See "Setting Up Gemini API" section below for details

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### Setting Up Gemini API

> **⚠️ SECURITY NOTE**: The `.env` file is NOT included in this repository for security reasons. You must create your own.

1. **Get Your API Key**: Visit https://aistudio.google.com/app/apikey
2. **Sign in** with your Google account
3. Click **"Get API Key"** or **"Create API Key"**
4. **Copy the key** (starts with `AIza...`)

5. **Create `.env` file** in the project root directory:

```env
# .env file - DO NOT commit to Git!
GEMINI_API_KEY=AIza_your_actual_api_key_here
GEMINI_MODEL=gemini-2.0-flash-exp
DEBUG=True
SECRET_KEY=django-insecure-bjf#!8=3hnua7jz&y0!$vmn#r*i%ib@x$q1g5kli%6&eys!kt7
```

> **Note**: The `.env` file is already in `.gitignore` to prevent accidental commits.

6. **Restart the server**:
```bash
python manage.py runserver
```

### Access the Application

- **Dashboard**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/
- **WebSocket**: ws://localhost:8000/ws/auditor/

## 🏗️ Architecture

### Sentinel Architecture Pillars

1. **Massive Context Grounding** (2M Token Window)
   - Ingests entire regulatory documents
   - No traditional RAG needed
   - Full knowledge base in context

2. **Stateful Agentic Reasoning** ("Deep Think")
   - Maintains reasoning state via thought signatures
   - Multi-step analysis before decisions
   - Context-aware responses

3. **Real-Time Multimodal Feedback**
   - WebSocket-based communication
   - Video/audio/text processing
   - Instant alerts for critical events

4. **Operational Analytics**
   - Automatic deviation logging
   - Severity-based categorization
   - BigQuery integration for enterprise analytics

### Django Apps

- **core_auditor**: Main application with AI orchestrator and WebSocket handlers
- **analytics**: Deviation tracking and reporting
- **knowledge_vault**: Regulatory knowledge base management

## 📁 Project Structure

```
geminihackethon/
├── aegis_core/              # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── asgi.py             # ASGI config for WebSockets
├── core_auditor/            # Main application
│   ├── services/           # Business logic
│   │   ├── orchestrator.py # AI reasoning engine
│   │   ├── gemini_client.py # Gemini API wrapper
│   │   └── tools.py        # Function calling tools
│   ├── websockets/         # WebSocket handlers
│   │   ├── consumers.py    # WebSocket consumer
│   │   └── routing.py      # WebSocket URL routing
│   ├── templates/          # App templates
│   ├── static/             # App static files
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── analytics/              # Data & reporting
│   ├── models.py          # Deviation model
│   └── bigquery_client.py
├── knowledge_vault/        # Knowledge base
│   └── ingest.py          # Document ingestion
└── manage.py
```

## 🎮 Using the Dashboard

### Testing Safety Detection

1. Navigate to http://localhost:8000/
2. Use the simulation input field to send test events

**Example 1: Detect Safety Violation**
```
unsafe instrument detected in sterile field
```
- AI analyzes the event
- Logs HIGH severity deviation
- Shows decision in log
- Saves to database

**Example 2: Search Safety Protocols**
```
check protocol for sterile field procedures
```
- AI searches knowledge vault
- Returns relevant safety protocols
- Displays results in log

**Example 3: General Monitoring**
```
monitoring surgical procedure room 3
```
- AI acknowledges monitoring request
- Shows active watching status
- Logs the activity

### Dashboard Components

**Left Sidebar - System Status**
- **Model Context**: AI memory usage (2M token capacity)
- **Latency**: Response time metrics
- **Deviations (24h)**: Safety issues detected today
- **Active Policies**: Currently monitored safety rules

**Center Panel - Live Feed**
- Video stream area (placeholder in demo mode)
- Simulation input for testing

**Right Panel - Decision Log**
- Real-time AI decisions
- Color-coded by severity (Green/Yellow/Red)
- Thought signatures showing AI reasoning

## 🔧 Technology Stack

- **Backend**: Django 5.0+, Django Channels, Daphne
- **AI**: Google Gemini 1.5 Pro / 2.0
- **Database**: SQLite (dev), PostgreSQL (production)
- **Analytics**: Google Cloud BigQuery
- **Frontend**: Vanilla JavaScript, CSS3

## 📊 Key Features

- ✅ Real-time WebSocket communication
- ✅ AI-powered safety monitoring
- ✅ Automatic deviation logging with severity levels
- ✅ Knowledge vault for regulatory protocols
- ✅ Modern cyberpunk-themed dashboard
- ✅ Tool execution (function calling)
- ✅ Stateful reasoning with thought signatures

## 🛠️ Troubleshooting

### Dashboard won't load
1. Check if server is running
2. Look for: `Starting development server at http://127.0.0.1:8000/`
3. If not running: `python manage.py runserver`

### WebSocket shows "OFFLINE"
1. Refresh the page
2. Check server is running
3. Use `http://localhost:8000` (not `127.0.0.1`)

### "Simulation mode" message
1. Check `.env` file exists in project root
2. Verify `GEMINI_API_KEY=` has your actual key
3. Ensure no spaces around the `=`
4. Restart the server

### "API key not valid"
1. Go to Google AI Studio
2. Create a new API key
3. Update `.env` file
4. Restart server

## 📝 Environment Variables

Create a `.env` file for production:

```env
DJANGO_SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-2.0-flash-exp
BIGQUERY_PROJECT_ID=your-project-id
```

### Recommended Gemini Models

**gemini-2.0-flash-exp** (Default)
- Fastest responses
- Supports function calling
- Multimodal (text, images, video)
- Free tier available

**gemini-1.5-pro-latest**
- 2M token context window
- Best for knowledge grounding
- Most capable reasoning
- Slower, more expensive

**gemini-1.5-flash**
- Balanced speed/capability
- Good for most use cases
- Lower cost

## 🔮 Future Enhancements

- [ ] Real camera/microphone integration
- [ ] Multi-stream monitoring
- [ ] Advanced analytics dashboard
- [ ] Mobile app for alerts
- [ ] Custom model fine-tuning

## 🤝 Contributing

This is a hackathon project demonstrating the Sentinel Architecture. Feel free to fork and extend!

## 📄 License

MIT License - See LICENSE file for details

---

**Built with ❤️ using Django and Google Gemini for Gemini Hackathon**
