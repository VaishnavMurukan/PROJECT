import requests
from typing import List, Dict, Any
from ..models.schemas import DataSourceRequest, TextData

class DataIngestionService:
    """Service to fetch data from external APIs"""
    
    def __init__(self):
        self.session = requests.Session()
    
    def fetch_from_api(self, request: DataSourceRequest) -> List[TextData]:
        """
        Fetch data from an external API.
        This method is platform-agnostic and works with any API that returns
        data in a compatible JSON format.
        """
        try:
            # Build query parameters
            params = {}
            if request.language:
                params['language'] = request.language
            if request.date_from:
                params['date_from'] = request.date_from.isoformat()
            if request.date_to:
                params['date_to'] = request.date_to.isoformat()
            if request.filters:
                params.update(request.filters)
            
            # Make API request
            response = self.session.get(
                str(request.source_api),
                params=params,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Parse response based on data type
            if request.data_type == "comments":
                return self._parse_comments(data)
            elif request.data_type == "posts":
                return self._parse_posts(data)
            else:
                return self._parse_generic(data)
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching data from API: {str(e)}")
    
    def _parse_comments(self, data: List[Dict]) -> List[TextData]:
        """Parse comment data"""
        text_data = []
        for item in data:
            text_data.append(TextData(
                id=item.get('id'),
                text=item.get('content', item.get('text', '')),
                created_at=item.get('created_at'),
                metadata={
                    'is_bot': item.get('is_bot', False),
                    'type': 'comment'
                }
            ))
        return text_data
    
    def _parse_posts(self, data: List[Dict]) -> List[TextData]:
        """Parse post data, including comments"""
        text_data = []
        for post in data:
            # Add post content
            text_data.append(TextData(
                id=post.get('id'),
                text=post.get('content', ''),
                created_at=post.get('created_at'),
                metadata={
                    'type': 'post',
                    'topic': post.get('topic'),
                    'likes': post.get('likes', 0),
                    'dislikes': post.get('dislikes', 0)
                }
            ))
            
            # Add comments from the post
            if 'comments' in post:
                for comment in post['comments']:
                    text_data.append(TextData(
                        id=comment.get('id'),
                        text=comment.get('content', ''),
                        created_at=comment.get('created_at'),
                        metadata={
                            'type': 'comment',
                            'post_id': post.get('id'),
                            'is_bot': comment.get('is_bot', False)
                        }
                    ))
        
        return text_data
    
    def _parse_generic(self, data: List[Dict]) -> List[TextData]:
        """Parse generic text data"""
        text_data = []
        for item in data:
            # Try to find text field with common names
            text = item.get('text', item.get('content', item.get('message', '')))
            if text:
                text_data.append(TextData(
                    id=item.get('id', 0),
                    text=text,
                    created_at=item.get('created_at', item.get('timestamp')),
                    metadata=item
                ))
        return text_data
    
    def validate_data_sufficiency(self, data: List[TextData], min_samples: int = 10) -> Dict[str, Any]:
        """
        Validate if the fetched data is sufficient for reliable analysis
        """
        total_samples = len(data)
        
        if total_samples == 0:
            return {
                "sufficient": False,
                "reason": "No data found",
                "total_samples": 0,
                "recommendation": "Check the API endpoint and filters"
            }
        
        if total_samples < min_samples:
            return {
                "sufficient": False,
                "reason": f"Insufficient samples (minimum: {min_samples})",
                "total_samples": total_samples,
                "recommendation": "Collect more data or adjust date range"
            }
        
        # Check text quality
        empty_texts = sum(1 for item in data if not item.text.strip())
        if empty_texts > total_samples * 0.5:
            return {
                "sufficient": False,
                "reason": "Too many empty texts",
                "total_samples": total_samples,
                "empty_texts": empty_texts,
                "recommendation": "Check data quality at source"
            }
        
        # Calculate vocabulary diversity
        all_words = set()
        for item in data:
            all_words.update(item.text.lower().split())
        
        vocab_size = len(all_words)
        avg_vocab_per_text = vocab_size / total_samples if total_samples > 0 else 0
        
        return {
            "sufficient": True,
            "total_samples": total_samples,
            "empty_texts": empty_texts,
            "vocabulary_size": vocab_size,
            "avg_vocab_per_text": round(avg_vocab_per_text, 2),
            "recommendation": "Data quality is good for analysis"
        }
