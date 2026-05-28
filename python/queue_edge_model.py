"""
Queue Edge Data Model
JIRA: BITO-12018 - Queue edges should be identified & linked through ai-architect (api flow)

This module defines the data structures for queue edges, including queue operations,
edge metadata, and schema definitions for API integration.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict, field
from enum import Enum
import json
from datetime import datetime


class QueueOperationType(Enum):
    """Queue operation types"""
    PRODUCE = "produce"  # Publishing/sending to queue
    CONSUME = "consume"  # Receiving/reading from queue
    PUBLISH = "publish"
    SUBSCRIBE = "subscribe"
    SEND = "send"
    RECEIVE = "receive"


class QueuePattern(Enum):
    """Common queue patterns"""
    MESSAGE_QUEUE = "message_queue"
    PUBLISH_SUBSCRIBE = "pub_sub"
    REQUEST_REPLY = "request_reply"
    TOPIC = "topic"
    QUEUE = "queue"
    EVENT_STREAM = "event_stream"
    TASK_QUEUE = "task_queue"


@dataclass
class QueueEdgeRequest:
    """Request payload for queue edge"""
    operation: str  # produce, consume, publish, subscribe
    message_type: Optional[str] = None
    schema: Optional[Dict[str, Any]] = None
    encoding: str = "json"
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class QueueEdgeResponse:
    """Response payload for queue edge"""
    status: str  # success, failure, pending
    message: Optional[str] = None
    processing_time_ms: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class QueueEdge:
    """
    Queue Edge Data Model
    Represents a single queue operation in the system
    """
    # Identification
    edge_id: str  # Unique identifier (e.g., "queue_edge_uuid")
    source_identifier: str  # Source service/module name
    queue_identifier: str  # Queue name/identifier
    operation_type: str  # produce, consume, publish, subscribe, etc.
    
    # Metadata
    pattern: str = QueuePattern.MESSAGE_QUEUE.value
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    # Operation Details
    request: Optional[QueueEdgeRequest] = None
    response: Optional[QueueEdgeResponse] = None
    
    # Linking Information
    api_provider_edges: List[str] = field(default_factory=list)  # Incoming edges from API
    queue_call_edges: List[str] = field(default_factory=list)  # Outgoing queue calls
    
    # Additional Metadata
    description: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert edge to dictionary"""
        edge_dict = asdict(self)
        if self.request:
            edge_dict['request'] = self.request.to_dict()
        if self.response:
            edge_dict['response'] = self.response.to_dict()
        return edge_dict
    
    def to_json(self) -> str:
        """Convert edge to JSON string"""
        return json.dumps(self.to_dict(), indent=2)
    
def from_dict(cls, data: Dict[str, Any]) -> 'QueueEdge':
    """Create QueueEdge from dictionary"""
    data = dict(data)
    # Handle nested objects
    if 'request' in data and data['request']:
        data['request'] = QueueEdgeRequest(**data['request'])
    if 'response' in data and data['response']:
        data['response'] = QueueEdgeResponse(**data['response'])

    return cls(**data)


