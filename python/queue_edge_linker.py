"""
Queue Edge Linker Module
JIRA: BITO-12018 - Queue edges should be identified & linked through ai-architect (api flow)

This module provides functionality to link queue edges with API provider edges
and create the complete edge graph.
"""

from typing import List, Dict, Set, Optional, Tuple
from queue_edge_model import QueueEdge, QueueEdgeCollection
import uuid


class EdgeLinker:
    """
    Links queue edges with API provider edges to create the complete edge graph
    """
    
    def __init__(self):
        self.queue_edges: Dict[str, QueueEdge] = {}
        self.api_provider_edges: Dict[str, Dict] = {}
        self.edge_links: Dict[str, List[str]] = {}
    
    def register_queue_edge(self, edge: QueueEdge) -> None:
        """Register a queue edge"""
        self.queue_edges[edge.edge_id] = edge
    
    def register_api_provider_edge(self, edge_id: str, edge_data: Dict) -> None:
        """Register an API provider edge"""
        self.api_provider_edges[edge_id] = edge_data
    
    def link_queue_to_api_provider(
        self,
        queue_edge_id: str,
        api_provider_edge_id: str
    ) -> bool:
        """
        Link a queue edge to an API provider edge
        
        Args:
            queue_edge_id: ID of the queue edge
            api_provider_edge_id: ID of the API provider edge
        
        Returns:
            True if link was successful, False otherwise
        """
        if queue_edge_id not in self.queue_edges:
            return False
        
        queue_edge = self.queue_edges[queue_edge_id]
        
        # Add API provider edge link
        if api_provider_edge_id not in queue_edge.api_provider_edges:
            queue_edge.api_provider_edges.append(api_provider_edge_id)
        
        # Track the link
        if queue_edge_id not in self.edge_links:
            self.edge_links[queue_edge_id] = []
        self.edge_links[queue_edge_id].append(api_provider_edge_id)
        
        return True
    
    def link_queue_call(
        self,
        queue_edge_id: str,
        called_queue_edge_id: str
    ) -> bool:
        """
        Link a queue call (from one queue edge to another)
        
        Args:
            queue_edge_id: ID of the calling queue edge
            called_queue_edge_id: ID of the called queue edge
        
        Returns:
            True if link was successful, False otherwise
        """
        if queue_edge_id not in self.queue_edges:
            return False
        
        queue_edge = self.queue_edges[queue_edge_id]
        
        # Add queue call edge link
        if called_queue_edge_id not in queue_edge.queue_call_edges:
            queue_edge.queue_call_edges.append(called_queue_edge_id)
        
        return True
    
    def auto_link_edges(self, collection: QueueEdgeCollection) -> Dict[str, int]:
        """
        Automatically link edges based on service names and queue identifiers
        
        Args:
            collection: QueueEdgeCollection to link
        
        Returns:
            Dictionary with linking statistics
        """
        stats = {
            "total_edges": len(collection.edges),
            "linked_edges": 0,
            "links_created": 0
        }
        
        edges = collection.edges
        
        # Link edges by queue identifier
        queue_map: Dict[str, List[QueueEdge]] = {}
        for edge in edges:
            if edge.queue_identifier not in queue_map:
                queue_map[edge.queue_identifier] = []
            queue_map[edge.queue_identifier].append(edge)
        
        # Create links between producer and consumer
        for queue_edges in queue_map.values():
            producers = [e for e in queue_edges if e.operation_type == "produce"]
            consumers = [e for e in queue_edges if e.operation_type == "consume"]

            for producer in producers:
                for consumer in consumers:
                    if producer.source_identifier != consumer.source_identifier:
                        self.link_queue_call(producer.edge_id, consumer.edge_id)
                        stats["links_created"] += 1
                        stats["linked_edges"] += 1
        
        return stats
    
    def get_edge_graph(self) -> Dict:
        """
        Get the complete edge graph as a dictionary
        
        Returns:
            Dictionary representation of the edge graph
        """
        graph = {
            "nodes": [],
            "edges": []
        }
        
        # Add queue edges as nodes
        for edge_id, edge in self.queue_edges.items():
            graph["nodes"].append({
                "id": edge_id,
                "label": f"{edge.source_identifier}:{edge.queue_identifier}",
                "type": "queue",
                "operation": edge.operation_type,
                "pattern": edge.pattern
            })
        
        # Add API provider edges as nodes
        for edge_id, edge_data in self.api_provider_edges.items():
            graph["nodes"].append({
                "id": edge_id,
                "label": edge_data.get("name", edge_id),
                "type": "api_provider",
                **edge_data
            })
        
        # Add links as edges
        for queue_edge_id, linked_ids in self.edge_links.items():
            for linked_id in linked_ids:
                graph["edges"].append({
                    "source": queue_edge_id,
                    "target": linked_id,
                    "type": "api_link"
                })
        
        # Add queue call edges
        for edge_id, edge in self.queue_edges.items():
            for called_edge_id in edge.queue_call_edges:
                graph["edges"].append({
                    "source": edge_id,
                    "target": called_edge_id,
                    "type": "queue_call"
                })
        
        return graph
    
    def get_linked_edges_for_service(self, service_name: str) -> List[QueueEdge]:
        """
        Get all linked queue edges for a specific service
        
        Args:
            service_name: Name of the service
        
        Returns:
            List of QueueEdge objects for the service
        """
        return [
            edge for edge in self.queue_edges.values()
            if edge.source_identifier == service_name
        ]
    
    def get_edge_dependencies(self, edge_id: str) -> Dict[str, List[str]]:
        """
        Get all dependencies (incoming and outgoing) for an edge
        
        Args:
            edge_id: ID of the edge
        
        Returns:
            Dictionary with incoming and outgoing dependencies
        """
        dependencies = {
            "incoming": [],
            "outgoing": []
        }
        
        if edge_id not in self.queue_edges:
            return dependencies
        
        edge = self.queue_edges[edge_id]
        
        # Outgoing: API provider edges and queue call edges
        dependencies["outgoing"] = edge.api_provider_edges + edge.queue_call_edges
        
        # Incoming: Find edges that link to this edge
        for other_edge_id, other_edge in self.queue_edges.items():
            if edge_id in other_edge.queue_call_edges:
                dependencies["incoming"].append(other_edge_id)
        
        return dependencies
    
    def get_edge_path(self, start_edge_id: str, end_edge_id: str) -> Optional[List[str]]:
        """
        Find the shortest path between two edges
        
        Args:
            start_edge_id: ID of starting edge
            end_edge_id: ID of ending edge
        
        Returns:
            List of edge IDs representing the path, or None if no path exists
        """
        from collections import deque
        
        if start_edge_id not in self.queue_edges or end_edge_id not in self.queue_edges:
            return None
        
        visited = set()
        queue = deque([(start_edge_id, [start_edge_id])])
        
        while queue:
            current_id, path = queue.popleft()
            
            if current_id == end_edge_id:
                return path
            
            if current_id in visited:
                continue
            
            visited.add(current_id)
            
            if current_id in self.queue_edges:
                current_edge = self.queue_edges[current_id]
                
                for next_id in current_edge.queue_call_edges + current_edge.api_provider_edges:
                    if next_id not in visited:
                        queue.append((next_id, path + [next_id]))
        
        return None


