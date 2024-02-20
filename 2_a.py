def calculate_min_moves(machines):
    total_dresses = sum(machines)
    n = len(machines)
    
    if total_dresses % n != 0:
        return -1  # Equal distribution not possible
    
    average = total_dresses // n
    moves = 0
    balance = 0  # Represents the running total of adjustments needed to equalize to the average
    
    for dresses in machines:
        # The difference between the current machine's dresses and the average
        diff = dresses - average
        # Update balance to include the current difference
        balance += diff
        # The absolute value of balance is added to moves; it represents the necessary adjustments (moves) to equalize up to this machine
        moves += abs(balance)
    
    return moves

if __name__ == "__main__":
    print("Enter the number of dresses in each sewing machine separated by commas (e.g., 2, 1, 3, 0, 2):")
    input_line = input()  # Read the entire line as a single string
    # Split the input string by commas and convert each piece to an integer
    machines = list(map(int, input_line.split(",")))
    
    result = calculate_min_moves(machines)
    print("Minimum number of moves required:", result)
