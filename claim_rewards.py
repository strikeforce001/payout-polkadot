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
