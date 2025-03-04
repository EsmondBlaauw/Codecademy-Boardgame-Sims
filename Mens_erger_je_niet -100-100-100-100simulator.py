
import random
# Initialize positions for pawns of players A, B, C, D, starting at -100
pawn_positions = {
    'A': [-100, -100, -100, -100],
    'B': [-100, -100, -100, -100],
    'C': [-100, -100, -100, -100],
    'D': [-100, -100, -100, -100]
}
there_is_a_winner = False


# Die throw function (1-6)
def die_throw():
    input("Press Enter to roll the die...")
    result = random.randint(1, 6)
    print(f"Die rolled: {result}")
    return result


 # Check if a given position is occupied by an opponent's pawn
def check_for_hits(player, position):
    for opponent, pawns in pawn_positions.items():
        if opponent != player:
            for i in range(len(pawns)):
                if pawns[i] == position and position < 41:
                    print(f"Player {player}'s pawn hits Player {opponent}'s pawn at position {position}")
                    pawns[i] = -100  # Send opponent's pawn back to start


# Check if a pawn has reached or exceeded the finishing point
def check_for_finishing_point(position):
    if position > 44:
        return 44  # Cap at the last finishing position
    return position



# Display the current game state
def display_game_state():
    print("\nCurrent game state:")
    for player, pawns in pawn_positions.items():
        print(f"Player {player}: {pawns}")
# Move a pawn based on die roll, apply hit checks and finishing checks
def move_pawn(player, pawn_index, roll):
    current_position = pawn_positions[player][pawn_index]
    if current_position == 44:
        print(f"Player {player}'s pawn {pawn_index + 1} has already finished.")
        return False  # Pawn has finished, do not move it
    if current_position == -100:
        if roll == 6:
            print(f"Player {player} moves pawn {pawn_index + 1} onto the board at position 0.")
            pawn_positions[player][pawn_index] = 0
            return True
        else:
            print(f"Player {player} cannot move pawn {pawn_index + 1} onto the board without rolling a 6.")
            return False
    else:
        new_position = current_position + roll
        new_position = check_for_finishing_point(new_position)
        check_for_hits(player, new_position)
        pawn_positions[player][pawn_index] = new_position
        print(f"Player {player}'s pawn {pawn_index + 1} moves to position {new_position}")
        return True



# Player's turn with interactive input
def player_turn(player):
    global there_is_a_winner
    extra_turn = True
    while extra_turn:
        print(f"\n--- Player {player}'s Turn ---")
        display_game_state()
        roll = die_throw()
        extra_turn = (roll == 6)
        print(f"Player {player} rolled a {roll}")
        # Get list of movable pawns
        movable_pawns = []
        for i in range(4):
            pos = pawn_positions[player][i]
            if pos == -100 and roll == 6:
                movable_pawns.append(i)
            elif pos != -100 and pos != 44:
                movable_pawns.append(i)
        if not movable_pawns:
            print(f"No pawns can be moved for Player {player}.")
            continue
        # Ask player which pawn to move
        while True:
            try:
                pawn_choice = int(input(f"Player {player}, choose a pawn to move { [i+1 for i in movable_pawns] }: ")) - 1
                if pawn_choice in movable_pawns:
                    moved = move_pawn(player, pawn_choice, roll)
                    break
                else:
                    print("Invalid pawn choice. Please choose a movable pawn.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        # Check for win condition
        if all(p == 44 for p in pawn_positions[player]):
            print(f"\nGame Over - Player {player} is the winner!")
            there_is_a_winner = True
            return
        # If the player rolled a 6 and moved a pawn, they get another turn
        if extra_turn:
            print(f"Player {player} rolled a 6 and gets another turn.")



# Main game loop
def main():
    print("Welcome to 'Mens Erger Je Niet' simulator with simplified rules")
    print("Extra throwing after a 6 is allowed until you do not roll a 6.")
    print("Pawns cannot move beyond the last finishing position.")
    players = ['A', 'B', 'C', 'D']
    current_player_index = 0
    while not there_is_a_winner:
        player = players[current_player_index]
        player_turn(player)
        if there_is_a_winner:
            break
        current_player_index = (current_player_index + 1) % len(players)
if __name__ == "__main__":
    main()
