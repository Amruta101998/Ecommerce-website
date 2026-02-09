"""
Queue Edge API Integration Module
JIRA: BITO-12018 - Queue edges should be identified & linked through ai-architect (api flow)

This module provides integration with the ai-architect API for syncing queue edges.
"""

import json
import requests
from typing import Dict, List, Optional, Any
from queue_edge_model import QueueEdge, QueueEdgeCollection
from queue_edge_linker import EdgeLinker, QueueEdgeIndexer
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QueueEdgeAPIClient:
    """
    Client for communicating with the ai-architect API
    """
    
    def __init__(self, api_base_url: str, api_key: Optional[str] = None):
        """
        Initialize API client
        
        Args:
            api_base_url: Base URL of the ai-architect API
            api_key: Optional API key for authentication
        """
        self.api_base_url = api_base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {api_key}"
            })
        
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "QueueEdgeAPIClient/1.0"
        })
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Make HTTP request to API
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            data: Request body data
            params: Query parameters
        
        Returns:
            Response JSON as dictionary
        """
        url = f"{self.api_base_url}{endpoint}"
        
        try:
            if method == "GET":
                response = self.session.get(url, params=params, timeout=30)
            elif method == "POST":
                response = self.session.post(url, json=data, params=params, timeout=30)
            elif method == "PUT":
                response = self.session.put(url, json=data, params=params, timeout=30)
            elif method == "DELETE":
                response = self.session.delete(url, params=params, timeout=30)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            raise
    
    def create_queue_edge(self, edge: QueueEdge) -> Dict[str, Any]:
        """
        Create a queue edge via API
        
        Args:
            edge: QueueEdge object to create
        
        Returns:
            API response
        """
        logger.info(f"Creating queue edge: {edge.edge_id}")
        return self._make_request(
            "POST",
            "/api/v1/queue-edges",
            data=edge.to_dict()
        )
    
    def get_queue_edge(self, edge_id: str) -> Dict[str, Any]:
        """
        Get a queue edge via API
        
        Args:
            edge_id: ID of the queue edge
        
        Returns:
            Queue edge data
        """
        logger.info(f"Fetching queue edge: {edge_id}")
        return self._make_request(
            "GET",
            f"/api/v1/queue-edges/{edge_id}"
        )
    
    def update_queue_edge(self, edge_id: str, edge_data: Dict) -> Dict[str, Any]:
        """
        Update a queue edge via API
        
        Args:
            edge_id: ID of the queue edge
            edge_data: Updated edge data
        
        Returns:
            API response
        """
        logger.info(f"Updating queue edge: {edge_id}")
        return self._make_request(
            "PUT",
            f"/api/v1/queue-edges/{edge_id}",
            data=edge_data
        )
    
    def delete_queue_edge(self, edge_id: str) -> Dict[str, Any]:
        """
        Delete a queue edge via API
        
        Args:
            edge_id: ID of the queue edge
        
        Returns:
            API response
        """
        logger.info(f"Deleting queue edge: {edge_id}")
        return self._make_request(
            "DELETE",
            f"/api/v1/queue-edges/{edge_id}"
        )
    
    def bulk_create_queue_edges(self, edges: List[QueueEdge]) -> Dict[str, Any]:
        """
        Create multiple queue edges via API
        
        Args:
            edges: List of QueueEdge objects
        
        Returns:
            API response
        """
        logger.info(f"Creating {len(edges)} queue edges in bulk")
        return self._make_request(
            "POST",
            "/api/v1/queue-edges/bulk",
            data={"edges": [edge.to_dict() for edge in edges]}
        )
    
    def link_queue_edges(
        self,
        source_edge_id: str,
        target_edge_id: str,
        link_type: str = "queue_call"
    ) -> Dict[str, Any]:
        """
        Link two queue edges via API
        
        Args:
            source_edge_id: ID of source edge
            target_edge_id: ID of target edge
            link_type: Type of link (queue_call, api_provider, etc.)
        
        Returns:
            API response
        """
        logger.info(f"Linking edges: {source_edge_id} -> {target_edge_id}")
        return self._make_request(
            "POST",
            "/api/v1/queue-edges/links",
            data={
                "source_id": source_edge_id,
                "target_id": target_edge_id,
                "link_type": link_type
            }
        )
    
    def query_queue_edges(
        self,
        service_name: Optional[str] = None,
        queue_identifier: Optional[str] = None,
        operation_type: Optional[str] = None,
        pattern: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Query queue edges via API
        
        Args:
            service_name: Filter by service name
            queue_identifier: Filter by queue identifier
            operation_type: Filter by operation type
            pattern: Filter by pattern
        
        Returns:
            Query results
        """
        params = {}
        if service_name:
            params["service_name"] = service_name
        if queue_identifier:
            params["queue_identifier"] = queue_identifier
        if operation_type:
            params["operation_type"] = operation_type
        if pattern:
            params["pattern"] = pattern
        
        logger.info(f"Querying queue edges with params: {params}")
        return self._make_request(
            "GET",
            "/api/v1/queue-edges",
            params=params
        )
    
    def get_edge_graph(self) -> Dict[str, Any]:
        """
        Get the complete edge graph via API
        
        Returns:
            Edge graph data
        """
        logger.info("Fetching edge graph")
        return self._make_request(
            "GET",
            "/api/v1/queue-edges/graph"
        )
    
    def sync_collection(self, collection: QueueEdgeCollection) -> Dict[str, Any]:
        """
        Sync an entire QueueEdgeCollection via API
        
        Args:
            collection: QueueEdgeCollection to sync
        
        Returns:
            Sync results
        """
        logger.info(f"Syncing collection: {collection.service_name}")
        return self._make_request(
            "POST",
            "/api/v1/queue-edges/sync",
            data=collection.to_dict()
        )


