import concurrent.futures
import random
import queue
import time

def client_order_handler(order_queue, distributor_queues):
    while True:
        # Simulate client order
        order = "Order " + str(random.randint(1, 100))
        print(f"Received order: {order}")

        # Check distributor availability and assign orders
        assigned = False
        for queue in distributor_queues:
            try:
                queue.put_nowait(order)
                print(f"{order} assigned to distributor")
                assigned = True
                break
            except queue.Full:
                continue
        if not assigned:
            print(f"No available distributors for {order}. Queueing order.")
            order_queue.put(order)

        time.sleep(1)

def distributor_task(id, distributor_queue, order_queue):
    while True:
        try:
            order = distributor_queue.get_nowait()
            print(f"Distributor {id} is preparing {order}")
        except queue.Empty:
            try:
                order = order_queue.get_nowait()
                print(f"Distributor {id} is preparing queued order {order}")
            except queue.Empty:
                # Distributor is idle
                time.sleep(1)
                continue

        time.sleep(random.random() * 3)
        print(f"Distributor {id} has prepared {order}")
        time.sleep(1)
        print(f"Distributor {id} is available")

def order_completion_tracker():
    while True:
        time.sleep(2)

def main():
    order_queue = queue.Queue()
    distributor_queues = [queue.Queue() for _ in range(3)]
    order_completion_times = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=11) as executor:
        executor.submit(order_completion_tracker, order_completion_times)
        for id in range(8):
            executor.submit(client_order_handler, order_queue, distributor_queues)
        for i in range(3):
            executor.submit(distributor_task, i, distributor_queues[i], order_queue, order_completion_times)

if __name__ == "__main__":
    main()
