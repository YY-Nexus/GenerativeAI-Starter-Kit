"""
Text processing utilities for the GenerativeAI Starter Kit
"""
import re
from typing import List, Dict, Any, Optional
from pathlib import Path


class TextProcessor:
    """Text processing and cleaning utilities"""
    
    def __init__(self):
        self.common_words = {
            'english': {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'},
            'chinese': {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也'}
        }
    
    def clean_text(self, text: str, 
                  remove_extra_whitespace: bool = True,
                  remove_special_chars: bool = False,
                  lowercase: bool = False) -> str:
        """
        Clean and normalize text
        
        Args:
            text: Input text to clean
            remove_extra_whitespace: Remove extra spaces and newlines
            remove_special_chars: Remove special characters
            lowercase: Convert to lowercase
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        cleaned = text
        
        # Remove extra whitespace
        if remove_extra_whitespace:
            cleaned = re.sub(r'\s+', ' ', cleaned)
            cleaned = cleaned.strip()
        
        # Remove special characters (keep basic punctuation)
        if remove_special_chars:
            cleaned = re.sub(r'[^\w\s\.\,\!\?\-]', '', cleaned)
        
        # Convert to lowercase
        if lowercase:
            cleaned = cleaned.lower()
        
        return cleaned
    
    def extract_sentences(self, text: str, min_length: int = 10) -> List[str]:
        """
        Extract sentences from text
        
        Args:
            text: Input text
            min_length: Minimum sentence length
            
        Returns:
            List of sentences
        """
        # Simple sentence splitting (can be improved with NLTK/spaCy)
        sentences = re.split(r'[.!?]+', text)
        
        # Clean and filter sentences
        cleaned_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) >= min_length:
                cleaned_sentences.append(sentence)
        
        return cleaned_sentences
    
    def chunk_text(self, text: str, 
                   chunk_size: int = 1000, 
                   overlap: int = 200,
                   preserve_sentences: bool = True) -> List[Dict[str, Any]]:
        """
        Split text into chunks with optional overlap
        
        Args:
            text: Input text to chunk
            chunk_size: Maximum chunk size in characters
            overlap: Overlap between chunks
            preserve_sentences: Try to preserve sentence boundaries
            
        Returns:
            List of chunks with metadata
        """
        if len(text) <= chunk_size:
            return [{
                'text': text,
                'start': 0,
                'end': len(text),
                'chunk_id': 0,
                'word_count': len(text.split())
            }]
        
        chunks = []
        start = 0
        chunk_id = 0
        
        while start < len(text):
            end = start + chunk_size
            
            if preserve_sentences and end < len(text):
                # Try to end at sentence boundary
                sentence_ends = [m.end() for m in re.finditer(r'[.!?]+\s+', text[start:end])]
                if sentence_ends:
                    end = start + sentence_ends[-1]
            
            chunk_text = text[start:end]
            chunks.append({
                'text': chunk_text,
                'start': start,
                'end': end,
                'chunk_id': chunk_id,
                'word_count': len(chunk_text.split())
            })
            
            # Move start position considering overlap
            start = end - overlap
            chunk_id += 1
        
        return chunks
    
    def extract_keywords(self, text: str, 
                        top_k: int = 10,
                        min_word_length: int = 3,
                        language: str = 'english') -> List[Dict[str, Any]]:
        """
        Extract keywords from text using simple frequency analysis
        
        Args:
            text: Input text
            top_k: Number of top keywords to return
            min_word_length: Minimum word length
            language: Language for stop words
            
        Returns:
            List of keywords with scores
        """
        # Clean text
        cleaned_text = self.clean_text(text, lowercase=True, remove_special_chars=True)
        
        # Get words
        words = cleaned_text.split()
        
        # Filter words
        stop_words = self.common_words.get(language, set())
        filtered_words = [
            word for word in words 
            if len(word) >= min_word_length and word not in stop_words
        ]
        
        # Count frequencies
        word_freq = {}
        for word in filtered_words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        # Return top keywords with scores
        keywords = []
        total_words = len(filtered_words)
        
        for word, freq in sorted_words[:top_k]:
            keywords.append({
                'word': word,
                'frequency': freq,
                'score': freq / total_words if total_words > 0 else 0
            })
        
        return keywords
    
    def similarity_score(self, text1: str, text2: str) -> float:
        """
        Calculate simple similarity score between two texts using word overlap
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score (0-1)
        """
        # Clean and tokenize
        words1 = set(self.clean_text(text1, lowercase=True).split())
        words2 = set(self.clean_text(text2, lowercase=True).split())
        
        if not words1 or not words2:
            return 0.0
        
        # Calculate Jaccard similarity
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Simple entity extraction (email, URL, phone numbers, etc.)
        
        Args:
            text: Input text
            
        Returns:
            Dictionary of entity types and their values
        """
        entities = {
            'emails': [],
            'urls': [],
            'phone_numbers': [],
            'numbers': []
        }
        
        # Email pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        entities['emails'] = re.findall(email_pattern, text)
        
        # URL pattern
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        entities['urls'] = re.findall(url_pattern, text)
        
        # Phone number pattern (simple)
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        entities['phone_numbers'] = re.findall(phone_pattern, text)
        
        # Numbers
        number_pattern = r'\b\d+\.?\d*\b'
        entities['numbers'] = re.findall(number_pattern, text)
        
        return entities
    
    def summarize_text(self, text: str, max_sentences: int = 3) -> str:
        """
        Simple extractive text summarization
        
        Args:
            text: Input text
            max_sentences: Maximum sentences in summary
            
        Returns:
            Summary text
        """
        sentences = self.extract_sentences(text)
        
        if len(sentences) <= max_sentences:
            return text
        
        # Score sentences by word frequency
        word_freq = {}
        for sentence in sentences:
            words = self.clean_text(sentence, lowercase=True).split()
            for word in words:
                if len(word) > 3:  # Skip short words
                    word_freq[word] = word_freq.get(word, 0) + 1
        
        # Score sentences
        sentence_scores = []
        for i, sentence in enumerate(sentences):
            words = self.clean_text(sentence, lowercase=True).split()
            score = sum(word_freq.get(word, 0) for word in words if len(word) > 3)
            sentence_scores.append((score, i, sentence))
        
        # Select top sentences
        sentence_scores.sort(reverse=True)
        top_sentences = sorted(sentence_scores[:max_sentences], key=lambda x: x[1])
        
        return ' '.join([sentence for _, _, sentence in top_sentences])


if __name__ == "__main__":
    # Example usage
    processor = TextProcessor()
    
    sample_text = """
    Machine learning is a method of data analysis that automates analytical model building. 
    It is a branch of artificial intelligence (AI) based on the idea that systems can learn 
    from data, identify patterns and make decisions with minimal human intervention. 
    Machine learning algorithms build a model based on sample data, known as training data, 
    in order to make predictions or decisions without being explicitly programmed to do so.
    """
    
    print("Original text:")
    print(sample_text)
    print()
    
    # Clean text
    cleaned = processor.clean_text(sample_text)
    print(f"Cleaned text: {cleaned}")
    print()
    
    # Extract sentences
    sentences = processor.extract_sentences(sample_text)
    print(f"Sentences ({len(sentences)}):")
    for i, sentence in enumerate(sentences, 1):
        print(f"{i}. {sentence}")
    print()
    
    # Extract keywords
    keywords = processor.extract_keywords(sample_text, top_k=5)
    print("Top keywords:")
    for kw in keywords:
        print(f"- {kw['word']}: {kw['frequency']} ({kw['score']:.3f})")
    print()
    
    # Chunk text
    chunks = processor.chunk_text(sample_text, chunk_size=100)
    print(f"Text chunks ({len(chunks)}):")
    for chunk in chunks:
        print(f"Chunk {chunk['chunk_id']}: {chunk['text'][:50]}...")
    print()
    
    # Summarize
    summary = processor.summarize_text(sample_text, max_sentences=2)
    print(f"Summary: {summary}")
    print()
    
    # Extract entities
    entity_text = "Contact us at info@example.com or visit https://example.com or call 555-123-4567"
    entities = processor.extract_entities(entity_text)
    print(f"Entities in '{entity_text}':")
    for entity_type, values in entities.items():
        if values:
            print(f"- {entity_type}: {values}")