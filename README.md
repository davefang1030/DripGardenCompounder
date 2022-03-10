# Drip Garden Compounder
Automated scripts to compound drip garden without losing seeds. #DRIP #AnimalFarm #crypto

<!-- ABOUT THE PROJECT -->
## About The Project

I needed an automated tool to compound without needing to check the schedule on [the animal farm website](theanimal.farm/garden), setting timer on my phone and click
the button when it is ready. So here it is. Enjoy and use at your own risk.<br>

<p align="right">(<a href="#top">back to top</a>)</p>

## Installation

_The code is written in python so you just need to install python and a couple packages required._

1. Dowmload and install python if you don't have python installed from [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Install required packages if needed
   ```sh
   pip install web3
   pip install
   ```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

To use the tool, first we need to set up configuration file which includes your wallet address, referral address you used, and private key. Use the following command to generate a template configure file.
   ```sh
   python DripGardenCompounder.py --gencfg ./drip_garden.json
   ```
Now use your favoriate text editor to modify the json file generated.
<li> Change YOUR_WALLET_ADDRESS to your wallet address.</li>
<li> Change "" with referral address to the referral address you used. If you don't have referral, skip.</li>
<li> Change YOUR_PRIVATE_KEY to your private key exported from your wallet. Should be a string of 64 hex characters.</li> 
<br>
To get private key for your wallet, go to [metamask faq](https://metamask.zendesk.com/hc/en-us/articles/360015289632-How-to-Export-an-Account-Private-Key'>). Becuase the config file contains private key, please don't put file
in public drive or public computer. <b>Guard this file!!!</b> The finished json file should look like the following:
<br>
<pre>
{"wallet_address": "0x143Ad...", "referral_address": "", "key": "0xabcd8..."}
</pre>

To just see your harvest schedule, run the following
   ```sh
   python DripGardenCompounder.py --schedule
   ```

To auto compound, run the following. The program will first figure out the time it needs to wait based on schedule, wait til 10 seconds after the harvest time, 
then call plant seeds of the contract to compound. After the call, the program will wait for the next harvest. The program is basically a endless loop unless some sort of
error happens or the user hit Ctrl-C to stop the program.
   ```sh
   python DripGardenCompounder.py --run
   ```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Project Link: [https://github.com/davefang1030/DripGardenCompounder](https://github.com/davefang1030/DripGardenCompounder)

<p align="right">(<a href="#top">back to top</a>)</p>
