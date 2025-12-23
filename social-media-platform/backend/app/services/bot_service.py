import random
import time
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from ..models.bot import Bot, BotProfile, BotInteractionLog, EmotionalBias
from ..models.post import Post
from ..models.comment import Comment
from ..models.reaction import Reaction

# Predefined comment templates based on emotional bias
COMMENT_TEMPLATES = {
    EmotionalBias.POSITIVE: [
        "This is amazing! 😊",
        "Love this content!",
        "Great post! Keep it up! 👍",
        "Absolutely wonderful!",
        "This made my day! ❤️",
        "Fantastic work!",
        "So inspiring! 🌟",
        "This is exactly what I needed to see!",
    ],
    EmotionalBias.NEUTRAL: [
        "Interesting perspective.",
        "Thanks for sharing.",
        "Good point.",
        "I see what you mean.",
        "Worth considering.",
        "Noted.",
        "Fair enough.",
        "Makes sense.",
    ],
    EmotionalBias.NEGATIVE: [
        "I don't really agree with this.",
        "Not sure about this...",
        "Could be better.",
        "I have some concerns.",
        "This is questionable.",
        "Not convinced.",
        "I expected more.",
        "Disappointing.",
    ]
}

class BotEngine:
    """Rule-based bot interaction engine"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def is_universal_bot(self, bot: Bot) -> bool:
        """Check if bot is a universal bot (interacts with everything)"""
        if not bot.profile or not bot.profile.interests:
            return False
        interests = bot.profile.interests.lower()
        return 'universal' in interests or 'all' in interests or 'everything' in interests
    
    def calculate_relevance_score(self, bot: Bot, post: Post) -> float:
        """
        Calculate how relevant a post is to a bot's interests.
        Returns a score between 0.0 and 1.0
        """
        # Universal bots always have high relevance
        if self.is_universal_bot(bot):
            return 1.0
        
        if not bot.profile or not bot.profile.interests:
            return 0.0  # No interests = no relevance for topic-based bots
        
        bot_interests = set(interest.strip().lower() 
                          for interest in bot.profile.interests.split(','))
        
        relevance = 0.0
        
        # Check post topic (most important)
        if post.topic:
            post_topic = post.topic.lower()
            for interest in bot_interests:
                if interest and len(interest) > 2:  # Skip very short words
                    if interest in post_topic or post_topic in interest:
                        relevance += 0.5
                        break
        
        # Check post keywords
        if post.keywords:
            post_keywords = set(kw.strip().lower() 
                              for kw in post.keywords.split(','))
            for interest in bot_interests:
                for keyword in post_keywords:
                    if interest and keyword and (interest in keyword or keyword in interest):
                        relevance += 0.3
                        break
        
        # Check post content for interests
        content_lower = post.content.lower()
        for interest in bot_interests:
            if interest and len(interest) > 2 and interest in content_lower:
                relevance += 0.2
                break
        
        return min(relevance, 1.0)
    
    def should_interact(self, probability: float, relevance_score: float) -> bool:
        """
        Determine if bot should perform an action.
        Higher relevance increases the effective probability.
        """
        # For universal bots (relevance=1.0), use full probability
        # For topic bots, scale by relevance
        adjusted_probability = probability * (0.3 + relevance_score * 0.7)
        return random.random() < adjusted_probability
    
    def get_emotional_comment(self, bot: Bot) -> str:
        """Generate a comment based on bot's emotional bias"""
        if not bot.profile:
            emotional_bias = EmotionalBias.NEUTRAL
        else:
            emotional_bias = bot.profile.emotional_bias
        
        templates = COMMENT_TEMPLATES.get(emotional_bias, COMMENT_TEMPLATES[EmotionalBias.NEUTRAL])
        return random.choice(templates)
    
    def should_like_or_dislike(self, bot: Bot, relevance_score: float) -> Optional[bool]:
        """
        Determine if bot should like or dislike.
        Returns True for like, False for dislike, None for no reaction.
        Emotional bias affects the decision.
        """
        if not bot.profile:
            return None
        
        # Adjust probabilities based on emotional bias and relevance
        bias_multiplier = {
            EmotionalBias.POSITIVE: 1.5,
            EmotionalBias.NEUTRAL: 1.0,
            EmotionalBias.NEGATIVE: 0.6
        }
        
        multiplier = bias_multiplier.get(bot.profile.emotional_bias, 1.0)
        
        if self.should_interact(bot.profile.like_probability * multiplier, relevance_score):
            return True
        
        dislike_multiplier = 2.0 if bot.profile.emotional_bias == EmotionalBias.NEGATIVE else 1.0
        if self.should_interact(bot.profile.dislike_probability * dislike_multiplier, relevance_score):
            return False
        
        return None
    
    def process_post_for_bot(self, bot: Bot, post: Post):
        """Process a single post for a single bot"""
        if not bot.is_active:
            return False
        
        # Check if bot already interacted with this post
        existing_log = self.db.query(BotInteractionLog).filter(
            BotInteractionLog.bot_id == bot.id,
            BotInteractionLog.post_id == post.id
        ).first()
        
        if existing_log:
            return False  # Already processed
        
        # Calculate relevance
        relevance_score = self.calculate_relevance_score(bot, post)
        
        # Universal bots always interact, topic bots need relevance
        is_universal = self.is_universal_bot(bot)
        
        if is_universal:
            # Universal bots always have full relevance
            relevance_score = 1.0
        elif relevance_score < 0.1:
            # Topic-based bots skip irrelevant posts
            return False
        
        # Simulate response delay
        if bot.profile:
            delay = random.randint(
                bot.profile.min_response_delay,
                bot.profile.max_response_delay
            )
            time.sleep(min(delay, 5))  # Cap at 5 seconds for demonstration
        
        actions_taken = []
        
        # Try to react (like/dislike)
        existing_reaction = self.db.query(Reaction).filter(
            Reaction.post_id == post.id,
            Reaction.bot_id == bot.id
        ).first()
        
        if not existing_reaction:
            reaction_type = self.should_like_or_dislike(bot, relevance_score)
            if reaction_type is not None:
                reaction = Reaction(
                    post_id=post.id,
                    bot_id=bot.id,
                    is_like=reaction_type
                )
                self.db.add(reaction)
                actions_taken.append("like" if reaction_type else "dislike")
        
        # Try to comment
        existing_comment = self.db.query(Comment).filter(
            Comment.post_id == post.id,
            Comment.bot_id == bot.id
        ).first()
        
        if not existing_comment and bot.profile:
            if self.should_interact(bot.profile.comment_probability, relevance_score):
                comment_text = self.get_emotional_comment(bot)
                comment = Comment(
                    post_id=post.id,
                    bot_id=bot.id,
                    content=comment_text
                )
                self.db.add(comment)
                actions_taken.append("comment")
        
        # Log the interaction
        if actions_taken:
            log = BotInteractionLog(
                bot_id=bot.id,
                post_id=post.id,
                action_type=",".join(actions_taken),
                relevance_score=relevance_score
            )
            self.db.add(log)
            self.db.commit()
            return True
        return False
    
    def process_recent_posts(self, hours: int = 24):
        """Process recent posts for all active bots"""
        # Get recent posts
        since_time = datetime.utcnow() - timedelta(hours=hours)
        recent_posts = self.db.query(Post).filter(
            Post.created_at >= since_time
        ).all()
        
        # Get all active bots
        active_bots = self.db.query(Bot).filter(Bot.is_active == True).all()
        
        print(f"Processing {len(recent_posts)} posts for {len(active_bots)} bots...")
        
        interactions_count = 0
        for post in recent_posts:
            for bot in active_bots:
                try:
                    result = self.process_post_for_bot(bot, post)
                    if result:
                        interactions_count += 1
                except Exception as e:
                    print(f"Error processing post {post.id} for bot {bot.name}: {e}")
                    self.db.rollback()
        
        print(f"Bot processing complete! {interactions_count} interactions created.")
        return {
            "posts": len(recent_posts),
            "bots": len(active_bots),
            "interactions": interactions_count
        }
    
    def process_single_post(self, post_id: int):
        """Process a single post for all active bots"""
        post = self.db.query(Post).filter(Post.id == post_id).first()
        if not post:
            return
        
        active_bots = self.db.query(Bot).filter(Bot.is_active == True).all()
        
        for bot in active_bots:
            try:
                self.process_post_for_bot(bot, post)
            except Exception as e:
                print(f"Error processing post {post.id} for bot {bot.name}: {e}")
                self.db.rollback()
