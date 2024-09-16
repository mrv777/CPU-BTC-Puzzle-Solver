import multiprocessing as mp
from bitcoin_utils import generate_bitcoin_address  # This will now import the Cython version
import time
import argparse
from tqdm import tqdm  # Import tqdm for progress bar
import queue  # Import queue to handle empty exceptions
import random

def check_range(start, end, target_address, chunk_id, result_queue, progress_counter, lock):
    batch_size = 10000
    keys_to_check = list(range(start, end))
    random.shuffle(keys_to_check)  # Randomize the order of keys to check

    for i, key in enumerate(keys_to_check):
        if i % batch_size == 0 and i != 0:
            with lock:
                progress_counter.value += batch_size
            if i % 1000000 == 0:
                print(f"Chunk {chunk_id}: Checked {i:,} keys")
        
        private_key = format(key, '064x')
        address = generate_bitcoin_address(private_key)
        if address == target_address:
            result_queue.put(private_key)
            return

    # Handle remaining keys
    remaining = len(keys_to_check) % batch_size
    if remaining:
        with lock:
            progress_counter.value += remaining
    result_queue.put(None)

def main():
    parser = argparse.ArgumentParser(description="Bitcoin private key brute-force search")
    parser.add_argument("--puzzle", type=int, choices=[15, 20, 22, 24, 25, 30, 67, 71], required=True, help="Puzzle number to solve")
    parser.add_argument("--start", type=lambda x: int(x, 0), help="Start of range (in hex)")
    parser.add_argument("--end", type=lambda x: int(x, 0), help="End of range (in hex)")
    args = parser.parse_args()

    if args.puzzle == 15:
        target_address = "1QCbW9HWnwQWiQqVo5exhAnmfqKRrCRsvW"
        start = args.start or 0x4000
        end = args.end or 0x7fff
    elif args.puzzle == 20:
        target_address = "1HsMJxNiV7TLxmoF6uJNkydxPFDog4NQum"
        start = args.start or 0x80000
        end = args.end or 0xfffff
    elif args.puzzle == 22:
        target_address = "1CfZWK1QTQE3eS9qn61dQjV89KDjZzfNcv"
        start = args.start or 0x200000
        end = args.end or 0x3fffff
    elif args.puzzle == 24:
        target_address = "1rSnXMr63jdCuegJFuidJqWxUPV7AtUf7"
        start = args.start or 0x800000
        end = args.end or 0xffffff
    elif args.puzzle == 25:
        target_address = "15JhYXn6Mx3oF4Y7PcTAv2wVVAuCFFQNiP"
        start = args.start or 0x1000000
        end = args.end or 0x1ffffff
    elif args.puzzle == 30:
        target_address = "1LHtnpd8nU5VHEMkG2TMYYNUjjLc992bps"
        start = args.start or 0x20000000
        end = args.end or 0x3fffffff
    elif args.puzzle == 67:
        target_address = "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9"
        start = args.start or 0x40000000000000000
        end = args.end or 0x7ffffffffffffffff
    elif args.puzzle == 71:
        target_address = "1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU"
        start = args.start or 0x400000000000000000
        end = args.end or 0x7fffffffffffffffff

    num_cores = mp.cpu_count() - 2  # Reserve 2 cores for other tasks
    print(f"Using {num_cores} CPU cores")

    chunk_size = (end - start) // num_cores
    ranges = [(start + i * chunk_size, start + (i + 1) * chunk_size, i) for i in range(num_cores)]

    # Add a small overlap between chunks
    overlap = min(1000, chunk_size // 100)  # 1% overlap or 1000 keys, whichever is smaller
    ranges = [(max(start, r[0] - overlap), min(end, r[1] + overlap), r[2]) for r in ranges]

    result_queue = mp.Queue()

    manager = mp.Manager()
    progress_counter = manager.Value('Q', 0)  # Changed from 'i' to 'Q' for larger ranges
    lock = manager.Lock()  # Lock to synchronize access to the counter

    processes = []

    start_time = time.time()

    for r in ranges:
        p = mp.Process(target=check_range, args=(r[0], r[1], target_address, r[2], result_queue, progress_counter, lock))
        processes.append(p)
        p.start()

    total_keys = end - start
    with tqdm(total=total_keys, desc="Progress", unit="keys") as pbar:
        solution = None
        completed_processes = 0
        last_progress = 0
        while completed_processes < num_cores and solution is None:
            try:
                result = result_queue.get(timeout=1)  # Wait for 1 second
                if result is not None:
                    solution = result
                    break
                completed_processes += 1
            except queue.Empty:
                # No result received in the last second, continue to update progress
                pass
            # Update progress bar
            with lock:
                current_progress = progress_counter.value
            delta = current_progress - last_progress
            if delta > 0:
                pbar.update(delta)
                last_progress = current_progress

    # **Final Progress Update Before Termination**
    with lock:
        current_progress = progress_counter.value
    delta = current_progress - last_progress
    if delta > 0:
        pbar.update(delta)
        last_progress = current_progress

    # Terminate all processes if a solution was found
    if solution:
        for p in processes:
            p.terminate()

    for p in processes:
        p.join()

    end_time = time.time()
    elapsed_time = end_time - start_time

    # **Use progress_counter.value for Final Calculation**
    keys_checked = progress_counter.value

    if solution:
        print(f"\nSolution found! Private key: {solution}")
    else:
        print("\nNo solution found in the given range.")

    print(f"Total execution time: {elapsed_time:.2f} seconds")
    print(f"Approximate keys checked per second: {(keys_checked / elapsed_time):,.2f}")

def test():
    private_key = format(0x68f3, '064x')
    address = generate_bitcoin_address(private_key)
    print(f"Private key: {private_key}")
    print(f"Address: {address}")

if __name__ == "__main__":
    main()
