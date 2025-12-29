"""
AI-powered comment generator using Hugging Face's AI models.
Generates natural, human-like responses based on bot personality.
"""

import requests
import os
import random
from typing import Optional

# Hugging Face API configuration
HF_API_TOKEN = os.getenv("HF_API_TOKEN", "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")

# Use a more capable model for natural language generation
# Mistral-7B-Instruct is great for natural, human-like responses
HF_MODEL_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

# Fallback models if primary is unavailable
FALLBACK_MODELS = [
    "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta",
    "https://api-inference.huggingface.co/models/google/flan-t5-large",
]


def build_personality_prompt(personality_type: str, interests: str, profession: str, emotional_bias: str) -> str:
    """
    Build a natural personality description for the AI to embody.
    """
    personality_traits = {
        "optimistic": "You are warm, encouraging, and see the positive side of things. You genuinely celebrate others' successes and offer supportive words. You use exclamation marks naturally and occasionally emojis.",
        
        "critical": "You are a thoughtful skeptic who asks probing questions. You're not mean, but you like to dig deeper and challenge assumptions. You often say 'but' or 'have you considered...'",
        
        "neutral": "You are balanced and objective. You acknowledge points fairly without being overly positive or negative. You're the voice of reason.",
        
        "sarcastic": "You have a dry wit and use light, playful sarcasm. You're funny but never mean-spirited. You might use phrases like 'Oh sure...' or make ironic observations.",
        
        "techie": "You're a tech enthusiast who loves geeking out about technology, code, and systems. You naturally ask about implementation details or share technical insights.",
        
        "minimal": "You're a person of few words. You reply with short, punchy responses - usually just 2-5 words. Think 'nice', 'solid work', 'facts', 'this 👆'.",
    }
    
    base_trait = personality_traits.get(personality_type, personality_traits["neutral"])
    
    # Add profession context if available
    profession_context = ""
    if profession and profession.strip():
        profession_context = f" You work as a {profession}, which influences your perspective."
    
    # Add interests context if available
    interests_context = ""
    if interests and interests.strip():
        interests_context = f" You're particularly interested in {interests}."
    
    # Add emotional bias
    bias_context = ""
    if emotional_bias == "positive":
        bias_context = " You tend to be upbeat and encouraging."
    elif emotional_bias == "negative":
        bias_context = " You tend to be more skeptical and questioning."
    
    return f"{base_trait}{profession_context}{interests_context}{bias_context}"


# Stance control per personality - humans react differently to opinions
STANCE_BY_PERSONALITY = {
    "optimistic": "You generally try to see the good side, even if you partly agree.",
    "critical": "You question the statement and challenge it thoughtfully.",
    "neutral": "You reflect without fully agreeing or disagreeing.",
    "sarcastic": "You respond with light irony, but still reference the opinion.",
    "techie": "You relate it to technology, platforms, or systems.",
    "minimal": "You react briefly, but still clearly.",
}


# Expected behavior per context and personality - industry-grade prompt conditioning
EXPECTED_BEHAVIOR = {
    "technical_work": {
        "optimistic": "encourage effort and celebrate the success",
        "critical": "question what was hard or how it was solved",
        "neutral": "acknowledge the effort calmly",
        "sarcastic": "joke about debugging pain or dev struggles",
        "techie": "mention debugging, backend, tools, or technical details",
        "minimal": "short acknowledgement of effort",
    },
    "emotional": {
        "optimistic": "offer genuine support and encouragement",
        "critical": "ask thoughtful questions about the situation",
        "neutral": "acknowledge feelings without judgment",
        "sarcastic": "use light humor to relate to the struggle",
        "techie": "relate feelings to work/tech context if relevant",
        "minimal": "brief supportive reaction",
    },
    "opinion": {
        "optimistic": "find the positive angle even if you partly agree",
        "critical": "challenge the opinion respectfully",
        "neutral": "reflect on both sides",
        "sarcastic": "use irony to comment on the opinion",
        "techie": "relate it to platforms, algorithms, or tech",
        "minimal": "quick agreement or disagreement",
    },
    "achievement": {
        "optimistic": "celebrate their win enthusiastically",
        "critical": "ask about the journey or challenges",
        "neutral": "acknowledge the accomplishment",
        "sarcastic": "playfully downplay while still being supportive",
        "techie": "ask about the tech stack or implementation",
        "minimal": "brief congratulations",
    },
    "general": {
        "optimistic": "find something positive to say",
        "critical": "ask a thoughtful question",
        "neutral": "acknowledge what they said",
        "sarcastic": "make a witty observation",
        "techie": "relate to tech if possible",
        "minimal": "brief reaction",
    },
}


