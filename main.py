import multiprocessing as mp
from bitcoin_utils import generate_bitcoin_address  # This will now import the Cython version
import time
import argparse

def check_range(start, end, target_address, chunk_id, result_queue):
    for i in range(start, end):
        if i % 1000000 == 0:
            print(f"Chunk {chunk_id}: Checked {i - start:,} keys")
        private_key = format(i, '064x')
        address = generate_bitcoin_address(private_key)
        if address == target_address:
            result_queue.put(private_key)
            return
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

    num_cores = mp.cpu_count()-2
    print(f"Using {num_cores} CPU cores")
    
    chunk_size = (end - start) // num_cores
    ranges = [(start + i * chunk_size, start + (i + 1) * chunk_size, i) for i in range(num_cores)]
    
    result_queue = mp.Queue()
    processes = []
    
    start_time = time.time()
    
    for r in ranges:
        p = mp.Process(target=check_range, args=(r[0], r[1], target_address, r[2], result_queue))
        processes.append(p)
        p.start()
    
    solution = None
    completed_processes = 0
    
    while completed_processes < num_cores:
        result = result_queue.get()
        if result is not None:
            solution = result
            break
        completed_processes += 1
    
    for p in processes:
        p.terminate()
    
    for p in processes:
        p.join()
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    if solution:
        print(f"Solution found! Private key: {solution}")
    else:
        print("No solution found in the given range.")
    
    print(f"Total execution time: {elapsed_time:.2f} seconds")
    # Note: This is an approximation, as we don't know exactly how many keys were checked
    print(f"Approximate keys checked per second: {((end - start) / elapsed_time):,.2f}")

def test():
    private_key = format(0x68f3, '064x')
    address = generate_bitcoin_address(private_key)
    print(f"Private key: {private_key}")
    print(f"Address: {address}")

if __name__ == "__main__":
    main()