class QueueEdgeIndexSync:
    """
    Synchronizes queue edge index with API
    """
    
    def __init__(self, api_client: QueueEdgeAPIClient):
        """
        Initialize sync manager
        
        Args:
            api_client: QueueEdgeAPIClient instance
        """
        self.api_client = api_client
        self.indexer = QueueEdgeIndexer()
        self.local_index: Dict[str, QueueEdge] = {}
    
    def sync_from_api(self) -> Dict[str, Any]:
        """
        Fetch queue edges from API and update local index
        
        Returns:
            Sync statistics
        """
        logger.info("Syncing from API")
        
        try:
            response = self.api_client.get_edge_graph()
            
            stats = {
                "synced": True,
                "edges_fetched": 0,
                "edges_indexed": 0,
                "errors": []
            }
            
            if "nodes" in response:
                for node in response["nodes"]:
                    if node.get("type") == "queue":
                        stats["edges_fetched"] += 1
            
            return stats
        
        except Exception as e:
            logger.error(f"Sync from API failed: {str(e)}")
            return {
                "synced": False,
                "error": str(e)
            }
    
    def sync_to_api(self, collection: QueueEdgeCollection) -> Dict[str, Any]:
        """
        Push queue edges to API
        
        Args:
            collection: QueueEdgeCollection to push
        
        Returns:
            Sync statistics
        """
        logger.info(f"Syncing to API: {collection.service_name}")
        
        try:
            response = self.api_client.sync_collection(collection)
            
            stats = {
                "synced": True,
                "edges_pushed": len(collection.edges),
                "response": response
            }
            
            return stats
        
        except Exception as e:
            logger.error(f"Sync to API failed: {str(e)}")
            return {
                "synced": False,
                "error": str(e)
            }


class QueueEdgeIntegrationManager:
    """
    Manages the complete integration workflow for queue edges
    """
    
    def __init__(self, api_base_url: str, api_key: Optional[str] = None):
        """
        Initialize integration manager
        
        Args:
            api_base_url: Base URL of the ai-architect API
            api_key: Optional API key
        """
        self.api_client = QueueEdgeAPIClient(api_base_url, api_key)
        self.linker = EdgeLinker()
        self.indexer = QueueEdgeIndexer()
        self.sync = QueueEdgeIndexSync(self.api_client)
    
    def process_and_sync(
        self,
        collection: QueueEdgeCollection
    ) -> Dict[str, Any]:
        """
        Process a queue edge collection and sync with API
        
        Args:
            collection: QueueEdgeCollection to process
        
        Returns:
            Processing and sync results
        """
        logger.info(f"Processing and syncing: {collection.service_name}")
        
        results = {
            "service_name": collection.service_name,
            "total_edges": len(collection.edges),
            "linking_stats": {},
            "sync_stats": {},
            "errors": []
        }
        
        try:
            # Register edges with linker
            for edge in collection.edges:
                self.linker.register_queue_edge(edge)
            
            # Auto-link edges
            results["linking_stats"] = self.linker.auto_link_edges(collection)
            
            # Build index
            self.indexer.build_index(collection)
            
            # Sync to API
            results["sync_stats"] = self.sync.sync_to_api(collection)
            
        except Exception as e:
            logger.error(f"Processing failed: {str(e)}")
            results["errors"].append(str(e))
        
        return results
    
    def get_integration_status(self) -> Dict[str, Any]:
        """
        Get current integration status
        
        Returns:
            Status information
        """
        return {
            "queue_edges_registered": len(self.linker.queue_edges),
            "api_provider_edges_registered": len(self.linker.api_provider_edges),
            "index_stats": self.indexer.get_statistics()
        }


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("Queue Edge API Integration - Example Usage")
    print("=" * 60)
    
    # Initialize API client
    api_client = QueueEdgeAPIClient(
        api_base_url="http://localhost:8080",
        api_key="your-api-key"
    )
    
    print("\nAPI Client initialized")
    print(f"Base URL: {api_client.api_base_url}")
    
    # Note: Actual API calls would require a running server
    print("\nTo test with a real API:")
    print("1. Set up the ai-architect API server")
    print("2. Update the api_base_url and api_key")
    print("3. Call api_client methods to interact with the API")