def detect_post_context(post: str) -> str:
    """
    Classify the post into a context category to anchor the AI response.
    """
    post_lower = post.lower()
    
    # Technical work - debugging, coding, building
    if any(word in post_lower for word in ["debug", "bug", "backend", "frontend", "code", "coding", 
                                            "project", "deploy", "server", "api", "database", "error",
                                            "fix", "fixed", "hours", "finally", "working", "build"]):
        return "technical_work"
    
    # Achievement - completed something, shipped, launched
    if any(word in post_lower for word in ["finished", "completed", "launched", "shipped", "built",
                                            "released", "proud", "achieved", "milestone", "done"]):
        return "achievement"
    
    # Emotional - feelings, stress, mental state
    if any(word in post_lower for word in ["feel", "feeling", "mental", "tired", "stress", "stressed",
                                            "exhausted", "burned", "burnout", "anxious", "happy", "sad"]):
        return "emotional"
    
    # Opinion - views on topics, social media, life
    if any(word in post_lower for word in ["think", "believe", "opinion", "seems", "honestly",
                                            "social media", "platform", "society", "people"]):
        return "opinion"
    
    return "general"


def create_comment_prompt(post_content: str, personality_description: str, personality_type: str) -> str:
    """
    Create a natural prompt that instructs the AI to generate a human-like comment.
    The key is making the model respond to the SPECIFIC SITUATION in the post.
    """
    stance_instruction = STANCE_BY_PERSONALITY.get(personality_type, "")
    context = detect_post_context(post_content)
    expected_behavior = EXPECTED_BEHAVIOR.get(context, EXPECTED_BEHAVIOR["general"]).get(personality_type, "")
    
    # For minimal personality, keep it extra short
    if personality_type == "minimal":
        return f"""You are a real human scrolling social media.
{personality_description}

Someone shared this update:
"{post_content}"

Post context: {context}

Your task:
- React in 2-5 words max
- Reference the specific situation in the post
- Sound like a quick, genuine reaction

Expected behavior: {expected_behavior}

Comment:"""
    
    return f"""You are a real human scrolling social media.
{personality_description}

Someone shared this update:
"{post_content}"

Post context: {context}

Your task:
- Respond directly to THIS update
- Explicitly reference the situation (debugging, backend, effort, outcome, feelings, etc.)
- Sound natural and conversational
- Take a light stance (react, encourage, reflect, joke, or question)
- Do NOT be generic
- Do NOT introduce unrelated topics
- Keep it to 1-2 sentences max

Expected behavior: {expected_behavior}

Reaction style:
{stance_instruction}

Comment:"""


