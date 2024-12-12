
## Creating vector stores and adding files 

You can create a vector store and add files to it in a single API call:

```python
vector_store = project_client.agents.create_vector_store_file_batch_and_poll(
  name="my_vector_store",
  file_ids=['file_path_1', 'file_path_2', 'file_path_3', 'file_path_4', 'file_path_5']
)
```

Adding files to vector stores is an async operation. To ensure the operation is complete, we recommend that you use the 'create and poll' helpers in our official SDKs. If you're not using the SDKs, you can retrieve the `vector_store` object and monitor its `file_counts` property to see the result of the file ingestion operation.

Files can also be added to a vector store after it's created by creating vector store files.

```python

# create a vector store with no file and wait for it to be processed
vector_store = project_client.agents.create_vector_store_and_poll(data_sources=[], name="sample_vector_store")
print(f"Created vector store, vector store ID: {vector_store.id}")

# add the file to the vector store or you can supply file ids in the vector store creation
vector_store_file_batch = project_client.agents.create_vector_store_file_batch_and_poll(
    vector_store_id=vector_store.id, file_ids=[file.id]
)
print(f"Created vector store file batch, vector store file batch ID: {vector_store_file_batch.id}")

```

Alternatively, you can add several files to a vector store by creating batches of up to 500 files.

```python
batch = project_client.agents.create_vector_store_file_batch_and_poll(
  vector_store_id=vector_store.id,
  file_ids=['file_1', 'file_2', 'file_3', 'file_4', 'file_5']
)
```

### Basic agent setup: Deleting files from vector stores
Files can be removed from a vector store by either:

* Deleting the vector store file object or,
* By deleting the underlying file object (which removes the file it from all vector_store and code_interpreter configurations across all agents and threads in your organization)

The maximum file size is 512 MB. Each file should contain no more than 5,000,000 tokens per file (computed automatically when you attach a file).


## Remove vector store 

You can can remove a vector store from the file search tool.

```python
file_search_tool.remove_vector_store(vector_store.id)
print(f"Removed vector store from file search, vector store ID: {vector_store.id}")

project_client.agents.update_agent(
    assistant_id=agent.id, tools=file_search_tool.definitions, tool_resources=file_search_tool.resources
)
print(f"Updated agent, agent ID: {agent.id}")

```

## Deleting vector stores
```python
project_client.agents.delete_vector_store(vector_store.id)
print("Deleted vector store")
```

## Ensuring vector store readiness before creating runs

We highly recommend that you ensure all files in a vector_store are fully processed before you create a run. This ensures that all the data in your vector store is searchable. You can check for vector store readiness by using the polling helpers in the SDKs, or by manually polling the `vector_store` object to ensure the status is completed.

As a fallback, there's a 60-second maximum wait in the run object when the thread's vector store contains files that are still being processed. This is to ensure that any files your users upload in a thread a fully searchable before the run proceeds. This fallback wait does not apply to the agent's vector store.

## Managing costs with expiration policies

For basic agent setup. the `file_search` tool uses the `vector_stores` object as its resource and you will be billed based on the size of the vector_store objects created. The size of the vector store object is the sum of all the parsed chunks from your files and their corresponding embeddings.

In order to help you manage the costs associated with these vector_store objects, we have added support for expiration policies in the `vector_store` object. You can set these policies when creating or updating the `vector_store` object.

```python
vector_store = project_client.agents.create_vector_store_and_poll(
  name="Product Documentation",
  file_ids=['file_1', 'file_2', 'file_3', 'file_4', 'file_5'],
  expires_after={
      "anchor": "last_active_at",
      "days": 7
  }
)
```

### Thread vector stores have default expiration policies

Vector stores created using thread helpers (like `tool_resources.file_search.vector_stores` in Threads or `message.attachments` in Messages) have a default expiration policy of seven days after they were last active (defined as the last time the vector store was part of a run).

When a vector store expires, the runs on that thread fail. To fix this, you can recreate a new vector_store with the same files and reattach it to the thread.

```python
all_files = list(client.beta.vector_stores.files.list("vs_expired"))

vector_store = client.beta.vector_stores.create(name="rag-store")
client.beta.threads.update(
    "thread_abc123",
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
)

for file_batch in chunked(all_files, 100):
    client.beta.vector_stores.file_batches.create_and_poll(
        vector_store_id=vector_store.id, file_ids=[file.id for file in file_batch]
    )
```