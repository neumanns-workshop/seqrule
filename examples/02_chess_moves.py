"""
Example 02: Chess Move Validation
===============================

This example demonstrates how to use seqrule to validate chess moves,
enforcing rules like:
- Legal piece movements
- Board boundaries
- Capture rules
- Basic piece-specific rules (knight moves, pawn direction)
"""


from seqrule import Object, RuleBuilder, set_logging_level

# Disable debug logging
set_logging_level("WARNING")

def create_position(square: str, name: str = None, **properties) -> Object:
    """Create a chess position object from algebraic notation (e.g. 'e4')."""
    file = square[0]
    rank = int(square[1])

    position = {
        'file': file,
        'rank': rank,
        'file_num': ord(file) - ord('a') + 1,  # Convert a-h to 1-8
        'square': square,
        **properties
    }
    return Object(name or square, **position)

def check_knight_move(obj, context):
    """Verify if move follows knight's L-shaped pattern."""
    prev = context['prev']
    if prev is None:
        return True

    # Calculate the difference in ranks and files
    rank_diff = abs(obj.get('rank') - prev.get('rank'))
    file_diff = abs(obj.get('file_num') - prev.get('file_num'))

    # Knight moves 2 squares in one direction and 1 in the other
    valid_move = (rank_diff == 2 and file_diff == 1) or (rank_diff == 1 and file_diff == 2)
    if not valid_move:
        print(f"Invalid knight move from {prev.get('square')} to {obj.get('square')}")
    return valid_move

def check_bishop_move(obj, context):
    """Verify if move follows bishop's diagonal pattern."""
    prev = context['prev']
    if prev is None:
        return True

    # Calculate the difference in ranks and files
    rank_diff = abs(obj.get('rank') - prev.get('rank'))
    file_diff = abs(obj.get('file_num') - prev.get('file_num'))

    # Bishop moves must have equal rank and file differences (diagonal)
    valid_move = rank_diff == file_diff
    if not valid_move:
        print(f"Invalid bishop move from {prev.get('square')} to {obj.get('square')}")
    return valid_move

def check_rook_move(obj, context):
    """Verify if move follows rook's straight line pattern."""
    prev = context['prev']
    if prev is None:
        return True

    # Calculate the difference in ranks and files
    rank_diff = abs(obj.get('rank') - prev.get('rank'))
    file_diff = abs(obj.get('file_num') - prev.get('file_num'))

    # Rook moves must be either horizontal (same rank) or vertical (same file)
    valid_move = rank_diff == 0 or file_diff == 0
    if not valid_move:
        print(f"Invalid rook move from {prev.get('square')} to {obj.get('square')}")
    return valid_move

def check_pawn_advance(obj, context):
    """Verify if pawn move follows correct direction and distance."""
    prev = context['prev']
    if prev is None:
        return True

    # Get move properties
    rank_diff = obj.get('rank') - prev.get('rank')
    file_diff = abs(obj.get('file_num') - prev.get('file_num'))
    is_white = prev.get('color') == 'white'
    start_rank = 2 if is_white else 7

    # Pawns can move 2 squares from starting position
    if prev.get('rank') == start_rank and file_diff == 0:
        valid_move = rank_diff == (2 if is_white else -2)
    # Otherwise, pawns move 1 square forward
    else:
        valid_move = rank_diff == (1 if is_white else -1) and file_diff == 0

    if not valid_move:
        print(f"Invalid pawn move from {prev.get('square')} to {obj.get('square')}")
    return valid_move

def test_knight_moves():
    """Test knight move validation."""
    print("\nTesting Knight Moves...")

    # Create a rule for knight movement
    knight_rule = RuleBuilder()\
        .add_condition("square", check_knight_move, None)\
        .set_sequence(['start', 'end'])\
        .build()

    # Test valid knight moves
    valid_moves = [
        create_position('e4', name='start'),  # Starting position
        create_position('f6', name='end')     # Valid L-shape move
    ]

    invalid_moves = [
        create_position('e4', name='start'),
        create_position('e6', name='end')     # Invalid - straight line
    ]

    result = knight_rule.evaluate(valid_moves)
    print(f"Valid knight move (e4-f6): {result[0]}")

    result = knight_rule.evaluate(invalid_moves)
    print(f"Invalid knight move (e4-e6): {result[0]}")

def test_pawn_moves():
    """Test pawn move validation."""
    print("\nTesting Pawn Moves...")

    # Create a rule for pawn movement
    pawn_rule = RuleBuilder()\
        .add_condition("square", check_pawn_advance, None)\
        .set_sequence(['start', 'end'])\
        .build()

    # Test valid pawn moves
    valid_moves = [
        create_position('e2', name='start', color='white'),  # Starting position
        create_position('e4', name='end')                    # Valid 2-square advance
    ]

    invalid_moves = [
        create_position('e3', name='start', color='white'),  # Not on starting rank
        create_position('e5', name='end')                    # Invalid 2-square advance
    ]

    result = pawn_rule.evaluate(valid_moves)
    print(f"Valid pawn move (e2-e4): {result[0]}")

    result = pawn_rule.evaluate(invalid_moves)
    print(f"Invalid pawn move (e3-e5): {result[0]}")

def test_bishop_moves():
    """Test bishop move validation."""
    print("\nTesting Bishop Moves...")

    # Create a rule for bishop movement
    bishop_rule = RuleBuilder()\
        .add_condition("square", check_bishop_move, None)\
        .set_sequence(['start', 'end'])\
        .build()

    # Test valid bishop moves
    valid_moves = [
        create_position('c1', name='start'),
        create_position('f4', name='end')   # Valid diagonal
    ]

    invalid_moves = [
        create_position('c1', name='start'),
        create_position('c4', name='end')   # Invalid - straight line
    ]

    result = bishop_rule.evaluate(valid_moves)
    print(f"Valid bishop move (c1-f4): {result[0]}")

    result = bishop_rule.evaluate(invalid_moves)
    print(f"Invalid bishop move (c1-c4): {result[0]}")

