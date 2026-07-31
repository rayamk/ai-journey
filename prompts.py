class PromptTemplates:
    """Prompt templates for different content types"""
    
    @staticmethod
    def get_ideas_prompt(topic, platform, audience, style, language):
        return f"""Generate 5 creative content ideas for a {style} style post about "{topic}" 
        on {platform} platform targeting {audience} audience.
        
        The ideas should be:
        - Attention-grabbing and unique
        - Platform-appropriate for {platform}
        - Engaging for Myanmar audience
        - Practical and actionable
        - Relevant to current trends
        
        Format: Numbered list with brief description (2-3 sentences each)
        
        Response in {language}:"""
    
    @staticmethod
    def get_hooks_prompt(topic, platform, style, language):
        return f"""Create 5 attention-grabbing hooks for a {style} video/post about "{topic}" 
        on {platform}.
        
        Hooks should:
        - Be compelling and curiosity-driven
        - Start with strong opening words
        - Be platform-appropriate for {platform}
        - Relate to Myanmar audience interests
        - Create emotional connection or curiosity
        
        Format: Numbered list of hooks (1 sentence each)
        
        Response in {language}:"""
    
    @staticmethod
    def get_script_prompt(topic, platform, audience, style, language):
        return f"""Write a short {style} video script (15-30 seconds) about "{topic}" 
        for {platform} targeting {audience}.
        
        Script should include:
        - An attention-grabbing opening hook
        - 3-4 key points or message
        - A clear call-to-action
        - {style} tone throughout
        - Visual or action suggestions if applicable
        - Engagement trigger for {platform} audience
        
        Format: 
        HOOK: [opening hook]
        CONTENT: [main content with key points]
        CTA: [call to action]
        
        Response in {language}:"""
    
    @staticmethod
    def get_captions_prompt(topic, platform, style, language):
        return f"""Generate 3 engaging captions for a {style} post about "{topic}" 
        on {platform}.
        
        Captions should:
        - Be platform-appropriate length for {platform}
        - Include relevant emojis where suitable
        - Have a clear and compelling message
        - Encourage engagement (likes, comments, shares)
        - Match the {style} tone
        - Include a question or prompt for audience interaction
        
        Format: Numbered list of captions (2-3 sentences each, with emojis)
        
        Response in {language}:"""
    
    @staticmethod
    def get_hashtags_prompt(topic, platform, language):
        return f"""Generate relevant hashtags for a post about "{topic}" 
        on {platform}.
        
        Include:
        - 5 popular/general hashtags
        - 3 niche-specific hashtags
        - 2 location-based hashtags (Myanmar related)
        - Brief explanation for each hashtag
        
        Hashtags should be:
        - Relevant to the topic
        - Searchable and popular
        - Mix of broad and specific tags
        - Myanmar-relevant where applicable
        
        Format: List of hashtags with brief explanation of each
        
        Response in {language}:"""
