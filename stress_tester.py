import asyncio
import aiohttp
import time
from config import REQUEST_TIMEOUT

# Example custom payloads
LIGHT_PAYLOAD = { "jsonrpc": "2.0", "method": "eth_blockNumber", "params": [], "id": 1 }

HEAVY_PAYLOADS = [
    { "jsonrpc": "2.0", "method": "eth_getLogs", "params": [{"fromBlock": "0x0", "toBlock": "latest"}], "id": 1 },
    { "jsonrpc": "2.0", "method": "eth_getBlockByNumber", "params": ["0x1", True], "id": 2 },
    { "jsonrpc": "2.0", "method": "eth_getBalance", "params": ["0x0000000000000000000000000000000000000000", "latest"], "id": 3 },
]

BATCH_PAYLOAD = [
    { "jsonrpc": "2.0", "method": "eth_blockNumber", "params": [], "id": i }
    for i in range(1, 101)
]

async def send_request(session, url, payload):
    """Send a single JSON-RPC request."""
    try:
        async with session.post(url, json=payload, timeout=REQUEST_TIMEOUT) as response:
            return response.status, await response.text()
    except Exception as e:
        return "error", str(e)

async def overload_rpc(url, num_requests, concurrency, payloads):
    """
    Overload the RPC endpoint with massive requests.
    
    Args:
        url (str): The target RPC URL.
        num_requests (int): Total number of requests to send.
        concurrency (int): Number of concurrent requests.
        payloads (list): A list of payloads to send.
    """
    async def worker(queue, session):
        while not queue.empty():
            payload = await queue.get()
            status, response = await send_request(session, url, payload)
            print(f"Sent request - Status: {status}, Response: {response[:100]}")  # Log trimmed response
    
    queue = asyncio.Queue()
    for _ in range(num_requests):
        for payload in payloads:
            await queue.put(payload)

    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(worker(queue, session)) for _ in range(concurrency)]
        await asyncio.gather(*tasks)

async def start_stress_test():
    """Start the overload stress test."""
    target_url = input("Enter the target RPC URL: ").strip()
    total_requests = 10000  # Total requests to send
