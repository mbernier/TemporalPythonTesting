import asyncio
from temporalio.client import Client

# Import the workflow from the previous code
from run_worker import SayHello

async def main():
    # Create client connected to server at the given address and namespace
    client = await Client.connect("localhost:7233", namespace="default")

    # Start a workflow
    handle = await client.start_workflow(SayHello.run, "M@", id="my-workflow-id", task_queue="my-task-queue")

    # Wait for result
    result = await handle.result()
    print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())