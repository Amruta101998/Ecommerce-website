"""
Queue Edge Detection Module
JIRA: BITO-12018 - Queue edges should be identified & linked through ai-architect (api flow)

This module provides functionality to detect queue operations in source code
and create corresponding QueueEdge objects.
"""

import re
import ast
from typing import List, Dict, Set, Optional, Tuple, Any
from pathlib import Path
from queue_edge_model import QueueEdge, QueueEdgeCollection, QueueOperationType, QueuePattern
import uuid


class QueueOperationPattern:
    """
    Patterns for detecting queue operations in code
    Supports multiple queue systems: RabbitMQ, Kafka, AWS SQS, etc.
    """
    
    # RabbitMQ patterns
    RABBITMQ_PUBLISH = [
        r'channel\.basic_publish',
        r'\.publish\(',
        r'pika\.BasicProperties',
        r'channel\.queue_declare',
    ]
    
    RABBITMQ_CONSUME = [
        r'channel\.basic_consume',
        r'\.callback',
        r'pika\.adapters',
        r'start_consuming',
    ]
    
    # Kafka patterns
    KAFKA_PRODUCE = [
        r'KafkaProducer',
        r'\.send\(',
        r'producer\.send',
        r'kafka\.KafkaProducer',
    ]
    
    KAFKA_CONSUME = [
        r'KafkaConsumer',
        r'consumer\.poll',
        r'kafka\.KafkaConsumer',
        r'for.*in.*consumer',
    ]
    
    # AWS SQS patterns
    SQS_SEND = [
        r'send_message',
        r'\.send_message\(',
        r'sqs\.send_message',
        r'SendMessage',
    ]
    
    SQS_RECEIVE = [
        r'receive_message',
        r'\.receive_message\(',
        r'sqs\.receive_message',
        r'ReceiveMessage',
    ]
    
    # Generic queue patterns
    GENERIC_PRODUCE = [
        r'queue\.put\(',
        r'\.enqueue\(',
        r'\.push\(',
        r'\.add\(',
    ]
    
    GENERIC_CONSUME = [
        r'queue\.get\(',
        r'\.dequeue\(',
        r'\.pop\(',
        r'\.poll\(',
    ]


