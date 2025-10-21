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
  "session_id": "user_123", // Optional, defaults to "default"
  "include_biosignal_context": true // Optional, defaults to true
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
curl -X POST https://wearable-biosignal-backend.onrender.com/api/v1/chat \
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
curl https://wearable-biosignal-backend.onrender.com/api/v1/chat/history/test_user_001
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
curl -X DELETE https://wearable-biosignal-backend.onrender.com/api/v1/chat/history/test_user_001
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
curl -X POST https://wearable-biosignal-backend.onrender.com/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How am I doing right now?",
    "session_id": "user_001",
    "include_biosignal_context": true
  }'
```

### 2. Understanding Metrics

```bash
curl -X POST https://wearable-biosignal-backend.onrender.com/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What does my LF/HF ratio mean?",
    "session_id": "user_001",
    "include_biosignal_context": true
  }'
```

### 3. Activity Recommendations

```bash
curl -X POST https://wearable-biosignal-backend.onrender.com/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Is this a good time to exercise based on my circadian phase?",
    "session_id": "user_001",
    "include_biosignal_context": true
  }'
```

### 4. General Health Advice (without current data)

```bash
curl -X POST https://wearable-biosignal-backend.onrender.com/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are some tips to improve my sleep quality?",
    "session_id": "user_001",
    "include_biosignal_context": false
  }'
```

The server will display:

```
✓ LIA Core™ Chat Engine initialized with OpenAI
✓ Backend ready to accept connections on https://wearable-biosignal-backend.onrender.com
```

## Interactive Documentation

Once the server is running, visit:

- Swagger UI: https://wearable-biosignal-backend.onrender.com/docs
- ReDoc: https://wearable-biosignal-backend.onrender.com/redoc

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

---

**LIA Core™ Conversational Module** - Powered by OpenAI GPT-4o-mini
_Integrated with Clarity™, iFRS™, and Timesystems™ proprietary biosignal processing layers_
