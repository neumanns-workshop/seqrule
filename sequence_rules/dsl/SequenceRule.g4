grammar SequenceRule;

// Parser Rules
rule
    : sequence                                    # SimpleRule
    | IF condition THEN sequence (ELSE sequence)? # ConditionalRule
    ;

sequence
    : element (COMMA element)*                    # CommaSequence
    | element ARROW element                       # ArrowSequence
    | element (element)*                         # SpaceSequence
    ;

element
    : IDENTIFIER                                  # SimpleElement
    | IDENTIFIER LPAREN condition RPAREN          # ConstrainedElement
    | IDENTIFIER AT number                        # PosElement
    ;

number
    : NUMBER                                      # SignedNumber
    ;

condition
    : expression                                # SingleCondition
    | LPAREN condition RPAREN                   # ParenCondition
    | condition AND condition                   # AndCondition
    | condition OR condition                    # OrCondition
    ;

expression
    : property relOp value                      # ComparisonExpression
    ;

property
    : IDENTIFIER (AT number)?
    ;

relOp
    : EQ | NEQ | LT | GT | LTE | GTE
    ;

value
    : number                                    # NumericValue
    | BOOLEAN                                   # BooleanValue
    | STRING                                    # StringValue
    | property                                  # PropertyValue
    ;

// Lexer Rules
NUMBER: [0-9]+;
COMMA: ',';
IF: 'if';
THEN: 'then';
ELSE: 'else';
AND: 'and';
OR: 'or';
AT: '@';
ARROW: '->';
STRING: '"' (~["\r\n])* '"';
IDENTIFIER: [a-zA-Z_][a-zA-Z0-9_]*;
LPAREN: '(';
RPAREN: ')';
EQ: '=';
NEQ: '!=';
LT: '<';
GT: '>';
LTE: '<=';
GTE: '>=';
BOOLEAN: 'true' | 'false';
WS: [ \t\r\n]+ -> skip;

// Fragment rules for better error reporting
fragment DIGIT: [0-9];
fragment LETTER: [a-zA-Z];
fragment QUOTE: '"'; 