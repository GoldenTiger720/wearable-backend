# LIA Core™ - cURL Command Examples

Quick reference guide for testing the LIA Core™ Conversational Module using curl commands.

## Basic Health Status Chat

```bash
curl -X POST https://wearable-biosignal-backend.onrender.com/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello! Can you tell me about my current health status?",
    "session_id": "user_001",
    "include_biosignal_context": true
  }'
```

## Ask About Specific Metrics

### Heart Rate Variability (HRV)

```bash
curl -X POST https://wearable-biosignal-backend.onrender.com/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What does my HRV score mean? Is it good or bad?",
    "session_id": "user_001",
    "include_biosignal_context": true
  }'
```

### Blood Oxygen (SpO2)

```bash
curl -X POST https://wearable-biosignal-backend.onrender.com/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How is my blood oxygen level? Should I be concerned?",
    "session_id": "user_001",
    "include_biosignal_context": true
  }'
```

### Circadian Rhythm

```bash
curl -X POST https://wearable-biosignal-backend.onrender.com/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What does my circadian phase indicate? Is this a good time for exercise?",
    "session_id": "user_001",
    "include_biosignal_context": true
  }'
```

### Wellness Score

```bash
curl -X POST https://wearable-biosignal-backend.onrender.com/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Explain my overall wellness score. What areas should I focus on improving?",
    "session_id": "user_001",
    "include_biosignal_context": true
  }'
```

## General Health Questions (Without Current Data)

```bash
curl -X POST https://wearable-biosignal-backend.onrender.com/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the best ways to improve my sleep quality?",
    "session_id": "user_001",
    "include_biosignal_context": false
  }'
```

```bash
curl -X POST https://wearable-biosignal-backend.onrender.com/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What exercises are best for improving cardiovascular health?",
    "session_id": "user_001",
    "include_biosignal_context": false
  }'
```

## Conversation Management

### Get Conversation History

```bash
curl https://wearable-biosignal-backend.onrender.com/api/v1/chat/history/user_001
```

### Clear Conversation History

```bash
curl -X DELETE https://wearable-biosignal-backend.onrender.com/api/v1/chat/history/user_001
```

## Get Current Biosignal Data

```bash
# Get processed data from all layers
curl https://wearable-biosignal-backend.onrender.com/api/v1/stream | python3 -m json.tool
```

```bash
# Get prediction/condition
curl https://wearable-biosignal-backend.onrender.com/api/v1/predict | python3 -m json.tool
```

```bash
# Get processing logs
curl https://wearable-biosignal-backend.onrender.com/api/v1/logs/processing?limit=50 | python3 -m json.tool
```

## System Status

```bash
# Check API info
curl https://wearable-biosignal-backend.onrender.com/ | python3 -m json.tool
```

```bash
# Health check
curl https://wearable-biosignal-backend.onrender.com/api/v1/health | python3 -m json.tool
```

## Multi-turn Conversation Example

```bash
# Message 1
curl -X POST https://wearable-biosignal-backend.onrender.com/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hi LIA, how am I doing today?",
    "session_id": "conversation_demo",
    "include_biosignal_context": true
  }'

# Message 2 (follows context from Message 1)
curl -X POST https://wearable-biosignal-backend.onrender.com/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Can you explain my HRV in more detail?",
    "session_id": "conversation_demo",
    "include_biosignal_context": true
  }'

# Message 3 (follows context from Messages 1 & 2)
curl -X POST https://wearable-biosignal-backend.onrender.com/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What should I do to improve it?",
    "session_id": "conversation_demo",
    "include_biosignal_context": true
  }'

# View the full conversation
curl https://wearable-biosignal-backend.onrender.com/api/v1/chat/history/conversation_demo | python3 -m json.tool
```

## Pretty Print JSON Responses

Add `| python3 -m json.tool` to any curl command for formatted output:

```bash
curl -X POST https://wearable-biosignal-backend.onrender.com/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How is my heart rate?",
    "session_id": "user_001",
    "include_biosignal_context": true
  }' | python3 -m json.tool
```

## Extract Just the Response Message

```bash
curl -s -X POST https://wearable-biosignal-backend.onrender.com/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How is my health?",
    "session_id": "user_001",
    "include_biosignal_context": true
  }' | python3 -c "import sys, json; print(json.load(sys.stdin)['response'])"
```

## Useful One-Liners

```bash
# Quick health check
curl -s https://wearable-biosignal-backend.onrender.com/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Quick health summary?","session_id":"quick"}' \
  | python3 -c "import sys, json; print(json.load(sys.stdin)['response'])"

# Check if server is running
curl -s https://wearable-biosignal-backend.onrender.com/api/v1/health | python3 -c "import sys, json; print('Status:', json.load(sys.stdin)['status'])"

# Get current heart rate
curl -s https://wearable-biosignal-backend.onrender.com/api/v1/stream | python3 -c "import sys, json; print('Heart Rate:', json.load(sys.stdin)['raw_signals']['heart_rate'], 'BPM')"

# Get wellness score
curl -s https://wearable-biosignal-backend.onrender.com/api/v1/stream | python3 -c "import sys, json; print('Wellness Score:', json.load(sys.stdin)['lia_insights']['wellness_score'])"
```

## Interactive API Documentation

Instead of curl, you can also test the API using the interactive Swagger UI:

Open in browser: **https://wearable-biosignal-backend.onrender.com/docs**

This provides a web interface where you can:

- See all available endpoints
- Test requests directly in the browser
- View request/response schemas
- Try different parameters

---

**Note**: All examples assume the server is running on `https://wearable-biosignal-backend.onrender.com`.
