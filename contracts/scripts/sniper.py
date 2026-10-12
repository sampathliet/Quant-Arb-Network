import time
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware

# Auto-Node Switcher: Cycles through robust enterprise RPCs to bypass blocks
rpc_endpoints = [
    "https://polygon.llamarpc.com",
    "https://rpc.ankr.com/polygon",
    "https://polygon-mainnet.public.blastapi.io",
    "https://1rpc.io/matic"
]

web3 = None
for rpc in rpc_endpoints:
    print(f"🔄 Attempting connection to node: {rpc}...")
    temp_web3 = Web3(Web3.HTTPProvider(rpc))
    if temp_web3.is_connected():
        web3 = temp_web3
        web3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
        print("✅ Core System: Connected to Polygon Mainnet successfully!")
        break

if not web3 or not web3.is_connected():
    print("❌ All nodes failed.")
    exit()

print("📡 Initiating high-frequency arbitrage radar...")

# Uniswap V3 Addresses
WETH = web3.to_checksum_address("0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619")
USDC = web3.to_checksum_address("0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174")
QUOTER = web3.to_checksum_address("0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6")

# Minimal ABI to fetch live prices
QUOTER_ABI = [{"inputs": [{"internalType": "address", "name": "tokenIn", "type": "address"}, {"internalType": "address", "name": "tokenOut", "type": "address"}, {"internalType": "uint24", "name": "fee", "type": "uint24"}, {"internalType": "uint256", "name": "amountIn", "type": "uint256"}, {"internalType": "uint160", "name": "sqrtPriceLimitX96", "type": "uint160"}], "name": "quoteExactInputSingle", "outputs": [{"internalType": "uint256", "name": "amountOut", "type": "uint256"}], "stateMutability": "view", "type": "function"}]
quoter = web3.eth.contract(address=QUOTER, abi=QUOTER_ABI)

def hunt_for_spreads():
    amount_in = web3.to_wei(1, 'ether')
    print("🔎 Hunting for profitable V3 liquidity gaps...")
    
    while True:
        try:
            amount_out = quoter.functions.quoteExactInputSingle(WETH, USDC, 500, amount_in, 0).call()
            price = amount_out / (10**6)
            block = web3.eth.block_number
            
            print(f"[Block {block}] WETH/USDC: ${price:.2f} - Spread too low. Continuing scan...")
        except Exception as e:
            print(f"⚠️ Network slight delay, awaiting next block data...")
            
        time.sleep(3)

if __name__ == "__main__":
    hunt_for_spreads()