class QueueEdgeIndexer:
    """
    Creates and manages an index of queue edges for fast querying
    """
    
    def __init__(self):
        self.index_by_service: Dict[str, List[QueueEdge]] = {}
        self.index_by_queue: Dict[str, List[QueueEdge]] = {}
        self.index_by_operation: Dict[str, List[QueueEdge]] = {}
        self.index_by_pattern: Dict[str, List[QueueEdge]] = {}
        self.all_edges: List[QueueEdge] = []
    
    def build_index(self, collection: QueueEdgeCollection) -> None:
        """Build index from a QueueEdgeCollection"""
        self.all_edges = collection.edges
        
        for edge in collection.edges:
            # Index by service
            if edge.source_identifier not in self.index_by_service:
                self.index_by_service[edge.source_identifier] = []
            self.index_by_service[edge.source_identifier].append(edge)
            
            # Index by queue
            if edge.queue_identifier not in self.index_by_queue:
                self.index_by_queue[edge.queue_identifier] = []
            self.index_by_queue[edge.queue_identifier].append(edge)
            
            # Index by operation
            if edge.operation_type not in self.index_by_operation:
                self.index_by_operation[edge.operation_type] = []
            self.index_by_operation[edge.operation_type].append(edge)
            
            # Index by pattern
            if edge.pattern not in self.index_by_pattern:
                self.index_by_pattern[edge.pattern] = []
            self.index_by_pattern[edge.pattern].append(edge)
    
    def query_by_service(self, service_name: str) -> List[QueueEdge]:
        """Query edges by service name"""
        return self.index_by_service.get(service_name, [])
    
    def query_by_queue(self, queue_identifier: str) -> List[QueueEdge]:
        """Query edges by queue identifier"""
        return self.index_by_queue.get(queue_identifier, [])
    
    def query_by_operation(self, operation_type: str) -> List[QueueEdge]:
        """Query edges by operation type"""
        return self.index_by_operation.get(operation_type, [])
    
    def query_by_pattern(self, pattern: str) -> List[QueueEdge]:
        """Query edges by pattern"""
        return self.index_by_pattern.get(pattern, [])
    
    def get_statistics(self) -> Dict:
        """Get index statistics"""
        return {
            "total_edges": len(self.all_edges),
            "services": len(self.index_by_service),
            "queues": len(self.index_by_queue),
            "operation_types": len(self.index_by_operation),
            "patterns": len(self.index_by_pattern),
            "index_by_service": {k: len(v) for k, v in self.index_by_service.items()},
            "index_by_queue": {k: len(v) for k, v in self.index_by_queue.items()},
            "index_by_operation": {k: len(v) for k, v in self.index_by_operation.items()},
            "index_by_pattern": {k: len(v) for k, v in self.index_by_pattern.items()},
        }


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("Queue Edge Linker - Example Usage")
    print("=" * 60)
    
    from queue_edge_model import create_queue_edge
    
    # Create linker
    linker = EdgeLinker()
    
    # Create sample edges
    edge1 = create_queue_edge(
        edge_id="edge_001",
        source_identifier="order_service",
        queue_identifier="order_queue",
        operation_type="produce"
    )
    
    edge2 = create_queue_edge(
        edge_id="edge_002",
        source_identifier="payment_service",
        queue_identifier="order_queue",
        operation_type="consume"
    )
    
    # Register edges
    linker.register_queue_edge(edge1)
    linker.register_queue_edge(edge2)
    
    # Link edges
    linker.link_queue_call("edge_001", "edge_002")
    
    # Get graph
    graph = linker.get_edge_graph()
    print("\nEdge Graph:")
    import json
    print(json.dumps(graph, indent=2))
    
    # Get dependencies
    deps = linker.get_edge_dependencies("edge_001")
    print(f"\nDependencies for edge_001: {deps}")
