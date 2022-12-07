import asyncio
from temporalio.client import Client
from greeting import GreetingWorkflow

async def create_greeting(client: Client) -> str:
    greeting = GreetingWorkflow()
    # Start the workflow
    handle = await client.start_workflow(greeting.run, "M@", id="temp-trial-2", task_queue="my-task-queue")
    # Change the salutation
    await handle.signal(greeting.update_salutation, "Aloha")
    # Tell it to complete
    await handle.signal(greeting.complete_with_greeting)
    # Wait and return result
    return await handle.result()
