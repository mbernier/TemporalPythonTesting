This is a modified version of the example code from https://github.com/temporalio/sdk-python

Specifically the samples found in these sections:
[Worker](https://github.com/temporalio/sdk-python#workers)
[Workflows](https://github.com/temporalio/sdk-python#workflows)
[Running](https://github.com/temporalio/sdk-python#running)

## Modifications:
*greeting.py*
I copied the code from "Workflow" section linked above into greeting.py
1. Removed the following imports that are not used in this file: 
    ```python
        from temporalio.client import Client
        from temporalio.worker import Worker
    ```

*worker.py* 
Copied the code from "Worker" section above, made these modifications: 

Made these modifications from the example code:
```python
    import asyncio
    # -- removed this bc it's not used in the example
    # --import logging
    from temporalio.client import Client
    from temporalio.worker import Worker
    # Import your own workflows and activities
    # -- from my_workflow_package import MyWorkflow, my_activity
    # ++ include the class and method from greeting.py
    from greeting import GreetingWorkflow, create_creeting_activity
    # ++ include the client code 
    from client import create_greeting

    # -- I could not figure out how/why we were passing an asyncio.Event here, so removed it
    # -- async def run_worker(stop_event: asyncio.Event):
    # ++ Change to this
    async def run_worker():

        # Create client connected to server at the given address
        # -- client = await Client.connect("localhost:7233", namespace="my-namespace")
        # ++
        client = await Client.connect("localhost:7233", namespace="default")

        # Run the worker until the event is set
        worker = Worker(client, 
                        task_queue="my-task-queue", 
        # --                workflows=[MyWorkflow], 
        # ++
                        workflows=[GreetingWorkflow]
        # --                activities=[my_activity])
        # ++
                        activities=[create_greeting_activity])

        async with worker:
        # --    this can't run, if removed from method params
        # --    await stop_event.wait()
        # ++
            result = await create_greeting(client)
        # ++
            print(f"Greeting: {result}")

    # ++
    if __name__ == "__main__":
    # ++
        asyncio.run(run_worker())
```

*Client*
Copied code from "running" section linked above
1. Added the import to pull in the Greeting workflow class
    ```python
        from greeting import GreetingWorkflow
    ```

## Run the code 
`python worker.py`

## other notes
You get the same output to the console if: 

in *client.py#l13*, you change:
```python
    return await handle.result()
```
to this: 
```python
        result = await handle.result()
        print(f"Greeting: {result}")
```

And you change *worker.py#L20-21* to:
```python
    await create_greeting(client)
```
