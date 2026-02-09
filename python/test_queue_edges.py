"""
Queue Edge Implementation - Test Suite
JIRA: BITO-12018 - Queue edges should be identified & linked through ai-architect (api flow)

Comprehensive test suite for queue edge functionality
"""

import unittest
import json
from queue_edge_model import (
    QueueEdge, QueueEdgeCollection, QueueEdgeRequest, QueueEdgeResponse,
    QueueOperationType, QueuePattern, create_queue_edge, QueueEdgeSchema
)
from queue_edge_detector import QueueEdgeDetector
from queue_edge_linker import EdgeLinker, QueueEdgeIndexer
from enhanced_queue_manager import EnhancedTaskManager


class TestQueueEdgeModel(unittest.TestCase):
    """Test QueueEdge data model"""
    
    def test_create_queue_edge(self):
        """Test creating a queue edge"""
        edge = create_queue_edge(
            edge_id="test_001",
            source_identifier="service_a",
            queue_identifier="test_queue",
            operation_type="produce"
        )
        
        self.assertEqual(edge.edge_id, "test_001")
        self.assertEqual(edge.source_identifier, "service_a")
        self.assertEqual(edge.queue_identifier, "test_queue")
        self.assertEqual(edge.operation_type, "produce")
    
    def test_queue_edge_to_dict(self):
        """Test converting queue edge to dictionary"""
        edge = create_queue_edge(
            edge_id="test_002",
            source_identifier="service_b",
            queue_identifier="test_queue",
            operation_type="consume"
        )
        
        edge_dict = edge.to_dict()
        
        self.assertIn("edge_id", edge_dict)
        self.assertIn("source_identifier", edge_dict)
        self.assertEqual(edge_dict["operation_type"], "consume")
    
    def test_queue_edge_to_json(self):
        """Test converting queue edge to JSON"""
        edge = create_queue_edge(
            edge_id="test_003",
            source_identifier="service_c",
            queue_identifier="test_queue",
            operation_type="produce"
        )
        
        json_str = edge.to_json()
        parsed = json.loads(json_str)
        
        self.assertEqual(parsed["edge_id"], "test_003")
    
    def test_queue_edge_with_request_response(self):
        """Test queue edge with request and response"""
        request = QueueEdgeRequest(
            operation="produce",
            message_type="TestMessage",
            schema={"id": "string"}
        )
        response = QueueEdgeResponse(
            status="success",
            processing_time_ms=100
        )
        
        edge = create_queue_edge(
            edge_id="test_004",
            source_identifier="service_d",
            queue_identifier="test_queue",
            operation_type="produce",
            request=request,
            response=response
        )
        
        self.assertIsNotNone(edge.request)
        self.assertIsNotNone(edge.response)
        self.assertEqual(edge.response.status, "success")
    
    def test_queue_edge_collection(self):
        """Test queue edge collection"""
        collection = QueueEdgeCollection(service_name="test_service")
        
        edge1 = create_queue_edge(
            edge_id="edge_1",
            source_identifier="test_service",
            queue_identifier="queue_a",
            operation_type="produce"
        )
        
        edge2 = create_queue_edge(
            edge_id="edge_2",
            source_identifier="test_service",
            queue_identifier="queue_a",
            operation_type="consume"
        )
        
        collection.add_edge(edge1)
        collection.add_edge(edge2)
        
        self.assertEqual(len(collection.edges), 2)
        
        # Test filtering
        produce_edges = collection.get_edges_by_operation("produce")
        self.assertEqual(len(produce_edges), 1)
        
        queue_edges = collection.get_edges_by_queue("queue_a")
        self.assertEqual(len(queue_edges), 2)
    
    def test_queue_edge_schema_validation(self):
        """Test queue edge schema validation"""
        valid_edge = {
            "edge_id": "test_001",
            "source_identifier": "service_a",
            "queue_identifier": "test_queue",
            "operation_type": "produce"
        }
        
        self.assertTrue(QueueEdgeSchema.validate_edge(valid_edge))
        
        # Missing required field
        invalid_edge = {
            "edge_id": "test_001",
            "source_identifier": "service_a"
        }
        
        self.assertFalse(QueueEdgeSchema.validate_edge(invalid_edge))


