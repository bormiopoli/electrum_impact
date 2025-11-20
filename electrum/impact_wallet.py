from electrum.wallet_db import WalletDB
from electrum.storage import WalletStorage
from electrum.address_synchronizer import AddressSynchronizer


class WizardWallet(AddressSynchronizer):
    def __init__(self, storage: WalletStorage, network):
        super().__init__(network)
        self.storage = storage
        self.db = WalletDB(self.storage.read(), upgrade=True)

        # hydrate impact info
        self._impact = self.db.data.get('impact_info', [])

        # ensure cumulative field exists
        if 'impact_cum' not in self.db.data:
            self.db.data['impact_cum'] = {}
            self.storage.write(self.db.dump())

    @property
    def impact(self):
        return self._impact

    @impact.setter
    def impact(self, val):
        self._impact = val
        self.db.data['impact_info'] = val
        self.storage.write(self.db.dump())

    def receive_tx_callback(self, tx):
        # preserve original behavior
        super().receive_tx_callback(tx)

        # compute cumulative impact based on outputs
        try:
            amount = sum(o.value for o in tx.outputs()) if hasattr(tx, 'outputs') else 0
        except Exception:
            amount = 0

        # update cumulative impact
        current_cum = self.db.data.get('impact_cum', 0)
        self.db.data['impact_cum'] = current_cum + amount

        # optionally store last tx context
        self.db.data['impact_last_tx'] = {
            'txid': tx.txid() if hasattr(tx, 'txid') else None,
            'amount': amount
        }

        # persist changes
        self.storage.write(self.db.dump())