def check_piece_type(obj, context):
    """Verify if the piece matches the expected type."""
    expected_type = context.get('expected_type')
    if not expected_type:
        return True
    piece_type = obj.get('piece_type')
    if piece_type != expected_type:
        print(f"Expected {expected_type} at {obj.get('square')}, got {piece_type}")
    return piece_type == expected_type

def check_move(obj, context):
    """Check if the move is valid based on piece type."""
    prev = context['prev']
    if prev is None:
        return True

    # Only check moves between start and end positions of the same piece
    curr_name = obj.name
    prev_name = prev.name

    # Skip if not checking a move (e.g., start to end position)
    if not (curr_name.endswith('_end') and prev_name == curr_name[:-4]):
        return True

    piece_type = prev.get('piece_type')
    if piece_type == 'pawn':
        return check_pawn_advance(obj, context)
    elif piece_type == 'knight':
        return check_knight_move(obj, context)
    elif piece_type == 'bishop':
        return check_bishop_move(obj, context)
    elif piece_type == 'rook':
        return check_rook_move(obj, context)
    elif piece_type == 'queen':
        return check_queen_move(obj, context)
    else:
        print(f"Unknown piece type: {piece_type}")
        return False

def test_scholars_mate():
    """Test Scholar's Mate sequence validation."""
    print("\nTesting Scholar's Mate...")

    # Scholar's Mate sequence:
    # 1. e4 e5
    # 2. Bc4 Nc6
    # 3. Qh5 Nf6??
    # 4. Qxf7#

    scholars_mate = [
        create_position('e2', name='w_pawn1', piece_type='pawn', color='white'),
        create_position('e4', name='w_pawn1_end', piece_type='pawn', color='white'),
        create_position('e7', name='b_pawn1', piece_type='pawn', color='black'),
        create_position('e5', name='b_pawn1_end', piece_type='pawn', color='black'),
        create_position('f1', name='w_bishop', piece_type='bishop', color='white'),
        create_position('c4', name='w_bishop_end', piece_type='bishop', color='white'),
        create_position('b8', name='b_knight', piece_type='knight', color='black'),
        create_position('c6', name='b_knight_end', piece_type='knight', color='black'),
        create_position('d1', name='w_queen', piece_type='queen', color='white'),
        create_position('h5', name='w_queen_end', piece_type='queen', color='white'),
        create_position('g8', name='b_knight2', piece_type='knight', color='black'),
        create_position('f6', name='b_knight2_end', piece_type='knight', color='black'),
        create_position('h5', name='w_queen2', piece_type='queen', color='white'),
        create_position(
            'f7',
            name='w_queen2_end',
            piece_type='queen',
            color='white',
            is_capture=True
        )
    ]

    # Create a rule that validates the entire Scholar's Mate sequence
    scholars_rule = RuleBuilder()\
        .add_condition('square', check_move, None)\
        .add_condition('piece_type', check_piece_type, 'expected_type')\
        .set_sequence([pos.name for pos in scholars_mate])\
        .build()

    result = scholars_rule.evaluate(scholars_mate)
    print(f"Scholar's Mate sequence valid: {result[0]}")

def check_queen_move(obj, context):
    """Verify if move follows queen's movement pattern (diagonal or straight)."""
    prev = context['prev']
    if prev is None:
        return True

    # Queen combines bishop and rook movement
    diagonal = check_bishop_move(obj, context)
    straight = check_rook_move(obj, context)

    valid_move = diagonal or straight
    if not valid_move:
        print(f"Invalid queen move from {prev.get('square')} to {obj.get('square')}")
    return valid_move

def test_ruy_lopez():
    """Test Ruy Lopez opening sequence validation."""
    print("\nTesting Ruy Lopez Opening...")

    # Ruy Lopez sequence:
    # 1. e4 e5
    # 2. Nf3 Nc6
    # 3. Bb5

    ruy_lopez = [
        create_position('e2', name='w_pawn1', piece_type='pawn', color='white'),
        create_position('e4', name='w_pawn1_end', piece_type='pawn', color='white'),
        create_position('e7', name='b_pawn1', piece_type='pawn', color='black'),
        create_position('e5', name='b_pawn1_end', piece_type='pawn', color='black'),
        create_position('g1', name='w_knight', piece_type='knight', color='white'),
        create_position('f3', name='w_knight_end', piece_type='knight', color='white'),
        create_position('b8', name='b_knight', piece_type='knight', color='black'),
        create_position('c6', name='b_knight_end', piece_type='knight', color='black'),
        create_position('f1', name='w_bishop', piece_type='bishop', color='white'),
        create_position('b5', name='w_bishop_end', piece_type='bishop', color='white')
    ]

    # Create a rule that validates the Ruy Lopez sequence
    ruy_lopez_rule = RuleBuilder()\
        .add_condition('square', check_move, None)\
        .add_condition('piece_type', check_piece_type, 'expected_type')\
        .set_sequence([pos.name for pos in ruy_lopez])\
        .build()

    result = ruy_lopez_rule.evaluate(ruy_lopez)
    print(f"Ruy Lopez sequence valid: {result[0]}")

if __name__ == "__main__":
    print("Chess Move Validation Example")
    print("============================")
    test_knight_moves()
    test_pawn_moves()
    test_bishop_moves()
    test_scholars_mate()
    test_ruy_lopez()
