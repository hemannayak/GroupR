import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional
from datetime import datetime
from loguru import logger

from backend.models import DisasterEvent, DisasterType, Severity


class DisasterVectorStore:
    def __init__(self, persist_dir: str = "chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(name="disaster_events")
        self.encoder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    def add_tweets(self, events: List[DisasterEvent]):
        """Embed tweet text and store with metadata."""
        if not events:
            return
        
        documents = []
        metadatas = []
        ids = []
        
        for event in events:
            documents.append(event.text)
            metadatas.append({
                "id": event.id,
                "disaster_type": event.disaster_type.value,
                "severity": event.severity.value,
                "location": event.location or "",
                "timestamp": event.timestamp.isoformat(),
                "source": event.source,
                "lat": event.coordinates[0] if event.coordinates else None,
                "lon": event.coordinates[1] if event.coordinates else None,
            })
            ids.append(event.id)
        
        # Batch add
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            self.collection.add(
                documents=documents[i:i+batch_size],
                metadatas=metadatas[i:i+batch_size],
                ids=ids[i:i+batch_size]
            )
        
        logger.info(f"Added {len(documents)} events to vector store")
    
    def add_events(self, events: List[DisasterEvent]):
        """Alias for add_tweets"""
        return self.add_tweets(events)

    def query(self, query_text: str, k: int = 5, filters: Optional[Dict] = None) -> List[DisasterEvent]:
        """Query vector store and return full DisasterEvent objects"""
        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=k,
                where=filters
            )
            
            if not results or not results['documents'][0]:
                return []
            
            events = []
            for i in range(len(results['documents'][0])):
                metadata = results['metadatas'][0][i]
                document = results['documents'][0][i]
                
                # Reconstruct DisasterEvent from metadata
                event = DisasterEvent(
                    id=metadata['id'],
                    text=document,
                    timestamp=datetime.fromisoformat(metadata['timestamp']),
                    location=metadata['location'],
                    coordinates=(metadata.get('lat'), metadata.get('lon')) if metadata.get('lat') else None,
                    disaster_type=DisasterType(metadata['disaster_type']),
                    severity=Severity(metadata['severity']),
                    confidence=0.8,  # Default
                    source=metadata['source'],
                    needs=[],
                    is_verified=False
                )
                events.append(event)
            
            return events
            
        except Exception as e:
            logger.error(f"Query error: {e}")
            return []

    def get_stats(self) -> Dict:
        """Return collection statistics."""
        try:
            count = self.collection.count()
            return {
                'total_documents': count,
                'collection_name': 'disaster_events'
            }
        except:
            return {
                'total_documents': 0,
                'collection_name': 'disaster_events'
            }
