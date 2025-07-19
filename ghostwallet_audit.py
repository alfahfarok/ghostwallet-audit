import time
import datetime
from web3 import Web3
from typing import List, Dict

class GhostWalletAuditor:
    def __init__(self, rpc_url: str):
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))
        assert self.web3.isConnected(), "Web3 connection failed."

    def audit_wallets(self, addresses: List[str], inactivity_days: int = 365) -> List[Dict]:
        current_block = self.web3.eth.block_number
        ghost_wallets = []

        for address in addresses:
            try:
                tx_count = self.web3.eth.get_transaction_count(address)
                if tx_count == 0:
                    balance = self.web3.eth.get_balance(address)
                    if balance > 0:
                        ghost_wallets.append({
                            "address": address,
                            "status": "no tx ever",
                            "balance": self.web3.fromWei(balance, 'ether')
                        })
                    continue

                latest_tx_block = self._get_latest_tx_block(address)
                if not latest_tx_block:
                    continue

                latest_block_time = self._get_block_timestamp(latest_tx_block)
                delta_days = (time.time() - latest_block_time) / (60 * 60 * 24)

                if delta_days >= inactivity_days:
                    balance = self.web3.eth.get_balance(address)
                    ghost_wallets.append({
                        "address": address,
                        "last_active_days_ago": round(delta_days),
                        "balance": self.web3.fromWei(balance, 'ether')
                    })
            except Exception as e:
                print(f"[!] Error analyzing {address}: {e}")

        return ghost_wallets

    def _get_latest_tx_block(self, address: str):
        # NOTE: This requires using external API or archive node for full accuracy.
        # We'll simulate with current implementation as placeholder.
        # Real implementation would use Etherscan or block explorer API.
        return None

    def _get_block_timestamp(self, block_number: int):
        block = self.web3.eth.get_block(block_number)
        return block.timestamp
