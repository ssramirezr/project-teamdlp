from collections import defaultdict

def firstFunction(grammar): # Find First of non terminals function
    first = defaultdict(set) # 'first' is a dictionary with non-terminals as keys and their productions as values
    calculated = set()  # Set to store calculated First sets

    def first_symbol(symbol): # Internal function with a non terminal symbol as parameter
        if symbol not in grammar:  # If it's a terminal
            return {symbol}

        if symbol in calculated:  # If already calculated
            return first[symbol]

        calculated.add(symbol)  # Mark as calculated

        for production in grammar[symbol]:
            if production == 'e':  # Empty production
                first[symbol].add('e')
            else:
                for prod_symbol in production: # For each character in the production
                    prod_first = first_symbol(prod_symbol) # Recursive call
                    first[symbol].update(prod_first - {'e'}) # Add the terminals to the list of first of the symbol
                    if 'e' not in prod_first:
                        break
                else:
                    first[symbol].add('e')
        
        return first[symbol]

    for non_terminal in grammar: # For each non terminal, call first_symbol()
        first_symbol(non_terminal)
    
    return first


def followFunction(grammar, first): # Find Follow of non terminals function
    follow = defaultdict(set)
    calculated = set()  # Set to store calculated Follow sets

    def follow_of(symbol): # Internal function 
        if symbol in calculated:  # If already calculated
            return follow[symbol]

        calculated.add(symbol)  # Mark as calculated
        
        # Rule 1: Add '$' to Follow of 'S'
        start_symbol = next(iter(grammar))  # Grab the first one
        follow[start_symbol].add('$')

        for non_terminal, productions in grammar.items(): # We take non_terminal as the key and productions as the set of productions in the given grammar
            for production in productions: # For every prodcution in productions
                if symbol in production: # For every symbol in the production
                    position = production.index(symbol) # We find the position to satisfy the second rule
                    # Regla 2: If there is a production A → αBβ, then add First(β) \ {ε} to Follow(B)
                    if position < len(production) - 1: # Verify that there is characters after the non terminal
                        beta = production[position + 1:] # Take that characters
                        for prod_symbol in beta: # For every symbol in that string
                            if prod_symbol in grammar: # If the symbol is a non terminal 
                                prod_first = first[prod_symbol] # We can find the first in the 'first' dictionary
                            else: # If the symbol is a terminal
                                prod_first = {prod_symbol} # The first is itself
                            follow[symbol].update(prod_first - {'e'}) 
                            if 'e' not in prod_first:
                                break
                        else: 
                            # Regla 3: If there is a production A → αB, or A → αBβ with ε ∈ First(β), then add Follow(A) to Follow(B)
                            follow[symbol].update(follow_of(non_terminal))
                    else: # If there is nothing next to the non terminal
                        # Regla 3: If there is a production A → αB, then add Follow(A) to Follow(B)
                        follow[symbol].update(follow_of(non_terminal))

        return follow[symbol]

    # Find the follow for each non terminal symbol
    for non_terminal in grammar:
        follow_of(non_terminal)

    return follow


# Function to read grammars and convert them into dictionaries
def read_grammars():
    num_cases = int(input().strip())  # Number of test cases
    grammars = []  # List to store the grammars

    for _ in range(num_cases):
        num_nonterminals = int(input().strip())  # Number of non-terminals in the grammar
        grammar = defaultdict(list)  # Dictionary to store the grammar
        
        # Iterate over each non-terminal
        for _ in range(num_nonterminals):
            line = input().strip().split()  # Read non-terminal and its productions
            non_terminal = line[0]  # Extract non-terminal
            productions = line[1:]  # Extract productions
            # Separate alternative productions
            for production in productions:
                grammar[non_terminal].append(production)
        
        grammars.append(grammar)  # Add the grammar to the list of grammars
    
    return grammars

def main():
    # Read grammars
    grammars = read_grammars()

    # Process each grammar and display the FIRST and FOLLOW sets
    for i, grammar in enumerate(grammars):
        
        # Calculate and display the FIRST sets
        first_sets = firstFunction(grammar)
        for non_terminal, first in sorted(first_sets.items()):
            print(f"FIRST({non_terminal}) = {{ {', '.join(sorted(first))} }}")
        
        # Calculate and display the FOLLOW sets
        follow_sets = followFunction(grammar, first_sets)
        for non_terminal, follow in sorted(follow_sets.items()):
            print(f"FOLLOW({non_terminal}) = {{ {', '.join(sorted(follow))} }}")

main()
