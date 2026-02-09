# Queue Edge Implementation - Complete Guide
## JIRA: BITO-12018 - Queue edges should be identified & linked through ai-architect (api flow)

## 📋 Overview

This implementation provides a complete solution for identifying, tracking, and linking queue edges through the ai-architect API flow. The system detects queue operations in source code, creates edge models, links them through the system, and syncs with the API.

## 🏗️ Architecture

### Components

1. **Queue Edge Model** (`queue_edge_model.py`)
   - Core data structures for queue edges
   - Request/Response payloads
   - Schema validation
   - Collection management

2. **Queue Edge Detector** (`queue_edge_detector.py`)
   - Detects queue operations in source code
   - Supports RabbitMQ, Kafka, AWS SQS, and generic queues
   - Pattern-based detection
   - File and directory scanning

3. **Queue Edge Linker** (`queue_edge_linker.py`)
   - Links queue edges together
   - Creates edge graphs
   - Manages dependencies
   - Finds edge paths

4. **Queue Edge API** (`queue_edge_api.py`)
   - API client for ai-architect integration
   - CRUD operations for queue edges
   - Bulk operations
   - Index synchronization

5. **Enhanced Queue Manager** (`enhanced_queue_manager.py`)
   - Task management with edge tracking
   - Callback system
   - Statistics and reporting
   - JSON export

## 📁 File Structure

```
python/
├── queue_edge_model.py          # Core data models
├── queue_edge_detector.py       # Detection logic
├── queue_edge_linker.py         # Edge linking
├── queue_edge_api.py            # API integration
├── enhanced_queue_manager.py    # Enhanced task manager
├── test_queue_edges.py          # Test suite
└── README_QUEUE_EDGES.md        # This file
```

## 🚀 Quick Start

### 1. Basic Queue Edge Creation

```python
from queue_edge_model import create_queue_edge

# Create a queue edge
edge = create_queue_edge(
    edge_id="queue_edge_001",
    source_identifier="order_service",
    queue_identifier="order_queue",
    operation_type="produce",
    description="Order service produces messages"
)

# Convert to JSON
print(edge.to_json())
```

### 2. Detect Queue Operations

```python
from queue_edge_detector import QueueEdgeDetector

detector = QueueEdgeDetector()

# Detect in a directory
collection = detector.detect_in_directory(
    "/path/to/code",
    "my_service"
)

print(f"Found {len(collection.edges)} queue edges")
```

### 3. Link Queue Edges

```python
from queue_edge_linker import EdgeLinker

linker = EdgeLinker()

# Register edges
linker.register_queue_edge(edge1)
linker.register_queue_edge(edge2)

# Link them
linker.link_queue_call("edge_1", "edge_2")

# Get graph
graph = linker.get_edge_graph()
```

### 4. API Integration

```python
from queue_edge_api import QueueEdgeIntegrationManager

manager = QueueEdgeIntegrationManager(
    api_base_url="http://localhost:8080",
    api_key="your-api-key"
)

# Process and sync
results = manager.process_and_sync(collection)
```

### 5. Enhanced Task Manager

```python
from enhanced_queue_manager import EnhancedTaskManager

manager = EnhancedTaskManager(
    "my_service",
    api_base_url="http://localhost:8080"
)

# Add tasks
manager.add_task(1, "Process order", queue_name="orders")
manager.add_task(2, "Send notification", queue_name="notifications")

# Get statistics
stats = manager.get_statistics()

# Sync to API
results = manager.sync_edges_to_api()
```

## 📊 Data Models

### QueueEdge

```python
@dataclass
class QueueEdge:
    edge_id: str                    # Unique identifier
    source_identifier: str          # Service/module name
    queue_identifier: str           # Queue name
    operation_type: str             # produce, consume, publish, subscribe, etc.
    pattern: str                    # message_queue, pub_sub, topic, etc.
    request: Optional[QueueEdgeRequest]
    response: Optional[QueueEdgeResponse]
    api_provider_edges: List[str]   # Incoming API edges
    queue_call_edges: List[str]     # Outgoing queue calls
    tags: List[str]
    metadata: Dict[str, Any]
```

### QueueOperationType

