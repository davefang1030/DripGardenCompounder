from web3 import Web3
from web3.middleware import geth_poa_middleware
from datetime import datetime, timedelta
import time
import numpy as np
import json
import argparse
import textwrap


class DripGardenCompounder:
    """
    This is the auto compounder for Drip Garden so you won't need to wait for the right time to click "Plant Seeds" so you
    don't lose seeds compounded that day. It basically hooks up with drip garden contract and figure out when the next time
    for plant to mature (so we don't waste seeds) and wait til that time and compound it automatically. The code will run
    in a loop until you ^-C it. But you can later re-run it to pick up what is left.
    """
    def __init__(self, json_config_file):
        """
        Create Drip Garden Compounder from config file
        :param json_config_file: json config file that contains your wallet address, your referral address and private key
                Don't show this json file to other people!!!
        """
        config = json.load(open(json_config_file))
        self.wallet_address = config['wallet_address']
        if not config['referral_address']:
            # referral address empty, set the referral to 0xdEaD
            self.ref_address = '0x000000000000000000000000000000000000dEaD'
        else:
            self.ref_address = config['referral_address']
        self.private_key = config['key']

        self.web3 = Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org/"))
        self.drip_garden = '0x685BFDd3C2937744c13d7De0821c83191E3027FF'
        self.drip_garden_abi = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"address","name":"ref","type":"address"},{"indexed":false,"internalType":"uint256","name":"amountBNB","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amountEggs","type":"uint256"}],"name":"SeedsBought","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"address","name":"ref","type":"address"},{"indexed":false,"internalType":"uint256","name":"seedsUsed","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"marketSeeds","type":"uint256"}],"name":"SeedsPlanted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"seedsSold","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"seedValue","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"marketSeeds","type":"uint256"}],"name":"SeedsSold","type":"event"},{"inputs":[],"name":"BusdAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"DripAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"DripBusdLp","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"DripVaultAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MarketingAndDevelopmentAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PancakeSwapRouter","outputs":[{"internalType":"contract IUniswapV2Router01","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PancakeSwapRouterAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"SEEDS_TO_GROW_1PLANT","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"ref","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"buySeeds","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"seeds","type":"uint256"}],"name":"calculateSeedSell","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"bnb","type":"uint256"},{"internalType":"uint256","name":"contractBalance","type":"uint256"}],"name":"calculateSeedsBuy","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"bnb","type":"uint256"}],"name":"calculateSeedsBuySimple","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"bnb","type":"uint256"}],"name":"calculateSeedsBuySimpleBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"bnb","type":"uint256"}],"name":"calculateSeedsBuySimpleTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"bnb","type":"uint256"}],"name":"calculateSeedsBuySimpleTotal","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"bnb","type":"uint256"},{"internalType":"uint256","name":"contractBalance","type":"uint256"}],"name":"calculateSeedsBuyTotal","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"rt","type":"uint256"},{"internalType":"uint256","name":"rs","type":"uint256"},{"internalType":"uint256","name":"bs","type":"uint256"}],"name":"calculateTrade","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"claimedSeeds","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"currentBalanceMultiplier","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"currentTimeMultiplier","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"devFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getMyPlants","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getMySeeds","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"adr","type":"address"}],"name":"getSeedsSinceLastPlant","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_user","type":"address"}],"name":"getUserSeeds","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"hatcheryPlants","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"initialized","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"lastPlant","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"marketSeeds","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"ref","type":"address"}],"name":"plantSeeds","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"referrals","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"seedMarket","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"sellSeeds","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_top","type":"uint256"},{"internalType":"uint256","name":"multiplier","type":"uint256"}],"name":"setBalanceMultiplier","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_seed","type":"uint256"}],"name":"setSeedAmount","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"startTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
        # let's also connect to the wallet and make sure web3 works
        self.contract = self.web3.eth.contract(address=self.drip_garden, abi=self.drip_garden_abi)
        acct_balance = self.web3.eth.get_balance(self.wallet_address)
        # fix POA chain issue
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        print(f"Wallet connected and BNB balance of your wallet is {self.web3.fromWei(acct_balance, 'ether')}")

    def calculate_schedule(self):
        """
        figure out harvest schedule
        :return: tuple of (seconds to next harvest, list of harvesting schedule as of now assuming none is harvested)
        """
        user_plants = self.contract.functions.hatcheryPlants(self.wallet_address).call()
        seeds_to_grow_1plant = self.contract.functions.SEEDS_TO_GROW_1PLANT().call()

        # 1 seed per second :)
        seeds_per_day_per_plant = 86400
        # seeds required for the next plant
        seeds_per_second = user_plants * seeds_per_day_per_plant / 86400
        seconds_to_grow_1plant_this_user = seeds_to_grow_1plant / seeds_per_second
        user_seeds = self.contract.functions.getUserSeeds(self.wallet_address).call()
        seeds_left = user_seeds % seeds_to_grow_1plant
        plants_ready = user_seeds / seeds_to_grow_1plant
        seconds_to_next_plant = (seeds_to_grow_1plant - seeds_left) / seeds_per_second

        # build a harvest schedule
        base = datetime.now()
        harvest_schedule = np.array(
            [base + timedelta(seconds=seconds_to_next_plant) + i * timedelta(seconds=seconds_to_grow_1plant_this_user)
            for i in range(10)])

        print(f"You have {user_plants} plants and {user_seeds} seeds ... Your next harvest is {harvest_schedule[0]}")
        return seconds_to_next_plant, harvest_schedule

    def plant_seeds(self):
        """
        Send transaction to drip garden to compound. If there is anything run calling drip garden contract, it will throw
        exception and the program should terminate.
        Don't call this function until your plant is ready for harvest. Otherwise, you will lose seeds and transaction fee!!!
        :return:
        """
        print("Trying to plant seeds (compound) ...")
        nonce = self.web3.eth.getTransactionCount(self.wallet_address)

        try:
            # Not sure how to set gas. So use 100000 which means it could be 0.0005 BNB (about $0.2).
            # BSC chain has not implemented BEP95 (which is similar to EIP-1559) yet???
            compound_seed_tx = self.contract.functions.plantSeeds(self.ref_address).buildTransaction({
                'chainId': 56,
                'nonce': nonce,
                'from': self.wallet_address,
                'gas': 100000,
                'gasPrice': self.web3.toWei('5', 'gwei'),
            })
            print("### transaction built and ready to send")
            signed_txn = self.web3.eth.account.signTransaction(compound_seed_tx, private_key=self.private_key)
            txn_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            print(f"### transaction {txn_hash} signed and sent")
            # wait for 5 minutes for transaction. Hopefully the gas is set correctly so 5 minutes is enough
            receipt = self.web3.eth.wait_for_transaction_receipt(txn_hash, timeout=300)
            print(f"### transaction confirmed at block {receipt['blockNumber']}. tx = {receipt['transactionHash']}")
            print(f"### Total gas used = {receipt['gasUsed']}")
        except Exception as err:
            # print out error and exit
            print(err)
            raise err

    def run(self):
        """
        endless loop to sleep and plant seeds
        :return:
        """
        while True:
            seconds_to_harvest, _ = self.calculate_schedule()
            print("Sleeping til harvest ...")
            # sleep til harvest time. Add 10 extra seconds to avoid wasting seeds.
            time.sleep(seconds_to_harvest + 10)
            # compound
            self.plant_seeds()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Drip Garden auto seed planter',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=textwrap.dedent('''\
                                        Examples:
                                            python DripGardenCompounder.py --gencfg ./drip_garden.json
                                            python DripGardenCompounder.py --gencfg c:\\temp\\drip_garden.json
                                            python DripGardenCompounder.py --config c:\\temp\\drip_garden.json --schedule
                                            python DripGardenCompounder.py --config c:\\temp\\drip_garden.json --run
                                            python DripGardenCompounder.py --config ./drip_garden.json --schedule
                                            python DripGardenCompounder.py --config ./drip_garden.json --run
                                            python DripGardenCompounder.py --run
                                            python DripGardenCompounder.py --schedule
                                        
                                        This program is meant to automate the compounding process without watching the website. Use at your own risk!!! 
                                        But if you like the program, use my wallet 0x5663c124602C97F9eA6fedBdbDDb7d2c0991bb2f as referral for DRIP or Animal
                                        Farm. Or send me small donation :)
                                        '''))
    parser.add_argument('--gencfg', type=str, help="generate template json config file with specified path. Run this option first before running other commands")
    parser.add_argument('--config', type=str, help='specify config file with path. If not specified, the default is drip_garden.json in current directory')
    parser.add_argument('--schedule', action='store_true', help='print out harvest schedule')
    parser.add_argument('--run', action='store_true', help='auto compound')
    args = parser.parse_args()
    if args.gencfg:
        # generate config file
        config = { "wallet_address": "YOUR_WALLET_ADDRESS",
	               "referral_address": "",
	               "key": "YOUR_PRIVATE_KEY"}
        with open(args.gencfg, 'w') as outfile:
            json.dump(config, outfile)
        print(f"{args.gencfg} file successfully created. Please use any text editor and change the entries in the file.               ")
        print("Step 1. Change YOUR_WALLET_ADDRESS to your wallet address.                                                             ")
        print("Step 2. Change \"\" for referral address to the referral address you used. If you don't have referral, skip.           ")
        print("Step 3. Change YOUR_PRIVATE_KEY to your private key exported from your wallet. Should be a string of 64 hex characters.")
        print("        and please append with 0x in front of the private key in the json file.                                        ")
        print("        See also https://metamask.zendesk.com/hc/en-us/articles/360015289632-How-to-Export-an-Account-Private-Key      ")
        print("                                                                                                                       ")
        print("After editing, your config json file should look like the following")
        print('{"wallet_address": "0xabc23....", "referral_address": "", "key": "0xc3df..."}')
        print()
        print("******************************************** IMPORTANT!!! *************************************************************")
        print("Please don't put this json config file in public directory and don't share this file with others!!! ")
        print("This file has your private key. This is the same as your seed phrase. Please guard it!!!")
        print()
    else:
        if args.config:
            config_file = args.config
        else:
            config_file = "./drip_garden.json"

        if args.schedule:
            compounder = DripGardenCompounder(config_file)
            # only print schedule
            seconds_to_harvest, schedule = compounder.calculate_schedule()
            for i in range(len(schedule)):
                print(i + 1, ":", schedule[i])
        elif args.run:
            compounder = DripGardenCompounder(config_file)
            # full run
            compounder.run()
        else:
            parser.print_help()

