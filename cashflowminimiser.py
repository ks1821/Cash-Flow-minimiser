def minimize_cash_flow(transactions):
    # Create a dictionary to track the net cash flow for each entity
    balance = {}

    # Calculate net cash flow for each entity
    for from_entity, to_entity, amount in transactions:
        # If the entity doesn't exist in the balance dictionary, create it with a balance of 0
        balance.setdefault(from_entity, 0)
        balance.setdefault(to_entity, 0)

        # Update the balances for both sender and receiver
        balance[from_entity] -= amount
        balance[to_entity] += amount

    # Initialize a list to store transactions needed to balance cash flows
    transactions_needed = []

    # Process entities with negative cash flow (debt)
    for entity, cash_flow in balance.items():
        if cash_flow < 0:
            # Find entities with positive cash flow (creditors) to balance the cash flow
            creditors = [e for e, cf in balance.items() if cf > 0]
            while cash_flow < 0:
                # Find the creditor with the maximum balance
                creditor = max(creditors, key=lambda x: balance[x])
                # Calculate the amount to transfer
                transfer_amount = min(-cash_flow, balance[creditor])
                # Record the transaction
                transactions_needed.append((creditor, entity, transfer_amount))
                # Update balances
                balance[creditor] -= transfer_amount
                balance[entity] += transfer_amount
                # Remove the creditor from the list if their balance reaches zero
                if balance[creditor] == 0:
                    creditors.remove(creditor)

    return transactions_needed

if __name__ == "__main__":
    # Define cash flow transactions as (from_entity, to_entity, amount)
    transactions = [
        ('A', 'B', 10),
        ('B', 'A', 5),
        ('C', 'A', 15),
        ('B', 'C', 10),
        ('C', 'B', 5),
    ]

    transactions_needed = minimize_cash_flow(transactions)

    print("Minimum Cash Flow Transactions:")
    for transaction in transactions_needed:
        print(f"Transfer {transaction[2]} from {transaction[0]} to {transaction[1]}")