```
PRODUCE = "produce"      # Publishing/sending to queue
CONSUME = "consume"      # Receiving/reading from queue
PUBLISH = "publish"
SUBSCRIBE = "subscribe"
SEND = "send"
RECEIVE = "receive"
```

### QueuePattern

```
MESSAGE_QUEUE = "message_queue"
PUBLISH_SUBSCRIBE = "pub_sub"
REQUEST_REPLY = "request_reply"
TOPIC = "topic"
QUEUE = "queue"
EVENT_STREAM = "event_stream"
TASK_QUEUE = "task_queue"
```

## 🔍 Detection Patterns

### RabbitMQ
- `channel.basic_publish` - Publish operations
- `channel.basic_consume` - Consume operations
- `pika.BasicProperties` - Message properties
- `start_consuming` - Start consuming

### Kafka
- `KafkaProducer` - Producer initialization
- `producer.send` - Send messages
- `KafkaConsumer` - Consumer initialization
- `consumer.poll` - Poll for messages

### AWS SQS
- `send_message` - Send operations
- `receive_message` - Receive operations
- `SendMessage` - Message operation
- `ReceiveMessage` - Message operation

### Generic Queues
- `queue.put()` - Enqueue
- `queue.get()` - Dequeue
- `.enqueue()` - Enqueue
- `.dequeue()` - Dequeue

## 🔗 Edge Linking

### Automatic Linking

```python
linker = EdgeLinker()
stats = linker.auto_link_edges(collection)
# Links producers to consumers by queue identifier
```

### Manual Linking

```python
# Link two edges
linker.link_queue_call(source_id, target_id)

# Link to API provider
linker.link_queue_to_api_provider(queue_edge_id, api_edge_id)
```

### Querying Links

```python
# Get dependencies
deps = linker.get_edge_dependencies(edge_id)
# Returns: {"incoming": [...], "outgoing": [...]}

# Find path between edges
path = linker.get_edge_path(start_id, end_id)
# Returns: [edge1, edge2, edge3, ...]
```

## 🌐 API Integration

### Endpoints

- `POST /api/v1/queue-edges` - Create edge
- `GET /api/v1/queue-edges/{id}` - Get edge
- `PUT /api/v1/queue-edges/{id}` - Update edge
- `DELETE /api/v1/queue-edges/{id}` - Delete edge
- `POST /api/v1/queue-edges/bulk` - Bulk create
- `POST /api/v1/queue-edges/links` - Create link
- `GET /api/v1/queue-edges` - Query edges
- `GET /api/v1/queue-edges/graph` - Get graph
- `POST /api/v1/queue-edges/sync` - Sync collection

### Authentication

```python
client = QueueEdgeAPIClient(
    api_base_url="http://localhost:8080",
    api_key="your-api-key"
)
```

### Synchronization

```python
sync = QueueEdgeIndexSync(api_client)

# Sync from API
stats = sync.sync_from_api()

# Sync to API
stats = sync.sync_to_api(collection)
```

## 📈 Statistics and Reporting

### Get Statistics

```python
manager = EnhancedTaskManager("my_service")
stats = manager.get_statistics()

# Returns:
# {
#   "service_name": "my_service",
#   "pending_tasks": 5,
#   "processed_tasks": 10,
#   "total_tasks": 15,
#   "tracked_edges": 8,
#   "api_integration": true,
#   "edge_statistics": {
#     "produce_edges": 3,
#     "consume_edges": 2,
#     "linked_edges": 4
#   }
# }
```

### Index Statistics

```python
indexer = QueueEdgeIndexer()
indexer.build_index(collection)
stats = indexer.get_statistics()

# Returns:
# {
#   "total_edges": 10,
#   "services": 3,
#   "queues": 5,
#   "operation_types": 2,
#   "patterns": 3,
#   "index_by_service": {...},
#   "index_by_queue": {...},
#   ...
# }
```

## 🧪 Testing

Run the test suite:

```bash
python test_queue_edges.py
```

Test coverage includes:
- Queue edge model creation and validation
- Edge detection in source code
- Edge linking and graph generation
- API integration
- Task management and tracking
- Statistics and reporting

## 📝 Examples