def clean_ai_response(response: str, personality_type: str) -> str:
    """
    Clean up the AI response to make it more natural.
    """
    if not response:
        return ""
    
    # Remove common AI artifacts
    response = response.strip()
    
    # Remove quotes if the entire response is quoted
    if response.startswith('"') and response.endswith('"'):
        response = response[1:-1]
    if response.startswith("'") and response.endswith("'"):
        response = response[1:-1]
    
    # Remove common prefixes
    prefixes_to_remove = [
        "Your reply:", "Reply:", "Comment:", "Response:",
        "Here's my reply:", "My reply:", "I would say:",
        "Here's a", "Here is", "As a", "Sure!", "Sure,",
        "Well,", "So,", "I think",
    ]
    for prefix in prefixes_to_remove:
        if response.lower().startswith(prefix.lower()):
            response = response[len(prefix):].strip()
    
    # Remove generic phrases that LLMs default to
    generic_phrases = [
        "thanks for sharing", "interesting point", "fair enough",
        "good to know", "i appreciate", "great post",
    ]
    response_lower = response.lower()
    for phrase in generic_phrases:
        if phrase in response_lower:
            # If the whole response is just a generic phrase, return empty to trigger fallback
            if len(response) < len(phrase) + 15:
                return ""
    
    # Remove asterisks used for emphasis in some models
    response = response.replace("**", "").replace("*", "")
    
    # Ensure it's not too long (social media comments are usually short)
    sentences = response.split('. ')
    if len(sentences) > 3:
        response = '. '.join(sentences[:2]) + '.'
    
    # For minimal personality, enforce brevity
    if personality_type == "minimal":
        words = response.split()
        if len(words) > 6:
            response = ' '.join(words[:5])
            if not response.endswith(('.', '!', '?')):
                response = response.rstrip(',') + '.'
    
    # Clean up any double spaces or weird punctuation
    response = ' '.join(response.split())
    response = response.replace(' .', '.').replace(' ,', ',').replace(' !', '!').replace(' ?', '?')
    
    return response.strip()


