# LIA Core™ Conversational Module Documentation

## Overview

The **LIA Core™ Conversational Module** is an advanced AI-powered chat interface that provides natural language interaction with your wearable biosignal monitoring system. It integrates OpenAI's GPT-4o-mini model with real-time biosignal data from the Clarity™, iFRS™, and Timesystems™ proprietary processing layers.

## Features

- **Natural Language Health Analysis**: Ask questions about your health in plain English and receive personalized insights
- **Real-time Biosignal Context**: LIA has access to your current heart rate, SpO2, temperature, activity, HRV, circadian rhythm, and more
- **Conversational Memory**: Maintains conversation context across multiple messages within a session
- **Multi-dimensional Insights**: Analyzes data from all three proprietary layers (Clarity™, iFRS™, Timesystems™)
- **Personalized Recommendations**: Provides actionable health advice based on your current state
- **Flexible Context Mode**: Chat with or without biosignal data depending on your needs

## Architecture

```
User Message → LIA Chat Engine → OpenAI GPT-4o-mini
                      ↓
            Biosignal Context (optional)
                      ↓
     ┌────────────────┴────────────────┐
     │                                 │
Clarity™ Layer              iFRS™ Layer           Timesystems™ Layer
(Signal Quality)      (HRV & Frequency)         (Circadian Rhythm)
     │                        │                        │
     └────────────────────────┴────────────────────────┘
                              ↓
                      LIA Insights
                              ↓
                    AI-Powered Response
```

## API Endpoints

### 1. Chat with LIA

**POST** `/api/v1/chat`

Engage in a conversation with LIA about your health.

**Request Body:**
```json
{
  "message": "How is my heart rate variability?",
  "session_id": "user_123",  // Optional, defaults to "default"
  "include_biosignal_context": true  // Optional, defaults to true
}
```

**Response:**
```json
{
  "success": true,
  "response": "Your heart rate variability (HRV) is looking excellent! Your HRV score is 75.0/100...",
  "timestamp": "2025-10-21T12:30:45.123456",
  "session_id": "user_123",
  "tokens_used": 245,
  "model": "gpt-4o-mini",
  "error": null
}
```

**Example with curl:**
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello! Can you tell me about my current health status?",
    "session_id": "test_user_001",
    "include_biosignal_context": true
  }'
```

### 2. Get Conversation History

**GET** `/api/v1/chat/history/{session_id}`

Retrieve the conversation history for a specific session.

**Response:**
```json
{
  "session_id": "user_123",
  "history": [
    {
      "role": "user",
      "content": "How is my HRV?"
    },
    {
      "role": "assistant",
      "content": "Your HRV score is 75.0/100..."
    }
  ],
  "message_count": 2
}
```

**Example with curl:**
```bash
curl http://localhost:8000/api/v1/chat/history/test_user_001
```

### 3. Clear Conversation History

**DELETE** `/api/v1/chat/history/{session_id}`

Delete all conversation history for a session.

**Response:**
```json
{
  "success": true,
  "message": "Conversation history cleared for session: user_123"
}
```

**Example with curl:**
```bash
curl -X DELETE http://localhost:8000/api/v1/chat/history/test_user_001
```

## Biosignal Context

When `include_biosignal_context` is set to `true`, LIA receives comprehensive real-time data:

### Raw Signals
- Heart Rate (BPM)
- Blood Oxygen Saturation (SpO2 %)
- Body Temperature (°C)
- Activity Level (steps/min)

### Clarity™ Layer
- Overall Quality Score (0-1)
- Signal-to-Noise Ratio (dB)
- Quality Assessment (excellent/good/fair/poor)
- Detected Artifacts

### iFRS™ Layer
- Dominant Frequency (Hz)
- Rhythm Classification (normal_sinus, elevated, low, irregular, athletic)
- HRV Score (0-100)
- HRV Metrics (RMSSD, SDNN, pNN50)
- LF/HF Ratio
- Respiratory Rate

### Timesystems™ Layer
- Pattern Type (stable, increasing, decreasing, oscillating, irregular)
- Circadian Phase (morning, afternoon, evening, night)
- Temporal Consistency Score (0-1)
- Rhythm Score (0-100)
- Circadian Alignment Score (0-1)

### LIA Health Insights
- Detected Health Condition
- Confidence Level (0-1)
- Overall Wellness Score (0-100)
- Wellness Breakdown (cardiovascular, respiratory, activity, stress)
- Risk Factors
- Positive Indicators
- Personalized Recommendations

## Example Use Cases

### 1. Health Status Check
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How am I doing right now?",
    "session_id": "user_001",
    "include_biosignal_context": true
  }'
```

