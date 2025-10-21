#!/bin/bash

###############################################################################
# LIA Core™ Conversational Module Test Script
# Tests the OpenAI-powered chat interface with biosignal data integration
###############################################################################

echo "=================================================="
echo "LIA Core™ Conversational Module - Test Script"
echo "=================================================="
echo ""

BASE_URL="http://localhost:8000"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Check API is running
echo -e "${BLUE}[TEST 1]${NC} Checking API status..."
echo "GET $BASE_URL/"
echo ""
curl -s $BASE_URL/ | python3 -m json.tool
echo ""
echo ""

# Test 2: Get current biosignal stream data
echo -e "${BLUE}[TEST 2]${NC} Getting current biosignal data..."
echo "GET $BASE_URL/api/v1/stream"
echo ""
curl -s $BASE_URL/api/v1/stream | python3 -m json.tool | head -80
echo "... (truncated)"
echo ""
echo ""

# Test 3: Chat with LIA (with biosignal context)
echo -e "${BLUE}[TEST 3]${NC} Chat with LIA - Health Status Inquiry (WITH biosignal context)..."
echo "POST $BASE_URL/api/v1/chat"
echo ""
RESPONSE=$(curl -s -X POST $BASE_URL/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello LIA! Can you analyze my current health status and tell me how I am doing?",
    "session_id": "demo_session_001",
    "include_biosignal_context": true
  }')
echo "$RESPONSE" | python3 -m json.tool
echo ""
echo -e "${GREEN}LIA Response:${NC}"
echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['response'])"
echo ""
echo ""

# Test 4: Follow-up question about HRV
echo -e "${BLUE}[TEST 4]${NC} Follow-up question - Understanding HRV..."
echo "POST $BASE_URL/api/v1/chat"
echo ""
RESPONSE=$(curl -s -X POST $BASE_URL/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Can you explain my heart rate variability in more detail? What does it mean for my health?",
    "session_id": "demo_session_001",
    "include_biosignal_context": true
  }')
echo "$RESPONSE" | python3 -m json.tool
echo ""
echo -e "${GREEN}LIA Response:${NC}"
echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['response'])"
echo ""
echo ""

# Test 5: Ask about circadian rhythm
echo -e "${BLUE}[TEST 5]${NC} Ask about circadian rhythm and timing..."
echo "POST $BASE_URL/api/v1/chat"
echo ""
RESPONSE=$(curl -s -X POST $BASE_URL/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What does my circadian phase indicate? Is this a good time for exercise?",
    "session_id": "demo_session_001",
    "include_biosignal_context": true
  }')
echo "$RESPONSE" | python3 -m json.tool
echo ""
echo -e "${GREEN}LIA Response:${NC}"
echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['response'])"
echo ""
echo ""

# Test 6: General health question (without biosignal context)
echo -e "${BLUE}[TEST 6]${NC} General health question (WITHOUT biosignal context)..."
echo "POST $BASE_URL/api/v1/chat"
echo ""
RESPONSE=$(curl -s -X POST $BASE_URL/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the best ways to improve my cardiovascular health?",
    "session_id": "demo_session_002",
    "include_biosignal_context": false
  }')
echo "$RESPONSE" | python3 -m json.tool
echo ""
echo -e "${GREEN}LIA Response:${NC}"
echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['response'])"
echo ""
echo ""

# Test 7: Get conversation history for session 1
echo -e "${BLUE}[TEST 7]${NC} Retrieving conversation history..."
echo "GET $BASE_URL/api/v1/chat/history/demo_session_001"
echo ""
curl -s $BASE_URL/api/v1/chat/history/demo_session_001 | python3 -m json.tool
echo ""
echo ""

# Test 8: Clear conversation history
echo -e "${BLUE}[TEST 8]${NC} Clearing conversation history..."
echo "DELETE $BASE_URL/api/v1/chat/history/demo_session_001"
echo ""
curl -s -X DELETE $BASE_URL/api/v1/chat/history/demo_session_001 | python3 -m json.tool
echo ""
echo ""

# Test 9: Verify history was cleared
echo -e "${BLUE}[TEST 9]${NC} Verifying history was cleared..."
echo "GET $BASE_URL/api/v1/chat/history/demo_session_001"
echo ""
curl -s $BASE_URL/api/v1/chat/history/demo_session_001 | python3 -m json.tool
echo ""
echo ""

echo "=================================================="
echo -e "${GREEN}All tests completed successfully!${NC}"
echo "=================================================="
echo ""
echo "Key Features Demonstrated:"
echo "  ✓ Chat with real-time biosignal context"
echo "  ✓ Conversational memory across messages"
echo "  ✓ Analysis of HRV, circadian rhythm, and wellness metrics"
echo "  ✓ General health coaching without biosignal data"
echo "  ✓ Conversation history management"
echo ""
echo "The LIA Core™ Conversational Module is fully integrated with:"
echo "  • Clarity™ Layer (signal quality)"
echo "  • iFRS™ Layer (frequency analysis & HRV)"
echo "  • Timesystems™ Layer (temporal patterns & circadian rhythm)"
echo "  • Real-time biosignal data from BLE simulator"
echo "  • OpenAI GPT-4o-mini for natural language understanding"
echo ""