### Example 1: Complete Workflow

```python
from queue_edge_detector import QueueEdgeDetector
from queue_edge_linker import EdgeLinker
from queue_edge_api import QueueEdgeIntegrationManager

# 1. Detect edges
detector = QueueEdgeDetector()
collection = detector.detect_in_directory("./src", "my_service")

# 2. Link edges
linker = EdgeLinker()
for edge in collection.edges:
    linker.register_queue_edge(edge)
linker.auto_link_edges(collection)

# 3. Sync to API
manager = QueueEdgeIntegrationManager("http://localhost:8080", "api-key")
results = manager.process_and_sync(collection)

print(f"Synced {results['linking_stats']['linked_edges']} edges")
```

### Example 2: Task Management with Edges

```python
from enhanced_queue_manager import EnhancedTaskManager

manager = EnhancedTaskManager("order_service")

# Register callbacks
def on_task_added(message, edge):
    print(f"Task added: {message.description}")

def on_task_processed(message):
    print(f"Task processed: {message.description}")

manager.register_task_added_callback(on_task_added)
manager.register_task_processed_callback(on_task_processed)

# Add and process tasks
manager.add_task(1, "Process order", queue_name="orders")
manager.add_task(2, "Send notification", queue_name="notifications")

while True:
    task = manager.get_next_task()
    if not task:
        break
```

### Example 3: Edge Graph Visualization

```python
from queue_edge_linker import EdgeLinker
import json

linker = EdgeLinker()
# ... register and link edges ...

graph = linker.get_edge_graph()
print(json.dumps(graph, indent=2))

# Output:
# {
#   "nodes": [
#     {"id": "edge_1", "label": "service_a:queue_1", "type": "queue", ...},
#     {"id": "edge_2", "label": "service_b:queue_1", "type": "queue", ...}
#   ],
#   "edges": [
#     {"source": "edge_1", "target": "edge_2", "type": "queue_call"}
#   ]
# }
```

## 🔐 Best Practices

1. **Always validate edges before syncing**
   ```python
   if QueueEdgeSchema.validate_edge(edge.to_dict()):
       # Sync to API
   ```

2. **Use meaningful identifiers**
   ```python
   edge_id = f"queue_edge_{service}_{queue}_{operation}_{uuid}"
   ```

3. **Track metadata for debugging**
   ```python
   edge.metadata = {
       "file": file_path,
       "line": line_number,
       "system": "RabbitMQ",
       "timestamp": datetime.utcnow().isoformat()
   }
   ```

4. **Implement callbacks for monitoring**
   ```python
   manager.register_task_added_callback(log_task_added)
   manager.register_task_processed_callback(log_task_processed)
   ```

5. **Export and backup regularly**
   ```python
   json_export = manager.export_to_json()
   with open("queue_edges_backup.json", "w") as f:
       f.write(json_export)
   ```

## 🐛 Troubleshooting

### Issue: Detection not finding queue operations

**Solution**: Check that the code patterns match your implementation. Update `QueueOperationPattern` in `queue_edge_detector.py` to include your patterns.

### Issue: API connection fails

**Solution**: Verify API server is running and accessible:
```python
try:
    response = client._make_request("GET", "/api/v1/health")
except Exception as e:
    print(f"API connection error: {e}")
```

### Issue: Edges not linking

**Solution**: Ensure queue identifiers match between producer and consumer:
```python
# These will link automatically
producer.queue_identifier == consumer.queue_identifier
```

## 📚 Additional Resources

- [JIRA Ticket: BITO-12018](https://bito.atlassian.net/browse/BITO-12018)
- [Parent Ticket: BITO-12017](https://bito.atlassian.net/browse/BITO-12017)
- Queue Edge Script: `queue_edges_script-v3.zip`
- Patch Script: `patch_queue_edges.sh`

## 🤝 Contributing

When adding new features:

1. Add corresponding tests in `test_queue_edges.py`
2. Update this documentation
3. Follow the existing code style
4. Ensure all tests pass

## 📄 License

This implementation is part of the Bito ai-architect project.

---

**Last Updated**: February 9, 2026
**Version**: 1.0
**Status**: Production Ready ✅
