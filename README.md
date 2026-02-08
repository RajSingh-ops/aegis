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

### Installation

```bash
# Clone the repository
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

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start development server
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
│   │   └── tools.py        # Function calling tools
│   ├── websockets/         # WebSocket handlers
│   │   ├── consumers.py    # WebSocket consumer
│   │   └── routing.py      # WebSocket URL routing
│   ├── templates/          # App templates
│   │   └── core_auditor/
│   │       ├── base.html
│   │       └── dashboard.html
│   ├── static/             # App static files
│   │   └── core_auditor/
│   │       ├── css/
│   │       └── js/
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

## 🧪 Testing

### Simulation Mode

The dashboard includes a simulation input for testing:

1. Navigate to http://localhost:8000/
2. Use the input field to send test events:
   - `"unsafe instrument detected"` → Triggers deviation logging
   - `"check protocol for sterile field"` → Triggers knowledge vault search
   - Any other text → Acknowledged and monitored

### WebSocket Testing

Open browser DevTools → Network → WS tab to monitor WebSocket connection and messages.

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

## 🔮 Future Enhancements

- [ ] Real camera/microphone integration
- [ ] Multi-stream monitoring
- [ ] Advanced analytics dashboard
- [ ] Mobile app for alerts
- [ ] Custom model fine-tuning

## 📝 Environment Variables

Create a `.env` file for production:

```env
DJANGO_SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
GOOGLE_API_KEY=your-gemini-api-key
BIGQUERY_PROJECT_ID=your-project-id
```

## 🤝 Contributing

This is a hackathon project demonstrating the Sentinel Architecture. Feel free to fork and extend!

## 📄 License

MIT License - See LICENSE file for details

## 🆘 Support

For issues or questions, please open an issue on GitHub.

---

**Built with ❤️ using Django and Google Gemini**
