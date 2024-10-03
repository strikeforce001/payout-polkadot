# Polkadot Validator Unclaimed Rewards Payout Script

This repository contains a Python script to automate claiming unclaimed staking rewards for a Polkadot validator. The script interacts with the Polkadot network and submits a payout transaction for a specific era.

## Prerequisites

Before you begin, make sure you have the following:
- A VPS running Linux (Ubuntu/Debian recommended).
- Python 3.8 or higher installed on your VPS.
- The mnemonic phrase of your validator's controller account.

## Setup Instructions

Follow these steps to set up and run the script on your VPS:

### 1. Connect to your VPS

Connect to your VPS using SSH:

```bash
ssh your_user@your_vps_ip
```
###  2. Install Python (if not installed)

Ensure Python is installed by running the following commands:
```bash
sudo apt update
sudo apt install python3 python3-pip -y
```
Verify the installation:
```bash
python3 --version
pip3 --version
```

### 3. Create a Project Directory
Create a directory for your project:
```bash
mkdir polkadot-validator-rewards
cd polkadot-validator-rewards
```

### 4. (Optional) Set Up a Virtual Environment

Set up a virtual environment to isolate dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 5. Install Required Dependencies

Install the necessary Python libraries:
```bash
pip3 install substrate-interface
```

### 6. Create the Python Script

Create a new Python script file named claim_rewards.py:
```bash
nano claim_rewards.py
```

Paste the following Python code into the file:
```bash
from substrateinterface import SubstrateInterface, Keypair
from substrateinterface.exceptions import SubstrateRequestException

# Connect to a Polkadot node
substrate = SubstrateInterface(
    url="wss://rpc.polkadot.io",  # URL of the public Polkadot node
    type_registry_preset='polkadot'
)

# Controller account keypair (replace with your mnemonic phrase)
keypair = Keypair.create_from_mnemonic("your mnemonic phrase here")

def claim_unclaimed_rewards(era_index):
    try:
        # Create a payout transaction for the staking rewards
        call = substrate.compose_call(
            call_module='Staking',
            call_function='payout_stakers',
            call_params={
                'validator_stash': keypair.ss58_address,  # Your Stash address
                'era': era_index  # The era for which you want to claim rewards
            }
        )

        # Create a signed extrinsic
        extrinsic = substrate.create_signed_extrinsic(
            call=call,
            keypair=keypair
        )

        # Submit the transaction
        receipt = substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)

        # Check transaction status
        if receipt.is_success:
            print(f"Payout successful for era {era_index}!")
        else:
            print(f"Payout failed for era {era_index}. Error: {receipt.error_message}")

    except SubstrateRequestException as e:
        print(f"Error during payout transaction: {e}")

# Example usage: claim rewards for a specific era (replace with actual era index)
era_index = 1234  # Replace with the correct era index
claim_unclaimed_rewards(era_index)
```

Replace your mnemonic phrase here with the mnemonic phrase of your controller account.

Save and exit the editor (CTRL+X, then Y, then Enter).

### 7. Run the Script

You can manually run the script using:
```bash
python3 claim_rewards.py
```

### 8. (Optional) Automate the Script with Cron

You can automate the script by setting up a cron job to run it regularly. For example, to run the script every day at midnight:

	1.	Open the cron configuration:
```bash
crontab -e
```

  2.	Add the following line to run the script daily at midnight:
```bash
0 0 * * * /usr/bin/python3 /path/to/your/script/claim_rewards.py >> /path/to/your/logfile.log 2>&1
```

Replace /path/to/your/script/claim_rewards.py with the full path to your script, and /path/to/your/logfile.log with the path to your log file.

### 9. Monitor Logs
You can check the log file to monitor the status of the script:
```bash
tail -f /path/to/your/logfile.log
```

