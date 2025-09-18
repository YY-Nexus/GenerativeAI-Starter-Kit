#!/usr/bin/env python3
"""
Customer Service Bot - Industry Solution Example

This example demonstrates how to build an intelligent customer service chatbot using RAG
that can answer customer questions based on:
- Product documentation
- FAQ databases
- Company policies
- Previous support tickets

Features:
- Context-aware responses
- Ticket classification
- Sentiment analysis
- Escalation detection
- Multi-language support
"""

import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
import json
from datetime import datetime

# Add src to path
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from rag.pipeline import RAGPipeline
from utils.text_processing import TextProcessor


class CustomerServiceBot:
    """Intelligent customer service chatbot"""
    
    def __init__(self, 
                 knowledge_base_path: Optional[str] = None,
                 model_config: Optional[Dict] = None):
        """
        Initialize customer service bot
        
        Args:
            knowledge_base_path: Path to knowledge base documents
            model_config: Model configuration options
        """
        self.text_processor = TextProcessor()
        
        # Initialize RAG pipeline for customer service
        self.rag_pipeline = RAGPipeline(
            vector_store_type="chroma",
            llm_provider="openai",
            collection_name="customer_service_kb",
            top_k=5,
            similarity_threshold=0.4,
            response_template=self._get_customer_service_template()
        )
        
        # Customer interaction tracking
        self.conversation_history = []
        self.customer_context = {}
        
        # Load knowledge base if provided
        if knowledge_base_path:
            self.load_knowledge_base(knowledge_base_path)
    
    def _get_customer_service_template(self) -> str:
        """Get specialized template for customer service responses"""
        return """You are a helpful and professional customer service assistant. Use the following context to provide accurate, friendly, and helpful responses to customer inquiries.

Context from Knowledge Base:
{context}

Customer Question: {question}

Instructions:
- Be polite, professional, and empathetic
- Provide specific, actionable information when possible
- If you cannot fully answer the question, suggest next steps or escalation
- Include relevant policy information or documentation references
- Keep responses concise but comprehensive

Response:"""
    
    def load_knowledge_base(self, knowledge_base_path: str) -> Dict[str, Any]:
        """
        Load customer service knowledge base
        
        Args:
            knowledge_base_path: Path to knowledge base directory or file
            
        Returns:
            Loading results
        """
        kb_path = Path(knowledge_base_path)
        
        if kb_path.is_file():
            # Single file
            documents = [self._load_document(kb_path)]
            metadata = [{"source": kb_path.name, "type": "knowledge_base"}]
        elif kb_path.is_dir():
            # Directory of files
            documents = []
            metadata = []
            
            for file_path in kb_path.glob("**/*.txt"):
                try:
                    doc_content = self._load_document(file_path)
                    documents.append(doc_content)
                    metadata.append({
                        "source": file_path.name,
                        "type": self._classify_document_type(file_path.name),
                        "path": str(file_path)
                    })
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")
        else:
            # Use sample knowledge base
            documents, metadata = self._get_sample_knowledge_base()
        
        # Add documents to RAG pipeline
        result = self.rag_pipeline.add_documents(documents, metadata)
        print(f"✅ Loaded {result['documents_added']} documents into knowledge base")
        
        return result
    
    def _load_document(self, file_path: Path) -> str:
        """Load content from a document file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return ""
    
    def _classify_document_type(self, filename: str) -> str:
        """Classify document type based on filename"""
        filename_lower = filename.lower()
        
        if 'faq' in filename_lower:
            return 'faq'
        elif 'policy' in filename_lower or 'terms' in filename_lower:
            return 'policy'
        elif 'product' in filename_lower or 'manual' in filename_lower:
            return 'product_info'
        elif 'troubleshoot' in filename_lower:
            return 'troubleshooting'
        else:
            return 'general'
    
    def _get_sample_knowledge_base(self) -> tuple:
        """Get sample customer service knowledge base"""
        documents = [
            """
            FREQUENTLY ASKED QUESTIONS - Account Management
            
            Q: How do I reset my password?
            A: To reset your password, go to the login page and click "Forgot Password". Enter your email address and follow the instructions sent to your email. If you don't receive the email within 10 minutes, check your spam folder.
            
            Q: How do I update my billing information?
            A: Log into your account, go to Settings > Billing, and click "Update Payment Method". You can add a new credit card or update your existing one. Changes take effect immediately.
            
            Q: Can I cancel my subscription anytime?
            A: Yes, you can cancel your subscription at any time. Go to Settings > Subscription and click "Cancel". Your account will remain active until the end of your current billing period.
            """,
            
            """
            PRODUCT INFORMATION - Premium Features
            
            Our Premium plan includes:
            - Advanced AI capabilities with GPT-4 access
            - Unlimited document uploads (up to 100MB per file)
            - Priority customer support with 24-hour response time
            - Custom model fine-tuning options
            - API access with higher rate limits (1000 requests/hour)
            - Data export and backup features
            - Team collaboration tools for up to 10 users
            
            Pricing: $29.99/month or $299/year (save 2 months)
            Free trial: 14 days, no credit card required
            """,
            
            """
            TROUBLESHOOTING GUIDE - Common Issues
            
            Issue: "Upload failed" error
            Solution: Check file size (max 100MB), ensure supported format (PDF, DOCX, TXT), and verify internet connection. Clear browser cache if problem persists.
            
            Issue: Slow response times
            Solution: This may occur during peak hours. Try again in a few minutes. Premium users have priority processing.
            
            Issue: API key not working
            Solution: Verify the API key is correct and not expired. Check that you haven't exceeded rate limits. Regenerate key if needed in Settings > API.
            
            Issue: Documents not being processed
            Solution: Ensure documents contain readable text. Scanned images need OCR processing. Contact support for files over 50MB.
            """,
            
            """
            COMPANY POLICIES - Terms of Service
            
            Data Privacy: We take your privacy seriously. Your data is encrypted at rest and in transit. We do not share your personal information with third parties without consent.
            
            Content Policy: Users are responsible for uploaded content. Prohibited content includes illegal material, spam, malware, or content that violates intellectual property rights.
            
            Refund Policy: We offer a 30-day money-back guarantee for annual subscriptions. Monthly subscriptions are not eligible for refunds but can be cancelled anytime.
            
            Service Availability: We aim for 99.9% uptime. Scheduled maintenance is announced 48 hours in advance.
            """,
            
            """
            CONTACT INFORMATION - Support Channels
            
            Email Support: support@example.com (24-48 hour response time)
            Premium Support: premium@example.com (4-8 hour response time for Premium users)
            
            Live Chat: Available Mon-Fri 9 AM - 6 PM EST on our website
            
            Community Forum: forum.example.com for user discussions and tips
            
            Emergency Issues: For critical outages, check status.example.com for updates
            
            Sales Inquiries: sales@example.com for enterprise and custom solutions
            """
        ]
        
        metadata = [
            {"source": "FAQ_Account.txt", "type": "faq", "category": "account"},
            {"source": "Product_Premium.txt", "type": "product_info", "category": "features"},
            {"source": "Troubleshooting_Guide.txt", "type": "troubleshooting", "category": "technical"},
            {"source": "Company_Policies.txt", "type": "policy", "category": "legal"},
            {"source": "Contact_Info.txt", "type": "contact", "category": "support"}
        ]
        
        return documents, metadata
    
    def analyze_customer_query(self, query: str) -> Dict[str, Any]:
        """
        Analyze customer query for intent, sentiment, and urgency
        
        Args:
            query: Customer's message
            
        Returns:
            Analysis results
        """
        # Extract entities and keywords
        entities = self.text_processor.extract_entities(query)
        keywords = self.text_processor.extract_keywords(query, top_k=5)
        
        # Simple intent classification
        intent = self._classify_intent(query.lower())
        
        # Simple sentiment analysis
        sentiment = self._analyze_sentiment(query.lower())
        
        # Urgency detection
        urgency = self._detect_urgency(query.lower())
        
        return {
            "intent": intent,
            "sentiment": sentiment,
            "urgency": urgency,
            "entities": entities,
            "keywords": [kw["word"] for kw in keywords],
            "query_length": len(query.split()),
            "has_question_mark": "?" in query
        }
    
    def _classify_intent(self, query: str) -> str:
        """Simple intent classification"""
        if any(word in query for word in ["password", "login", "signin", "account"]):
            return "account_issue"
        elif any(word in query for word in ["billing", "payment", "charge", "subscription"]):
            return "billing_inquiry"
        elif any(word in query for word in ["cancel", "refund", "unsubscribe"]):
            return "cancellation"
        elif any(word in query for word in ["error", "problem", "issue", "bug", "broken"]):
            return "technical_support"
        elif any(word in query for word in ["feature", "how to", "tutorial", "guide"]):
            return "how_to_question"
        elif any(word in query for word in ["price", "cost", "plan", "upgrade"]):
            return "pricing_inquiry"
        else:
            return "general_inquiry"
    
    def _analyze_sentiment(self, query: str) -> str:
        """Simple sentiment analysis"""
        positive_words = ["thank", "great", "love", "excellent", "good", "happy", "satisfied"]
        negative_words = ["hate", "terrible", "awful", "bad", "angry", "frustrated", "disappointed"]
        
        positive_count = sum(1 for word in positive_words if word in query)
        negative_count = sum(1 for word in negative_words if word in query)
        
        if negative_count > positive_count:
            return "negative"
        elif positive_count > negative_count:
            return "positive"
        else:
            return "neutral"
    
    def _detect_urgency(self, query: str) -> str:
        """Detect urgency level"""
        urgent_words = ["urgent", "emergency", "asap", "immediately", "critical", "broken", "down"]
        high_words = ["important", "soon", "quickly", "issue", "problem"]
        
        if any(word in query for word in urgent_words) or "!!!" in query:
            return "urgent"
        elif any(word in query for word in high_words) or query.count("!") >= 2:
            return "high"
        else:
            return "normal"
    
    def handle_customer_query(self, query: str, customer_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Handle a customer query end-to-end
        
        Args:
            query: Customer's question or message
            customer_id: Optional customer identifier
            
        Returns:
            Complete response with analysis and answer
        """
        # Analyze the query
        analysis = self.analyze_customer_query(query)
        
        # Get AI response using RAG
        rag_response = self.rag_pipeline.query(
            query,
            include_sources=True,
            conversation_mode=True,
            temperature=0.3,  # More focused responses for customer service
            max_tokens=400
        )
        
        # Prepare response
        response = {
            "customer_id": customer_id,
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "analysis": analysis,
            "answer": rag_response["answer"],
            "sources": rag_response.get("sources", []),
            "confidence_score": self._calculate_confidence(rag_response),
            "escalation_recommended": self._should_escalate(analysis, rag_response),
            "suggested_actions": self._get_suggested_actions(analysis)
        }
        
        # Store in conversation history
        self.conversation_history.append(response)
        
        return response
    
    def _calculate_confidence(self, rag_response: Dict) -> float:
        """Calculate confidence score for the response"""
        base_confidence = 0.5
        
        # Higher confidence if sources found
        if rag_response.get("sources"):
            base_confidence += 0.3
            
            # Even higher if multiple high-relevance sources
            avg_relevance = sum(s.get("relevance_score", 0) for s in rag_response["sources"]) / len(rag_response["sources"])
            base_confidence += avg_relevance * 0.2
        
        # Lower confidence for very long or very short responses
        answer_length = len(rag_response.get("answer", "").split())
        if 50 <= answer_length <= 200:
            base_confidence += 0.1
        elif answer_length < 20 or answer_length > 400:
            base_confidence -= 0.1
        
        return min(1.0, max(0.0, base_confidence))
    
    def _should_escalate(self, analysis: Dict, rag_response: Dict) -> bool:
        """Determine if query should be escalated to human agent"""
        # Escalate for urgent issues
        if analysis["urgency"] == "urgent":
            return True
        
        # Escalate for negative sentiment + technical issues
        if analysis["sentiment"] == "negative" and analysis["intent"] == "technical_support":
            return True
        
        # Escalate if confidence is low
        confidence = self._calculate_confidence(rag_response)
        if confidence < 0.4:
            return True
        
        # Escalate for billing/cancellation issues
        if analysis["intent"] in ["billing_inquiry", "cancellation"]:
            return True
        
        return False
    
    def _get_suggested_actions(self, analysis: Dict) -> List[str]:
        """Get suggested follow-up actions"""
        actions = []
        
        if analysis["intent"] == "account_issue":
            actions.extend([
                "Offer to send password reset link",
                "Verify customer identity",
                "Check account status"
            ])
        elif analysis["intent"] == "technical_support":
            actions.extend([
                "Gather system information",
                "Request error screenshots",
                "Check service status"
            ])
        elif analysis["intent"] == "billing_inquiry":
            actions.extend([
                "Review billing history",
                "Verify payment method",
                "Explain charges"
            ])
        
        if analysis["sentiment"] == "negative":
            actions.append("Acknowledge frustration and apologize")
        
        if analysis["urgency"] == "urgent":
            actions.append("Prioritize response and consider immediate escalation")
        
        return actions
    
    def get_conversation_summary(self, customer_id: Optional[str] = None) -> Dict[str, Any]:
        """Get summary of customer conversations"""
        relevant_conversations = [
            conv for conv in self.conversation_history
            if customer_id is None or conv.get("customer_id") == customer_id
        ]
        
        if not relevant_conversations:
            return {"message": "No conversations found"}
        
        # Analyze conversation patterns
        intents = [conv["analysis"]["intent"] for conv in relevant_conversations]
        sentiments = [conv["analysis"]["sentiment"] for conv in relevant_conversations]
        
        return {
            "total_conversations": len(relevant_conversations),
            "date_range": {
                "start": relevant_conversations[0]["timestamp"],
                "end": relevant_conversations[-1]["timestamp"]
            },
            "common_intents": list(set(intents)),
            "sentiment_distribution": {
                "positive": sentiments.count("positive"),
                "neutral": sentiments.count("neutral"),
                "negative": sentiments.count("negative")
            },
            "escalations_recommended": sum(1 for conv in relevant_conversations if conv["escalation_recommended"]),
            "average_confidence": sum(conv["confidence_score"] for conv in relevant_conversations) / len(relevant_conversations)
        }


