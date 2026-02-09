"""
Enhanced Queue Manager with Edge Tracking
JIRA: BITO-12018 - Queue edges should be identified & linked through ai-architect (api flow)

This module extends the basic queue functionality with queue edge tracking,
API integration, and edge detection capabilities.
"""

import heapq
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from queue_edge_model import QueueEdge, QueueEdgeCollection, create_queue_edge
from queue_edge_detector import QueueEdgeDetector
from queue_edge_linker import EdgeLinker
from queue_edge_api import QueueEdgeIntegrationManager
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QueueMessage:
    """Represents a message in the queue with metadata"""
    
    def __init__(self, priority: int, task_id: int, description: str, metadata: Optional[Dict] = None):
        self.priority = priority
        self.task_id = task_id
        self.description = description
        self.metadata = metadata or {}
        self.created_at = datetime.utcnow()
        self.processed_at: Optional[datetime] = None
    
    def __lt__(self, other):
        """For heap comparison"""
        return self.priority < other.priority
    
    def mark_processed(self):
        """Mark message as processed"""
        self.processed_at = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "priority": self.priority,
            "task_id": self.task_id,
            "description": self.description,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "processed_at": self.processed_at.isoformat() if self.processed_at else None
        }


class EnhancedTaskManager:
    """
    Enhanced task manager with queue edge tracking
    Extends the basic TaskManager with edge detection and API integration
    """
    
    def __init__(
        self,
        service_name: str,
        api_base_url: Optional[str] = None,
        api_key: Optional[str] = None
    ):
        """
        Initialize enhanced task manager
        
        Args:
            service_name: Name of the service
            api_base_url: Optional base URL for API integration
            api_key: Optional API key
        """
        self.service_name = service_name
        self.tasks: List[QueueMessage] = []
        self.task_id_counter = 1
        self.processed_tasks: List[QueueMessage] = []
        
        # Edge tracking
        self.queue_edges: Dict[str, QueueEdge] = {}
        self.edge_detector = QueueEdgeDetector()
        self.edge_linker = EdgeLinker()
        
        # API integration
        self.api_integration_manager: Optional[QueueEdgeIntegrationManager] = None
        if api_base_url:
            self.api_integration_manager = QueueEdgeIntegrationManager(api_base_url, api_key)
        
        # Callbacks
        self.on_task_added: List[Callable] = []
        self.on_task_processed: List[Callable] = []
    
    def add_task(
        self,
        priority: int,
        description: str,
        metadata: Optional[Dict] = None,
        queue_name: str = "default_queue"
    ) -> str:
        """
        Add a task to the queue with edge tracking
        
        Args:
            priority: Task priority
            description: Task description
            metadata: Optional metadata
            queue_name: Name of the queue
        
        Returns:
            Task ID
        """
        message = QueueMessage(priority, self.task_id_counter, description, metadata)
        heapq.heappush(self.tasks, message)
        
        # Create and track queue edge
        edge_id = f"queue_edge_{self.service_name}_{self.task_id_counter}"
        edge = create_queue_edge(
            edge_id=edge_id,
            source_identifier=self.service_name,
            queue_identifier=queue_name,
            operation_type="produce",
            description=f"Task {self.task_id_counter}: {description}",
            metadata={
                "priority": priority,
                "message": message.to_dict()
            }
        )
        
        self.queue_edges[edge_id] = edge
        self.edge_linker.register_queue_edge(edge)
        
        logger.info(f"Task added: ID={self.task_id_counter}, Priority={priority}, Queue={queue_name}")
        
        # Call callbacks
        for callback in self.on_task_added:
            callback(message, edge)
        
        self.task_id_counter += 1
        return edge_id
    
    def get_next_task(self) -> Optional[QueueMessage]:
        """
        Get and process the next task
        
        Returns:
            Next task or None if queue is empty
        """
        if not self.tasks:
            return None
        
        message = heapq.heappop(self.tasks)
        message.mark_processed()
        self.processed_tasks.append(message)
        
        logger.info(f"Task processed: ID={message.task_id}, Priority={message.priority}")
        
        # Call callbacks
        for callback in self.on_task_processed:
            callback(message)
        
        return message
    
    def display_tasks(self) -> None:
        """Display all current tasks"""
        print(f"\n{'=' * 60}")
        print(f"Current Tasks in {self.service_name}")
        print(f"{'=' * 60}")
        
        if not self.tasks:
            print("No tasks in queue")
            return
        
        for task in sorted(self.tasks, key=lambda t: t.priority):
            print(f"Task ID: {task.task_id}, Priority: {task.priority}, Description: {task.description}")
    
    def display_queue_edges(self) -> None:
        """Display all tracked queue edges"""
        print(f"\n{'=' * 60}")
        print(f"Queue Edges for {self.service_name}")
        print(f"{'=' * 60}")
        
        if not self.queue_edges:
            print("No queue edges tracked")
            return
        
        for edge_id, edge in self.queue_edges.items():
            print(f"\nEdge ID: {edge_id}")
            print(f"  Source: {edge.source_identifier}")
            print(f"  Queue: {edge.queue_identifier}")
            print(f"  Operation: {edge.operation_type}")
            print(f"  Pattern: {edge.pattern}")
            if edge.description:
                print(f"  Description: {edge.description}")
    
    def detect_edges_from_directory(self, directory_path: str) -> QueueEdgeCollection:
        """
        Detect queue edges from source code in a directory
        
        Args:
            directory_path: Path to directory to scan
        
        Returns:
            QueueEdgeCollection with detected edges
        """
        logger.info(f"Detecting queue edges in: {directory_path}")
        collection = self.edge_detector.detect_in_directory(directory_path, self.service_name)
        
        # Register detected edges
        for edge in collection.edges:
            self.queue_edges[edge.edge_id] = edge
            self.edge_linker.register_queue_edge(edge)
        
        logger.info(f"Detected {len(collection.edges)} queue edges")
        return collection
    
    def get_edge_collection(self) -> QueueEdgeCollection:
        """
        Get all tracked queue edges as a collection
        
        Returns:
            QueueEdgeCollection
        """
        collection = QueueEdgeCollection(service_name=self.service_name)
        for edge in self.queue_edges.values():
            collection.add_edge(edge)
        return collection
    
    def sync_edges_to_api(self) -> Optional[Dict[str, Any]]:
        """
        Sync queue edges to the API
        
        Returns:
            Sync results or None if API integration not configured
        """
        if not self.api_integration_manager:
            logger.warning("API integration not configured")
            return None
        
        collection = self.get_edge_collection()
        return self.api_integration_manager.process_and_sync(collection)
    
    def get_edge_graph(self) -> Dict[str, Any]:
        """
        Get the complete edge graph
        
        Returns:
            Edge graph dictionary
        """
        return self.edge_linker.get_edge_graph()
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get queue statistics including edge information
        
        Returns:
            Statistics dictionary
        """
        return {
            "service_name": self.service_name,
            "pending_tasks": len(self.tasks),
            "processed_tasks": len(self.processed_tasks),
            "total_tasks": self.task_id_counter - 1,
            "tracked_edges": len(self.queue_edges),
            "api_integration": self.api_integration_manager is not None,
            "edge_statistics": {
                "produce_edges": len([e for e in self.queue_edges.values() if e.operation_type == "produce"]),
                "consume_edges": len([e for e in self.queue_edges.values() if e.operation_type == "consume"]),
                "linked_edges": sum(len(e.queue_call_edges) for e in self.queue_edges.values())
            }
        }
    
    def register_task_added_callback(self, callback: Callable) -> None:
        """Register callback for when task is added"""
        self.on_task_added.append(callback)
    
    def register_task_processed_callback(self, callback: Callable) -> None:
        """Register callback for when task is processed"""
        self.on_task_processed.append(callback)
    
    def export_to_json(self) -> str:
        """Export queue state to JSON"""
        import json
        collection = self.get_edge_collection()
        return collection.to_json()


# Backward compatibility - extend original TaskManager
class TaskManager:
    """
    Original TaskManager for backward compatibility
    Now uses EnhancedTaskManager internally
    """
    
    def __init__(self):
        self.enhanced_manager = EnhancedTaskManager("default_service")
    
    def add_task(self, priority: int, description: str) -> None:
        """Add task (original interface)"""
        self.enhanced_manager.add_task(priority, description)
    
    def get_next_task(self) -> Optional[QueueMessage]:
        """Get next task (original interface)"""
        return self.enhanced_manager.get_next_task()
    
    def display_tasks(self) -> None:
        """Display tasks (original interface)"""
        self.enhanced_manager.display_tasks()


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("Enhanced Queue Manager - Example Usage")
    print("=" * 60)
    
    # Create enhanced task manager
    manager = EnhancedTaskManager("order_service")
    
    # Add tasks
    print("\n1. Adding tasks:")
    manager.add_task(2, "Process order #123", {"order_id": "123"}, "order_queue")
    manager.add_task(1, "Process payment", {"payment_id": "456"}, "payment_queue")
    manager.add_task(3, "Send notification", {"notification_id": "789"}, "notification_queue")
    
    # Display tasks
    manager.display_tasks()
    
    # Display queue edges
    manager.display_queue_edges()
    
    # Get statistics
    stats = manager.get_statistics()
    print(f"\n2. Statistics:")
    import json
    print(json.dumps(stats, indent=2))
    
    # Process tasks
    print(f"\n3. Processing tasks:")
    while True:
        task = manager.get_next_task()
        if not task:
            break
        print(f"Processed: {task.description}")
    
    # Export to JSON
    print(f"\n4. Exported JSON:")
    print(manager.export_to_json())