@dataclass
class QueueEdgeCollection:
    """Collection of queue edges for a service/module"""
    service_name: str
    edges: List[QueueEdge] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def add_edge(self, edge: QueueEdge) -> None:
        """Add a queue edge to the collection"""
        self.edges.append(edge)
    
    def get_edges_by_operation(self, operation_type: str) -> List[QueueEdge]:
        """Get all edges of a specific operation type"""
        return [edge for edge in self.edges if edge.operation_type == operation_type]
    
    def get_edges_by_queue(self, queue_identifier: str) -> List[QueueEdge]:
        """Get all edges for a specific queue"""
        return [edge for edge in self.edges if edge.queue_identifier == queue_identifier]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert collection to dictionary"""
        return {
            'service_name': self.service_name,
            'created_at': self.created_at,
            'edge_count': len(self.edges),
            'edges': [edge.to_dict() for edge in self.edges]
        }
    
    def to_json(self) -> str:
        """Convert collection to JSON string"""
        return json.dumps(self.to_dict(), indent=2)


class QueueEdgeSchema:
    """
    Schema definitions for queue edges
    Used for validation and API integration
    """
    
    QUEUE_EDGE_SCHEMA = {
        "type": "object",
        "properties": {
            "edge_id": {"type": "string", "description": "Unique edge identifier"},
            "source_identifier": {"type": "string", "description": "Source service/module"},
            "queue_identifier": {"type": "string", "description": "Queue name"},
            "operation_type": {
                "type": "string",
                "enum": ["produce", "consume", "publish", "subscribe", "send", "receive"],
                "description": "Type of queue operation"
            },
            "pattern": {
                "type": "string",
                "enum": [
                    "message_queue", "pub_sub", "request_reply",
                    "topic", "queue", "event_stream", "task_queue"
                ],
                "description": "Queue pattern"
            },
            "request": {
                "type": "object",
                "properties": {
                    "operation": {"type": "string"},
                    "message_type": {"type": ["string", "null"]},
                    "schema": {"type": ["object", "null"]},
                    "encoding": {"type": "string", "default": "json"}
                }
            },
            "response": {
                "type": "object",
                "properties": {
                    "status": {"type": "string"},
                    "message": {"type": ["string", "null"]},
                    "processing_time_ms": {"type": "integer"}
                }
            },
            "api_provider_edges": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Incoming API provider edges"
            },
            "queue_call_edges": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Outgoing queue call edges"
            },
            "tags": {"type": "array", "items": {"type": "string"}},
            "metadata": {"type": "object"}
        },
        "required": ["edge_id", "source_identifier", "queue_identifier", "operation_type"]
    }
    
    def validate_edge(edge: Dict[str, Any]) -> bool:
        """
        Check that all required fields are present.
        Note: QUEUE_EDGE_SCHEMA is available for full schema validation if jsonschema is installed.
        Returns True if valid, False otherwise
        """
        required_fields = ["edge_id", "source_identifier", "queue_identifier", "operation_type"]
        return all(field in edge for field in required_fields)


# Example usage and helper functions
def create_queue_edge(
    edge_id: str,
    source_identifier: str,
    queue_identifier: str,
    operation_type: str,
    **kwargs
) -> QueueEdge:
    """
    Factory function to create a QueueEdge
    
    Args:
        edge_id: Unique edge identifier
        source_identifier: Source service/module name
        queue_identifier: Queue name/identifier
        operation_type: Type of operation (produce, consume, etc.)
        **kwargs: Additional optional parameters
    
    Returns:
        QueueEdge instance
    """
    return QueueEdge(
        edge_id=edge_id,
        source_identifier=source_identifier,
        queue_identifier=queue_identifier,
        operation_type=operation_type,
        **kwargs
    )


if __name__ == "__main__":
    # Example: Create and display queue edges
    print("=" * 60)
    print("Queue Edge Model - Example Usage")
    print("=" * 60)
    
    # Create a queue edge
    edge = create_queue_edge(
        edge_id="queue_edge_001",
        source_identifier="order_service",
        queue_identifier="order_queue",
        operation_type=QueueOperationType.PRODUCE.value,
        pattern=QueuePattern.MESSAGE_QUEUE.value,
        description="Order service produces messages to order queue",
        tags=["order", "production", "critical"],
        request=QueueEdgeRequest(
            operation="produce",
            message_type="OrderMessage",
            schema={"order_id": "string", "amount": "number"}
        ),
        response=QueueEdgeResponse(
            status="success",
            processing_time_ms=45
        )
    )
    
    print("\n1. Queue Edge Object:")
    print(edge.to_json())
    
    # Create a collection
    collection = QueueEdgeCollection(service_name="order_service")
    collection.add_edge(edge)
    
    # Add another edge
    edge2 = create_queue_edge(
        edge_id="queue_edge_002",
        source_identifier="payment_service",
        queue_identifier="order_queue",
        operation_type=QueueOperationType.CONSUME.value,
        pattern=QueuePattern.MESSAGE_QUEUE.value,
        description="Payment service consumes from order queue"
    )
    collection.add_edge(edge2)
    
    print("\n2. Queue Edge Collection:")
    print(collection.to_json())
    
    print("\n3. Validation:")
    is_valid = QueueEdgeSchema.validate_edge(edge.to_dict())
    print(f"Edge validation result: {is_valid}")