class TestQueueEdgeLinker(unittest.TestCase):
    """Test queue edge linking functionality"""
    
    def test_register_and_link_edges(self):
        """Test registering and linking edges"""
        linker = EdgeLinker()
        
        edge1 = create_queue_edge(
            edge_id="edge_1",
            source_identifier="service_a",
            queue_identifier="queue_1",
            operation_type="produce"
        )
        
        edge2 = create_queue_edge(
            edge_id="edge_2",
            source_identifier="service_b",
            queue_identifier="queue_1",
            operation_type="consume"
        )
        
        linker.register_queue_edge(edge1)
        linker.register_queue_edge(edge2)
        
        # Link edges
        result = linker.link_queue_call("edge_1", "edge_2")
        self.assertTrue(result)
        
        # Verify link
        self.assertIn("edge_2", edge1.queue_call_edges)
    
    def test_edge_graph(self):
        """Test edge graph generation"""
        linker = EdgeLinker()
        
        edge1 = create_queue_edge(
            edge_id="edge_1",
            source_identifier="service_a",
            queue_identifier="queue_1",
            operation_type="produce"
        )
        
        edge2 = create_queue_edge(
            edge_id="edge_2",
            source_identifier="service_b",
            queue_identifier="queue_1",
            operation_type="consume"
        )
        
        linker.register_queue_edge(edge1)
        linker.register_queue_edge(edge2)
        linker.link_queue_call("edge_1", "edge_2")
        
        graph = linker.get_edge_graph()
        
        self.assertIn("nodes", graph)
        self.assertIn("edges", graph)
        self.assertGreater(len(graph["nodes"]), 0)
    
    def test_edge_dependencies(self):
        """Test getting edge dependencies"""
        linker = EdgeLinker()
        
        edge1 = create_queue_edge(
            edge_id="edge_1",
            source_identifier="service_a",
            queue_identifier="queue_1",
            operation_type="produce"
        )
        
        edge2 = create_queue_edge(
            edge_id="edge_2",
            source_identifier="service_b",
            queue_identifier="queue_1",
            operation_type="consume"
        )
        
        linker.register_queue_edge(edge1)
        linker.register_queue_edge(edge2)
        linker.link_queue_call("edge_1", "edge_2")
        
        deps = linker.get_edge_dependencies("edge_1")
        
        self.assertIn("edge_2", deps["outgoing"])


class TestQueueEdgeIndexer(unittest.TestCase):
    """Test queue edge indexing functionality"""
    
    def test_build_index(self):
        """Test building an index"""
        collection = QueueEdgeCollection(service_name="test_service")
        
        edge1 = create_queue_edge(
            edge_id="edge_1",
            source_identifier="service_a",
            queue_identifier="queue_1",
            operation_type="produce"
        )
        
        edge2 = create_queue_edge(
            edge_id="edge_2",
            source_identifier="service_b",
            queue_identifier="queue_1",
            operation_type="consume"
        )
        
        collection.add_edge(edge1)
        collection.add_edge(edge2)
        
        indexer = QueueEdgeIndexer()
        indexer.build_index(collection)
        
        # Query by service
        service_a_edges = indexer.query_by_service("service_a")
        self.assertEqual(len(service_a_edges), 1)
        
        # Query by queue
        queue_1_edges = indexer.query_by_queue("queue_1")
        self.assertEqual(len(queue_1_edges), 2)
        
        # Query by operation
        produce_edges = indexer.query_by_operation("produce")
        self.assertEqual(len(produce_edges), 1)
    
    def test_index_statistics(self):
        """Test getting index statistics"""
        collection = QueueEdgeCollection(service_name="test_service")
        
        edge1 = create_queue_edge(
            edge_id="edge_1",
            source_identifier="service_a",
            queue_identifier="queue_1",
            operation_type="produce"
        )
        
        collection.add_edge(edge1)
        
        indexer = QueueEdgeIndexer()
        indexer.build_index(collection)
        
        stats = indexer.get_statistics()
        
        self.assertEqual(stats["total_edges"], 1)
        self.assertGreater(stats["services"], 0)


class TestEnhancedQueueManager(unittest.TestCase):
    """Test enhanced queue manager"""
    
    def test_add_and_process_tasks(self):
        """Test adding and processing tasks"""
        manager = EnhancedTaskManager("test_service")
        
        # Add tasks
        manager.add_task(2, "Task 1", queue_name="queue_1")
        manager.add_task(1, "Task 2", queue_name="queue_1")
        
        # Get tasks
        task1 = manager.get_next_task()
        self.assertIsNotNone(task1)
        self.assertEqual(task1.priority, 1)
        
        task2 = manager.get_next_task()
        self.assertIsNotNone(task2)
        self.assertEqual(task2.priority, 2)
    
    def test_queue_edge_tracking(self):
        """Test queue edge tracking"""
        manager = EnhancedTaskManager("test_service")
        
        manager.add_task(1, "Task 1", queue_name="queue_1")
        manager.add_task(2, "Task 2", queue_name="queue_2")
        
        self.assertEqual(len(manager.queue_edges), 2)
    
    def test_edge_collection(self):
        """Test getting edge collection"""
        manager = EnhancedTaskManager("test_service")
        
        manager.add_task(1, "Task 1", queue_name="queue_1")
        manager.add_task(2, "Task 2", queue_name="queue_1")
        
        collection = manager.get_edge_collection()
        
        self.assertEqual(collection.service_name, "test_service")
        self.assertEqual(len(collection.edges), 2)
    
    def test_statistics(self):
        """Test getting statistics"""
        manager = EnhancedTaskManager("test_service")
        
        manager.add_task(1, "Task 1", queue_name="queue_1")
        manager.add_task(2, "Task 2", queue_name="queue_1")
        manager.get_next_task()
        
        stats = manager.get_statistics()
        
        self.assertEqual(stats["service_name"], "test_service")
        self.assertEqual(stats["pending_tasks"], 1)
        self.assertEqual(stats["processed_tasks"], 1)
        self.assertEqual(stats["total_tasks"], 2)


def run_tests():
    """Run all tests"""
    unittest.main(argv=[''], exit=False, verbosity=2)


if __name__ == "__main__":
    print("=" * 60)
    print("Queue Edge Implementation - Test Suite")
    print("=" * 60)
    print()
    
    run_tests()