def main():
    """Demo the customer service bot"""
    print("🤖 Customer Service Bot - Demo")
    print("=" * 50)
    
    # Initialize bot
    print("Initializing customer service bot...")
    bot = CustomerServiceBot()
    
    # Sample customer queries
    test_queries = [
        "I forgot my password and can't login to my account. This is urgent!",
        "How much does the premium plan cost?",
        "My file upload keeps failing with an error message",
        "I want to cancel my subscription",
        "Thank you for the great service! How do I upgrade to premium?",
        "The API is not working and my app is down. Please help immediately!"
    ]
    
    print(f"\n📝 Processing {len(test_queries)} sample customer queries...")
    print("=" * 50)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔹 Query {i}: {query}")
        print("-" * 40)
        
        # Process query
        response = bot.handle_customer_query(query, customer_id=f"customer_{i}")
        
        # Display results
        print(f"🎯 Intent: {response['analysis']['intent']}")
        print(f"😊 Sentiment: {response['analysis']['sentiment']}")
        print(f"⚡ Urgency: {response['analysis']['urgency']}")
        print(f"🎯 Confidence: {response['confidence_score']:.2f}")
        print(f"🚨 Escalate: {'Yes' if response['escalation_recommended'] else 'No'}")
        
        print(f"\n🤖 Response:")
        print(response['answer'])
        
        if response.get('sources'):
            print(f"\n📚 Sources:")
            for source in response['sources']:
                print(f"   • {source['name']}")
        
        if response['suggested_actions']:
            print(f"\n💡 Suggested Actions:")
            for action in response['suggested_actions']:
                print(f"   • {action}")
        
        print("=" * 50)
    
    # Show conversation summary
    print("\n📊 Conversation Summary:")
    summary = bot.get_conversation_summary()
    print(f"Total conversations: {summary['total_conversations']}")
    print(f"Common intents: {', '.join(summary['common_intents'])}")
    print(f"Sentiment distribution: {summary['sentiment_distribution']}")
    print(f"Escalations recommended: {summary['escalations_recommended']}")
    print(f"Average confidence: {summary['average_confidence']:.2f}")
    
    print("\n🎉 Customer service bot demo completed!")
    print("\nNext steps:")
    print("- Integrate with your customer support platform")
    print("- Add real customer data and conversation history")
    print("- Customize knowledge base with your documentation")
    print("- Implement escalation workflows")
    print("- Add sentiment analysis and customer satisfaction tracking")


if __name__ == "__main__":
    main()