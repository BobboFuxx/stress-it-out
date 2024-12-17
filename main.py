import asyncio
from validator_scanner import scan_and_display
from stress_tester import start_stress_test

def main():
    print("Select an option:")
    print("1. Scan for validators with open RPC endpoints")
    print("2. Stress test an RPC endpoint (Overload Mode)")
    
    choice = input("Enter your choice: ").strip()
    
    if choice == "1":
        print("Starting validator scan...")
        asyncio.run(scan_and_display())
    elif choice == "2":
        print("Starting RPC Overload Stress Test...")
        asyncio.run(start_stress_test())
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
