import aiohttp
import asyncio
from config import IP_LIST, DEFAULT_RPC_PORT, REQUEST_TIMEOUT

TEST_PAYLOAD = { "jsonrpc": "2.0", "method": "web3_clientVersion", "params": [], "id": 1 }

async def test_rpc_endpoint(session, url):
    """Check if the RPC endpoint is open and responding."""
    try:
        async with session.post(url, json=TEST_PAYLOAD, timeout=REQUEST_TIMEOUT) as response:
            if response.status == 200:
                text = await response.text()
                if "jsonrpc" in text:
                    return True, text
    except Exception:
        pass
    return False, None

async def scan_validators(ip_list, rpc_port):
    """
    Scan a list of IP addresses for open RPC endpoints.

    Args:
        ip_list (list): List of IPs or hostnames to scan.
        rpc_port (int): Port to test for RPC access.

    Returns:
        list: List of open RPC endpoints.
    """
    results = []

    async with aiohttp.ClientSession() as session:
        tasks = []
        for ip in ip_list:
            url = f"http://{ip}:{rpc_port}"
            tasks.append(test_rpc_endpoint(session, url))

        responses = await asyncio.gather(*tasks)
        for ip, (is_open, response) in zip(ip_list, responses):
            if is_open:
                print(f"Open RPC found at {ip}:{rpc_port}")
                results.append({"url": f"http://{ip}:{rpc_port}", "response": response})

    return results

async def scan_and_display():
    """Run the scan and display results."""
    print(f"Scanning {len(IP_LIST)} validators on port {DEFAULT_RPC_PORT}...")
    open_rpcs = await scan_validators(IP_LIST, DEFAULT_RPC_PORT)

    if open_rpcs:
        print("\nOpen RPC Endpoints Found:")
        for rpc in open_rpcs:
            print(f" - {rpc['url']}")
    else:
        print("No open RPC endpoints found.")
