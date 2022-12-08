import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
# Import your own workflows and activities
from greeting import GreetingWorkflow, create_greeting_activity
from client import create_greeting

# async def run_worker(stop_event: asyncio.Event):
async def run_worker(): 
    # Create client connected to server at the given address
    client = await Client.connect("localhost:7233", namespace="default")

    # Run the worker until the event is set
    worker = Worker(client, 
                        task_queue="my-task-queue", 
                        workflows=[GreetingWorkflow], 
                        activities=[create_greeting_activity])

    async with worker:
        result = await create_greeting(client)
        print(f"Greeting: {result}")

if __name__ == "__main__":
    asyncio.run(run_worker())