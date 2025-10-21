"""
LIA Core™ Conversational Module
Natural language interface for interacting with biosignal data and health insights
Integrates with OpenAI API to provide conversational AI capabilities
"""

import os
from typing import List, Dict, Optional
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

from app.models.schemas import (
    BiosignalData, LIAInsights, StreamDataResponse
)

# Load environment variables
load_dotenv()


class LIAChatEngine:
    """
    LIA Core™ Conversational Module

    Provides natural language interface for:
    - Querying current health status
    - Understanding biosignal data
    - Getting personalized health insights
    - Analyzing trends and patterns
    - Interactive health coaching
    """

    def __init__(self):
        """Initialize the LIA Chat Engine with OpenAI API"""
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

        # Initialize OpenAI client
        self.client = OpenAI(
            api_key=self.api_key,
            timeout=30.0,
            max_retries=2
        )
        self.model = "gpt-4o-mini"  # Using GPT-4o-mini for cost-effectiveness and speed

        # Conversation history per session
        self.conversations: Dict[str, List[Dict[str, str]]] = {}
        self.max_history = 20  # Keep last 20 messages per session

        # System prompt defining LIA's personality and capabilities
        self.system_prompt = """You are LIA (Lifestyle Intelligence Analysis), an advanced AI health assistant integrated with a wearable biosignal monitoring system.

You have access to real-time biosignal data from the user's wearable device, processed through three proprietary layers:

1. **Clarity™**: Signal quality assessment and noise reduction
2. **iFRS™ (Intelligent Frequency Response System)**: Heart rate variability (HRV) and frequency analysis
3. **Timesystems™**: Temporal pattern analysis and circadian rhythm detection

Your capabilities:
- Analyze current biosignal data (heart rate, SpO2, temperature, activity)
- Interpret HRV metrics and their health implications
- Explain circadian rhythm patterns
- Provide personalized health insights and recommendations
- Answer questions about wellness scores and health conditions
- Explain technical metrics in simple, understandable language
- Offer evidence-based lifestyle and wellness advice

Your personality:
- Professional yet warm and approachable
- Clear and concise in explanations
- Evidence-based and scientifically accurate
- Supportive and encouraging
- Never diagnose medical conditions (always recommend consulting healthcare providers for concerns)

When responding:
- Be specific and reference actual data values when available
- Explain technical terms in simple language
- Provide actionable insights
- Show empathy and understanding
- Keep responses concise but informative (2-4 sentences typically)
"""

    def get_context_from_stream_data(self, stream_data: StreamDataResponse) -> str:
        """
        Extract relevant context from stream data for the conversation

        Args:
            stream_data: Current biosignal stream data with all layer outputs

        Returns:
            Formatted context string for the AI
        """
        raw = stream_data.raw_signals
        clarity = stream_data.clarity_layer
        ifrs = stream_data.ifrs_layer
        timesystems = stream_data.timesystems_layer
        lia = stream_data.lia_insights

        context = f"""
CURRENT BIOSIGNAL DATA (as of {stream_data.timestamp.strftime('%Y-%m-%d %H:%M:%S')}):

Raw Signals:
- Heart Rate: {raw.heart_rate:.1f} BPM
- Blood Oxygen (SpO2): {raw.spo2:.1f}%
- Body Temperature: {raw.temperature:.1f}°C
- Activity Level: {raw.activity:.1f} steps/min

Clarity™ Layer (Signal Quality):
- Overall Quality Score: {clarity.quality_score:.2f}/1.0
- Signal-to-Noise Ratio: {clarity.signal_to_noise_ratio:.1f} dB
- Quality Assessment: {clarity.quality_assessment.value}
- Artifacts Detected: {', '.join(clarity.artifacts_detected) if clarity.artifacts_detected else 'None'}

iFRS™ Layer (Frequency Analysis):
- Dominant Frequency: {ifrs.dominant_frequency:.2f} Hz
- Rhythm Classification: {ifrs.rhythm_classification.value}
- HRV Score: {ifrs.hrv_features.hrv_score:.1f}/100
- HRV Metrics:
  * RMSSD: {ifrs.hrv_features.rmssd:.1f} ms
  * SDNN: {ifrs.hrv_features.sdnn:.1f} ms
  * pNN50: {ifrs.hrv_features.pnn50:.1f}%
- LF/HF Ratio: {ifrs.frequency_bands.lf_hf_ratio:.2f}
- Respiratory Rate: {ifrs.respiratory_rate:.1f} breaths/min

Timesystems™ Layer (Temporal Analysis):
- Pattern Type: {timesystems.pattern_type.value}
- Circadian Phase: {timesystems.circadian_phase.value}
- Temporal Consistency: {timesystems.temporal_consistency:.2f}/1.0
- Rhythm Score: {timesystems.rhythm_score:.1f}/100
- Circadian Alignment Score: {timesystems.circadian_alignment.alignment_score:.2f}/1.0

LIA Health Insights:
- Detected Condition: {lia.condition}
- Confidence: {lia.confidence:.1%}
- Overall Wellness Score: {lia.wellness_score:.1f}/100
- Wellness Breakdown:
  * Cardiovascular Health: {lia.wellness_assessment.cardiovascular_health:.1f}/100
  * Respiratory Health: {lia.wellness_assessment.respiratory_health:.1f}/100
  * Activity Level: {lia.wellness_assessment.activity_level:.1f}/100
  * Stress Level: {lia.wellness_assessment.stress_level:.1f}/100
- Risk Factors: {', '.join(lia.risk_factors) if lia.risk_factors else 'None identified'}
- Positive Indicators: {', '.join(lia.positive_indicators) if lia.positive_indicators else 'None'}
- Recommendation: {lia.recommendation}
"""
        return context

    def chat(
        self,
        user_message: str,
        stream_data: Optional[StreamDataResponse] = None,
        session_id: str = "default",
        include_context: bool = True
    ) -> Dict[str, any]:
        """
        Process a user message and generate a response

        Args:
            user_message: The user's question or message
            stream_data: Current biosignal data (optional, for context)
            session_id: Session identifier for conversation history
            include_context: Whether to include biosignal data context

        Returns:
            Dictionary containing response and metadata
        """
        try:
            # Initialize conversation history for this session if needed
            if session_id not in self.conversations:
                self.conversations[session_id] = []

            # Build messages array
            messages = [
                {"role": "system", "content": self.system_prompt}
            ]

            # Add conversation history
            messages.extend(self.conversations[session_id])

            # Add current biosignal data context if available and requested
            if include_context and stream_data:
                context = self.get_context_from_stream_data(stream_data)
                context_message = {
                    "role": "system",
                    "content": f"Here is the user's current real-time biosignal data:\n{context}"
                }
                messages.append(context_message)

            # Add user message
            messages.append({"role": "user", "content": user_message})

            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500,
                top_p=0.9,
                frequency_penalty=0.3,
                presence_penalty=0.3
            )

            # Extract response
            assistant_message = response.choices[0].message.content

            # Update conversation history
            self.conversations[session_id].append(
                {"role": "user", "content": user_message}
            )
            self.conversations[session_id].append(
                {"role": "assistant", "content": assistant_message}
            )

            # Trim history if too long
            if len(self.conversations[session_id]) > self.max_history:
                self.conversations[session_id] = self.conversations[session_id][-self.max_history:]

            return {
                "success": True,
                "response": assistant_message,
                "timestamp": datetime.now().isoformat(),
                "session_id": session_id,
                "tokens_used": response.usage.total_tokens,
                "model": self.model
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response": "I'm sorry, I encountered an error processing your request. Please try again.",
                "timestamp": datetime.now().isoformat(),
                "session_id": session_id
            }

    def clear_history(self, session_id: str = "default"):
        """Clear conversation history for a session"""
        if session_id in self.conversations:
            self.conversations[session_id] = []

    def get_conversation_history(self, session_id: str = "default") -> List[Dict[str, str]]:
        """Get conversation history for a session"""
        return self.conversations.get(session_id, [])
