import asyncio
import random

async def client_order_handler(order_queue, distributor_queues):
    while True:
        # Simulate client order
        order = "Order " + str(random.randint(1, 100))
        print(f"Received order: {order}")

        # Check distributor availability and assign orders
        assigned = False
        for queue in distributor_queues:
            if not queue.full():
                await queue.put(order)
                print(f"{order} assigned to distributor")
                assigned = True
                break
        if not assigned:
            print(f"No available distributors for {order}. Queueing order.")
            await order_queue.put(order)

        await asyncio.sleep(1)

async def distributor_task(id, distributor_queue, order_queue, order_completion_times):
    while True:
        if not distributor_queue.empty():
            order = await distributor_queue.get()
            print(f"Distributor {id} is preparing {order}")
            await asyncio.sleep(3)
            print(f"Distributor {id} has prepared {order}")
            await asyncio.sleep(1)
            print(f"Distributor {id} is available")
        else:
            if not order_queue.empty():
                order = await order_queue.get()
                print(f"Distributor {id} is preparing queued order {order}")
                await asyncio.sleep( 3)
                print(f"Distributor {id} has prepared queued order {order}")
                await asyncio.sleep(1)
                print(f"Distributor {id} is available")

async def order_completion_tracker(order_completion_times):
    while True:
        # Monitor order timestamps and calculate completion times
        # Trigger alerts for delays if needed
        await asyncio.sleep(2)

async def main():
    order_queue = asyncio.Queue()
    distributor_queues = [asyncio.Queue() for _ in range(3)]
    order_completion_times = []

    handlers = [client_order_handler(order_queue, distributor_queues) for _ in range(8)]
    distributors = [distributor_task(i, distributor_queues[i % 3], order_queue, order_completion_times) for i in range(3)]
    tracker = order_completion_tracker(order_completion_times)

    await asyncio.gather(*handlers, *distributors, tracker)

if __name__ == "__main__":
    asyncio.run(main())