def generate_simple_fallback(post_content: str, personality_type: str) -> str:
    """
    Generate a context-aware fallback if AI fails.
    Responses are grounded in the post's context, not generic.
    """
    context = detect_post_context(post_content)
    
    # Context-aware fallbacks per personality
    fallbacks = {
        "technical_work": {
            "optimistic": [
                "That debugging grind is real, but you pushed through! 💪",
                "Hours of fixing bugs and you made it work. Nice!",
                "The backend struggle is worth it when it finally clicks.",
                "Love seeing that persistence pay off!",
            ],
            "critical": [
                "What was the actual root cause? Always curious about those.",
                "Hours of debugging... was it a typo? It's always a typo.",
                "Interesting. What made it so tricky to track down?",
                "Did you find a better way to prevent this next time?",
            ],
            "neutral": [
                "That sounds like a tough debugging session.",
                "Backend issues can be brutal. Glad you got through it.",
                "Those hours add up, but at least it's working now.",
                "Solid effort getting that fixed.",
            ],
            "sarcastic": [
                "Only 5 hours? Rookie numbers 😏",
                "Let me guess... it was a missing semicolon?",
                "Backend debugging: the gift that keeps on giving.",
                "Ah yes, the classic 'it works now and I don't know why'.",
            ],
            "techie": [
                "What was the stack? Always curious about these debugging stories.",
                "Was it a race condition? Those are the worst.",
                "Backend bugs hit different. What tools did you use?",
                "Nice! Did you add some logging to catch it faster next time?",
            ],
            "minimal": [
                "The grind.",
                "Been there.",
                "Respect.",
                "Real.",
                "💪",
            ],
        },
        "achievement": {
            "optimistic": [
                "Congrats! That's a huge accomplishment!",
                "You did it! All that work paid off!",
                "This is awesome, well deserved!",
                "So happy to see this come together for you!",
            ],
            "critical": [
                "Nice! What was the hardest part of getting there?",
                "Congrats. How long did this take overall?",
                "Well done. Any lessons learned along the way?",
                "Solid achievement. What's next?",
            ],
            "neutral": [
                "That's a solid milestone. Well done.",
                "Good to see the effort paying off.",
                "Congrats on getting it done.",
                "That's real progress right there.",
            ],
            "sarcastic": [
                "Oh look, someone actually finished something 😄",
                "Wait, projects can actually get completed?",
                "Show off 😏 (but seriously, congrats)",
                "Must be nice to be productive!",
            ],
            "techie": [
                "Nice! What's the tech stack?",
                "Congrats! How's the architecture looking?",
                "Solid work. Any interesting technical challenges?",
                "Well done! Planning to open source it?",
            ],
            "minimal": [
                "Nice work.",
                "Congrats!",
                "Well done.",
                "🔥",
                "Shipped.",
            ],
        },
        "emotional": {
            "optimistic": [
                "Hang in there, you've got this! 💙",
                "It's okay to feel that way. Tomorrow's a new day.",
                "Sending good vibes your way.",
                "You're doing better than you think.",
            ],
            "critical": [
                "What's making it feel that way?",
                "Have you tried stepping back for a bit?",
                "Is there something specific driving this?",
                "Sometimes it helps to talk it out.",
            ],
            "neutral": [
                "That's a valid way to feel.",
                "I hear you. It's not easy.",
                "Makes sense given everything.",
                "Sometimes you just gotta sit with it.",
            ],
            "sarcastic": [
                "2024/2025 energy right there.",
                "Same honestly.",
                "Welcome to the club 😅",
                "It's giving... relatable.",
            ],
            "techie": [
                "Tech work burnout is real. Take care of yourself.",
                "Maybe time for a git stash on life for a bit.",
                "Sometimes you need to ctrl+z on the whole week.",
                "Have you tried turning yourself off and on again?",
            ],
            "minimal": [
                "Felt this.",
                "Same.",
                "💙",
                "Hang in there.",
                "Real.",
            ],
        },
        "opinion": {
            "optimistic": [
                "I see what you mean, but there's hope still!",
                "Fair point, though I think it can get better.",
                "Yeah, I get that. Still some good out there though.",
                "That's real, but I try to stay optimistic.",
            ],
            "critical": [
                "You're not wrong, but have you considered the flip side?",
                "That's one angle. What about...?",
                "I'd push back a bit on this framing.",
                "Interesting take. What's driving this view?",
            ],
            "neutral": [
                "It definitely feels that way sometimes.",
                "Hard to argue with that.",
                "I can see both sides of this.",
                "Yeah, it's complicated.",
            ],
            "sarcastic": [
                "Groundbreaking observation 😏",
                "Who could have possibly predicted this?",
                "I mean... where's the lie?",
                "Tell us something we don't know 😄",
            ],
            "techie": [
                "A lot of that comes down to how the algorithms work.",
                "That's the engagement-first model for you.",
                "It's basically by design at this point.",
                "Platform incentives drive this behavior.",
            ],
            "minimal": [
                "Facts.",
                "This 👆",
                "Real.",
                "Yep.",
                "Hard agree.",
            ],
        },
        "general": {
            "optimistic": [
                "Love this energy!",
                "This is great, keep it up!",
                "Really appreciate you sharing this.",
                "Good vibes from this one!",
            ],
            "critical": [
                "Interesting. Tell me more about your thinking here.",
                "What led you to this?",
                "I'd be curious to hear more context.",
                "That's an interesting angle.",
            ],
            "neutral": [
                "I hear you on this.",
                "That makes sense.",
                "Fair point.",
                "I can see that.",
            ],
            "sarcastic": [
                "Well, that's certainly something.",
                "Breaking news over here 😏",
                "I mean... okay!",
                "Bold move sharing this.",
            ],
            "techie": [
                "Interesting perspective from a tech angle.",
                "This relates to some stuff I've been thinking about.",
                "Would love to dig into this more.",
                "There's a systems angle to this.",
            ],
            "minimal": [
                "Nice.",
                "Noted.",
                "👍",
                "Real.",
                "True.",
            ],
        },
    }
    
    context_fallbacks = fallbacks.get(context, fallbacks["general"])
    personality_fallbacks = context_fallbacks.get(personality_type, context_fallbacks.get("neutral", ["I hear you."]))
    
    return random.choice(personality_fallbacks)


