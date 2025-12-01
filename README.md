
# TaskFlow AI - Multi-Channel Task Management System

## Overview
TaskFlow AI is a multi-agent system that processes tasks from multiple input channels (text, email, voice) and organizes them in Vikunja with intelligent enrichment and color-coding.

## Architecture

### Core Components
1. **Input Processor** - Handles text, email, and voice inputs
2. **Parser Agent** - Extracts structured task data using Gemini LLM
3. **Enricher Agent** - Enhances tasks with context and patterns
4. **Vikunja Agent** - Creates tasks in Vikunja with color-coding
5. **Orchestrator** - Coordinates multi-agent workflow

### Tools
- **Gemini LLM Service** - Task extraction and enrichment
- **Vikunja API Client** - Task management integration
- **Email Tools** - Email parsing
- **Voice Tools** - Audio transcription (mock mode)

### Block Diagram
```
INPUT SOURCES
    │
    ├─ TEXT INPUT
    ├─ EMAIL INPUT
    └─ VOICE INPUT
    │
    ▼
INPUT PROCESSOR
(Normalize & validate)
    │
    ▼
PARSER AGENT
(Extract with Gemini)
    │
    ▼
ENRICHER AGENT
(Enhance with context)
    │
    ▼
VIKUNJA AGENT
(Create tasks with colors)
    │
    ▼
VIKUNJA DATABASE
(Tasks stored)
    │
    ▼
SESSION MEMORY
(Learn patterns)
```

## Features
- [x] Multi-channel input (text, email, voice)
- [x] Intelligent task extraction with Gemini 2.5 Flash
- [x] Context-based task enrichment
- [x] Color-coded tasks by input source
- [x] Session memory with pattern learning
- [x] Structured JSON logging
- [x] OpenTelemetry tracing support
- [x] Error handling & graceful degradation

## Color Scheme
- 🔵 **Dark Blue** (#03346E) - Voice input
- 🟣 **Plum** (#8C3061) - Email input
- 🟦 **Dark Teal** (#1A3636) - Text input

## Setup

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Gemini API key: https://makersuite.google.com/app/apikey

### Installation

1. Clone repository:
```bash
git clone <your-repo>
cd taskflow-ai
```

2. Create .env file:
```bash
cp .env.example .env
# Edit .env with your credentials
```

3. Start Vikunja:
```bash
docker-compose up -d
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run:
```bash
python main.py
```

## Demo

Run the interactive demo:
```bash
python demo.py
```

Expected output:
- 3 sample tasks created
- Color-coded in Vikunja dashboard
- Logs showing extraction and enrichment

## Project Structure
```
taskflow-ai
├─ agents
│  ├─ enricher_agent.py
│  ├─ input_processor.py
│  ├─ orchestrator.py
│  ├─ parser_agent.py
│  ├─ vikunja_agent.py
│  └─ __init__.py
├─ config.py
├─ demo.py
├─ docker-compose.yml
├─ images
│  ├─ taskflow_vikunja_screenshot_1.png
│  └─ taskflow_vikunja_screenshot_2.png
├─ LICENSE
├─ main.py
├─ README.md
├─ requirements.txt
├─ tools
│  ├─ email_tools.py
│  ├─ gemini_tools.py
│  ├─ vikunja_api.py
│  ├─ voice_tools.py
│  └─ __init__.py
└─ utils
   ├─ logger.py
   ├─ memory.py
   ├─ tracing.py
   └─ __init__.py
```

## Course Concepts Covered

| Day | Concept | Implementation |
|-----|---------|-----------------|
| **Day 1** | Multi-agent Architecture | 5 specialized agents |
| **Day 2** | Tools & Integration | 4 tools with Gemini & Vikunja |
| **Day 3** | Context & Memory | SessionMemory with pattern learning |
| **Day 4** | Quality & Observability | JSON logging + OpenTelemetry tracing |
| **Day 5** | Production Deployment | Error handling, graceful degradation, containerization |

## Troubleshooting

### Vikunja 404 Error
- Ensure VIKUNJA_PROJECT_ID=18 in .env
- Verify Vikunja is running: docker-compose ps

### Gemini API Error
- Verify GEMINI_API_KEY is set correctly
- Key should start with "AIza"

### Tasks not appearing in Vikunja
- Check logs for errors
- Verify Vikunja credentials in .env
- Ensure project exists in Vikunja

## Performance Notes
- First task extraction: 2-3 seconds (Gemini API)
- Subsequent tasks: 1-2 seconds
- Total session: ~5 seconds for 3 tasks

## Future Enhancements
- Real voice transcription (Whisper API)
- Task scheduling and reminders
- Team collaboration features
- Advanced analytics and reporting