class QueueEdgeDetector:
    """
    Detects queue operations in source code files
    """
    
    def __init__(self):
        self.detected_edges: List[QueueEdge] = []
        self.patterns = QueueOperationPattern()
    
    def detect_in_file(self, file_path: str, service_name: str) -> List[QueueEdge]:
        """
        Detect queue operations in a single file
        
        Args:
            file_path: Path to source code file
            service_name: Name of the service/module
        
        Returns:
            List of detected QueueEdge objects
        """
        edges = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Detect different queue systems
            edges.extend(self._detect_rabbitmq(content, service_name, file_path))
            edges.extend(self._detect_kafka(content, service_name, file_path))
            edges.extend(self._detect_sqs(content, service_name, file_path))
            edges.extend(self._detect_generic_queues(content, service_name, file_path))
            
        except (IOError, OSError, UnicodeDecodeError) as e:
            print(f"Error processing file {file_path}: {str(e)}")
        
        return edges
    
    def detect_in_directory(self, directory_path: str, service_name: str) -> QueueEdgeCollection:
        """
        Detect queue operations in all Python files in a directory
        
        Args:
            directory_path: Path to directory
            service_name: Name of the service/module
        
        Returns:
            QueueEdgeCollection with all detected edges
        """
        collection = QueueEdgeCollection(service_name=service_name)
        
        path = Path(directory_path)
        for py_file in path.rglob("*.py"):
            edges = self.detect_in_file(str(py_file), service_name)
            for edge in edges:
                collection.add_edge(edge)
        
        return collection
    
    def _detect_rabbitmq(self, content: str, service_name: str, file_path: str) -> List[QueueEdge]:
        """Detect RabbitMQ operations"""
        edges = []
        
        # Detect publish operations
        for pattern in self.patterns.RABBITMQ_PUBLISH:
            matches = re.finditer(pattern, content)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                queue_name = self._extract_queue_name(content, match.start())
                
                edge = QueueEdge(
                    edge_id=str(uuid.uuid4()),
                    source_identifier=service_name,
                    queue_identifier=queue_name or "rabbitmq_queue",
                    operation_type=QueueOperationType.PRODUCE.value,
                    pattern=QueuePattern.MESSAGE_QUEUE.value,
                    description=f"RabbitMQ publish operation in {Path(file_path).name}:{line_num}",
                    tags=["rabbitmq", "produce", "message_queue"],
                    metadata={
                        "file": file_path,
                        "line": line_num,
                        "system": "RabbitMQ",
                        "match": match.group()
                    }
                )
                edges.append(edge)
        
        # Detect consume operations
        for pattern in self.patterns.RABBITMQ_CONSUME:
            matches = re.finditer(pattern, content)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                queue_name = self._extract_queue_name(content, match.start())
                
                edge = QueueEdge(
                    edge_id=str(uuid.uuid4()),
                    source_identifier=service_name,
                    queue_identifier=queue_name or "rabbitmq_queue",
                    operation_type=QueueOperationType.CONSUME.value,
                    pattern=QueuePattern.MESSAGE_QUEUE.value,
                    description=f"RabbitMQ consume operation in {Path(file_path).name}:{line_num}",
                    tags=["rabbitmq", "consume", "message_queue"],
                    metadata={
                        "file": file_path,
                        "line": line_num,
                        "system": "RabbitMQ",
                        "match": match.group()
                    }
                )
                edges.append(edge)
        
        return edges
    
    def _detect_kafka(self, content: str, service_name: str, file_path: str) -> List[QueueEdge]:
        """Detect Kafka operations"""
        edges = []
        
        # Detect producer operations
        for pattern in self.patterns.KAFKA_PRODUCE:
            matches = re.finditer(pattern, content)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                topic_name = self._extract_kafka_topic(content, match.start())
                
                edge = QueueEdge(
                    edge_id=str(uuid.uuid4()),
                    source_identifier=service_name,
                    queue_identifier=topic_name or "kafka_topic",
                    operation_type=QueueOperationType.PRODUCE.value,
                    pattern=QueuePattern.TOPIC.value,
                    description=f"Kafka produce operation in {Path(file_path).name}:{line_num}",
                    tags=["kafka", "produce", "topic"],
                    metadata={
                        "file": file_path,
                        "line": line_num,
                        "system": "Kafka",
                        "match": match.group()
                    }
                )
                edges.append(edge)
        
        # Detect consumer operations
        for pattern in self.patterns.KAFKA_CONSUME:
            matches = re.finditer(pattern, content)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                topic_name = self._extract_kafka_topic(content, match.start())
                
                edge = QueueEdge(
                    edge_id=str(uuid.uuid4()),
                    source_identifier=service_name,
                    queue_identifier=topic_name or "kafka_topic",
                    operation_type=QueueOperationType.CONSUME.value,
                    pattern=QueuePattern.TOPIC.value,
                    description=f"Kafka consume operation in {Path(file_path).name}:{line_num}",
                    tags=["kafka", "consume", "topic"],
                    metadata={
                        "file": file_path,
                        "line": line_num,
                        "system": "Kafka",
                        "match": match.group()
                    }
                )
                edges.append(edge)
        
        return edges
    
    def _detect_sqs(self, content: str, service_name: str, file_path: str) -> List[QueueEdge]:
        """Detect AWS SQS operations"""
        edges = []
        
        # Detect send operations
        for pattern in self.patterns.SQS_SEND:
            matches = re.finditer(pattern, content)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                queue_url = self._extract_sqs_queue_url(content, match.start())
                
                edge = QueueEdge(
                    edge_id=str(uuid.uuid4()),
                    source_identifier=service_name,
                    queue_identifier=queue_url or "sqs_queue",
                    operation_type=QueueOperationType.SEND.value,
                    pattern=QueuePattern.QUEUE.value,
                    description=f"AWS SQS send operation in {Path(file_path).name}:{line_num}",
                    tags=["aws_sqs", "send", "queue"],
                    metadata={
                        "file": file_path,
                        "line": line_num,
                        "system": "AWS SQS",
                        "match": match.group()
                    }
                )
                edges.append(edge)
        
        # Detect receive operations
        for pattern in self.patterns.SQS_RECEIVE:
            matches = re.finditer(pattern, content)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                queue_url = self._extract_sqs_queue_url(content, match.start())
                
                edge = QueueEdge(
                    edge_id=str(uuid.uuid4()),
                    source_identifier=service_name,
                    queue_identifier=queue_url or "sqs_queue",
                    operation_type=QueueOperationType.RECEIVE.value,
                    pattern=QueuePattern.QUEUE.value,
                    description=f"AWS SQS receive operation in {Path(file_path).name}:{line_num}",
                    tags=["aws_sqs", "receive", "queue"],
                    metadata={
                        "file": file_path,
                        "line": line_num,
                        "system": "AWS SQS",
                        "match": match.group()
                    }
                )
                edges.append(edge)
        
        return edges
    
    def _detect_generic_queues(self, content: str, service_name: str, file_path: str) -> List[QueueEdge]:
        """Detect generic queue operations"""
        edges = []
        
        # Detect produce operations
        for pattern in self.patterns.GENERIC_PRODUCE:
            matches = re.finditer(pattern, content)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                
                edge = QueueEdge(
                    edge_id=str(uuid.uuid4()),
                    source_identifier=service_name,
                    queue_identifier="generic_queue",
                    operation_type=QueueOperationType.PRODUCE.value,
                    pattern=QueuePattern.QUEUE.value,
                    description=f"Generic queue produce operation in {Path(file_path).name}:{line_num}",
                    tags=["generic", "produce"],
                    metadata={
                        "file": file_path,
                        "line": line_num,
                        "system": "Generic",
                        "match": match.group()
                    }
                )
                edges.append(edge)
        
        # Detect consume operations
        for pattern in self.patterns.GENERIC_CONSUME:
            matches = re.finditer(pattern, content)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                
                edge = QueueEdge(
                    edge_id=str(uuid.uuid4()),
                    source_identifier=service_name,
                    queue_identifier="generic_queue",
                    operation_type=QueueOperationType.CONSUME.value,
                    pattern=QueuePattern.QUEUE.value,
                    description=f"Generic queue consume operation in {Path(file_path).name}:{line_num}",
                    tags=["generic", "consume"],
                    metadata={
                        "file": file_path,
                        "line": line_num,
                        "system": "Generic",
                        "match": match.group()
                    }
                )
                edges.append(edge)
        
        return edges
    
    @staticmethod
    def _extract_queue_name(content: str, position: int, context_length: int = 100) -> Optional[str]:
        """Extract queue name from context around match"""
        start = max(0, position - context_length)
        end = min(len(content), position + context_length)
        context = content[start:end]
        
        # Try to find queue name in quotes
        match = re.search(r'["\']([a-zA-Z0-9_\-\.]+)["\']', context)
        if match:
            return match.group(1)
        return None
    
    @staticmethod
    def _extract_kafka_topic(content: str, position: int, context_length: int = 100) -> Optional[str]:
        """Extract Kafka topic name from context"""
        start = max(0, position - context_length)
        end = min(len(content), position + context_length)
        context = content[start:end]
        
        # Try to find topic in quotes or as parameter
        match = re.search(r'topics?[=\s]*["\']([a-zA-Z0-9_\-\.]+)["\']', context)
        if match:
            return match.group(1)
        return None
    
    @staticmethod
    def _extract_sqs_queue_url(content: str, position: int, context_length: int = 150) -> Optional[str]:
        """Extract SQS queue URL from context"""
        start = max(0, position - context_length)
        end = min(len(content), position + context_length)
        context = content[start:end]
        
        # Try to find queue URL
        match = re.search(r'https?://[^\s"\']+sqs[^\s"\']+', context)
        if match:
            return match.group(0)
        return None


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("Queue Edge Detection - Example Usage")
    print("=" * 60)
    
    detector = QueueEdgeDetector()
    
    # Example: Detect in current directory
    collection = detector.detect_in_directory(".", "example_service")
    
    print(f"\nDetected {len(collection.edges)} queue edges")
    print(collection.to_json())