def get_personality_from_bot_profile(interests: str, emotional_bias: str, profession: str) -> str:
    """
    Determine the bot's personality type from its profile.
    """
    interests_lower = interests.lower() if interests else ""
    profession_lower = profession.lower() if profession else ""
    
    # Check for specific personality indicators
    if any(word in interests_lower for word in ["optimistic", "encouraging", "positive", "supportive", "cheerful"]):
        return "optimistic"
    elif any(word in interests_lower for word in ["critical", "skeptic", "analyst", "questioning", "debate"]):
        return "critical"
    elif any(word in interests_lower for word in ["sarcastic", "irony", "humor", "wit", "funny"]):
        return "sarcastic"
    elif any(word in interests_lower or word in profession_lower for word in ["tech", "programming", "developer", "engineer", "coding", "software"]):
        return "techie"
    elif any(word in interests_lower for word in ["minimal", "brief", "short", "concise"]):
        return "minimal"
    else:
        # Default based on emotional bias
        if emotional_bias == "positive":
            return "optimistic"
        elif emotional_bias == "negative":
            return "critical"
        else:
            return "neutral"


def generate_ai_comment(post_content: str, personality_type: str, 
                        interests: str = "", profession: str = "", 
                        emotional_bias: str = "neutral", max_retries: int = 3) -> str:
    """
    Generate a natural, human-like comment using AI.
    
    Args:
        post_content: The content of the post to respond to
        personality_type: The bot's personality type
        interests: The bot's interests
        profession: The bot's profession
        emotional_bias: The bot's emotional bias
        max_retries: Number of retries if API fails
        
    Returns:
        Generated comment string
    """
    # Build the personality description
    personality_description = build_personality_prompt(
        personality_type, interests, profession, emotional_bias
    )
    
    # Create the prompt
    prompt = create_comment_prompt(post_content[:500], personality_description, personality_type)
    
    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Parameters tuned for natural, varied responses
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 80,
            "temperature": 0.9,
            "top_p": 0.9,
            "do_sample": True,
            "return_full_text": False,
            "repetition_penalty": 1.1,
            "stop": ["\n\n", "Comment:", "Your reply:", "---"]
        }
    }
    
    models_to_try = [HF_MODEL_URL] + FALLBACK_MODELS
    
    for model_url in models_to_try:
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    model_url,
                    headers=headers,
                    json=payload,
                    timeout=45
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Handle different response formats
                    if isinstance(result, list) and len(result) > 0:
                        generated_text = result[0].get("generated_text", "").strip()
                    elif isinstance(result, dict):
                        generated_text = result.get("generated_text", "").strip()
                    else:
                        generated_text = ""
                    
                    # Clean and validate the response
                    cleaned = clean_ai_response(generated_text, personality_type)
                    
                    if cleaned and len(cleaned) >= 2:
                        return cleaned
                
                elif response.status_code == 503:
                    # Model is loading, wait and retry
                    import time
                    time.sleep(3)
                    continue
                    
                elif response.status_code == 429:
                    # Rate limited, wait longer
                    import time
                    time.sleep(5)
                    continue
                    
            except Exception as e:
                print(f"AI comment generation error with {model_url} (attempt {attempt + 1}): {e}")
        
        # If this model failed all retries, try the next one
        print(f"Moving to fallback model after {model_url} failed")
    
    # Last resort: generate a simple contextual response
    return generate_simple_fallback(post_content, personality_type)


def generate_comment_for_bot(post_content: str, bot_interests: str, 
                              emotional_bias: str, profession: str) -> str:
    """
    Main function to generate a comment for a bot based on its profile.
    
    This is the entry point - it takes the bot's full profile and generates
    a natural, human-like comment that reflects their personality.
    
    Args:
        post_content: The content of the post
        bot_interests: Comma-separated interests of the bot
        emotional_bias: The bot's emotional bias (positive, neutral, negative)
        profession: The bot's profession
        
    Returns:
        Generated comment string
    """
    # Determine personality type from profile
    personality_type = get_personality_from_bot_profile(bot_interests, emotional_bias, profession)
    
    # Generate a natural AI comment with full context
    return generate_ai_comment(
        post_content=post_content,
        personality_type=personality_type,
        interests=bot_interests,
        profession=profession,
        emotional_bias=emotional_bias
    )
