def min_cost(costs):
    if not costs:
        return 0

    n = len(costs)  # Number of venues
    k = len(costs[0])  # Number of themes

    # Initialize the DP table
    dp = [[0] * k for _ in range(n)]
    dp[0] = costs[0]  # Base case: first row

    # Fill the DP table
    for i in range(1, n):
        for j in range(k):
            # Find the minimum cost of decorating the (i-1)-th venue with a different theme
            min_cost = float('inf')
            for l in range(k):
                if l != j:
                    min_cost = min(min_cost, dp[i - 1][l])
            dp[i][j] = costs[i][j] + min_cost

    # Find the minimum cost to decorate all venues
    return min(dp[-1])


# Example usage
costs = [[1, 3, 2], [4, 6, 8], [3, 1, 5]]
print(min_cost(costs))