### 2. Understanding Metrics
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What does my LF/HF ratio mean?",
    "session_id": "user_001",
    "include_biosignal_context": true
  }'
```

### 3. Activity Recommendations
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Is this a good time to exercise based on my circadian phase?",
    "session_id": "user_001",
    "include_biosignal_context": true
  }'
```

### 4. General Health Advice (without current data)
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are some tips to improve my sleep quality?",
    "session_id": "user_001",
    "include_biosignal_context": false
  }'
```

## Testing

A comprehensive test script is provided to verify the integration:

```bash
cd /home/administrator/Documents/wearable/backend
./test_lia_chat.sh
```

This script tests:
- API connectivity
- Biosignal data streaming
- Chat with biosignal context
- Follow-up questions with conversation memory
- General health questions without context
- Conversation history retrieval
- History management

## Configuration

### Environment Variables

The LIA Chat Engine requires the following environment variable in [.env](backend/.env):

```env
OPENAI_API_KEY=sk-proj-...your-api-key...
```

### Dependencies

The following packages are required (already added to [requirements.txt](backend/requirements.txt)):

```
openai==1.12.0
httpx==0.25.0
httpcore==0.18.0
```

### Installation

```bash
cd /home/administrator/Documents/wearable/backend
source venv/bin/activate
pip install -r requirements.txt
```

## Running the Server

```bash
cd /home/administrator/Documents/wearable/backend
source venv/bin/activate
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The server will display:
```
✓ LIA Core™ Chat Engine initialized with OpenAI
✓ Backend ready to accept connections on http://localhost:8000
```

## Interactive Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Technical Details

### AI Model
- **Model**: GPT-4o-mini
- **Provider**: OpenAI
- **Temperature**: 0.7 (balanced creativity and consistency)
- **Max Tokens**: 500 per response
- **Timeout**: 30 seconds
- **Max Retries**: 2

### Conversation Management
- **History Size**: 20 messages per session (last 10 exchanges)
- **Session Isolation**: Each session_id maintains separate conversation context
- **Memory Scope**: In-memory storage (resets on server restart)

### System Prompt
LIA is configured with a detailed system prompt that defines:
- Personality: Professional, warm, evidence-based
- Capabilities: Health analysis, metric interpretation, recommendations
- Limitations: Never diagnoses medical conditions
- Response Style: Concise, clear, actionable

## Security Considerations

1. **API Key**: Store OPENAI_API_KEY securely in environment variables, never commit to version control
2. **Rate Limiting**: Consider implementing rate limiting for production use
3. **Authentication**: Add user authentication before deploying to production
4. **Data Privacy**: Conversation history contains health data - implement appropriate data retention policies
5. **HTTPS**: Use HTTPS in production to encrypt data in transit

## Troubleshooting

### Issue: "LIA Chat Engine is not available"
- Check that OPENAI_API_KEY is set in the `.env` file
- Verify the OpenAI package is installed: `pip show openai`
- Check server logs for initialization errors

### Issue: Slow responses
- OpenAI API calls typically take 2-5 seconds
- Check your internet connection
- Verify OpenAI API status: https://status.openai.com/

### Issue: HTTP compatibility errors
- Ensure httpx==0.25.0 and httpcore==0.18.0 are installed
- Run: `pip install httpx==0.25.0 httpcore==0.18.0`

## Future Enhancements

Potential improvements for the LIA Chat Engine:
- [ ] Persistent conversation storage in PostgreSQL database
- [ ] Long-term trend analysis from historical biosignal data
- [ ] Multi-language support
- [ ] Voice input/output integration
- [ ] Personalized health coaching programs
- [ ] Integration with external health APIs (Apple Health, Google Fit)
- [ ] Export conversation history to PDF reports
- [ ] Custom AI model fine-tuning on health domain data

## Support

For questions or issues, refer to:
- API Documentation: http://localhost:8000/docs
- Main README: [README.md](README.md)
- Technical Documentation: [TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md)

---

**LIA Core™ Conversational Module** - Powered by OpenAI GPT-4o-mini
*Integrated with Clarity™, iFRS™, and Timesystems™ proprietary biosignal processing layers*
