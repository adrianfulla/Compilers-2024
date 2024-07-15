grammar MiniLang;

prog:   stat+ ;

stat:   expr NEWLINE                                                    # printExpr
    |   ID '=' expr NEWLINE                                             # assign
    |   'if' expr 'then' block ('else' block)? 'endif'                    # ifElse
    |   'while' expr 'do' block 'endwhile'                                # whileLoop
    |   NEWLINE                                                          # blank
    ;

block:  (stat | NEWLINE)*;

expr:   expr ('==' | '!=' | '<' | '>' | '<=' | '>=') expr   # Compare
    |   expr ('*'|'/') expr                                 # MulDiv
    |   expr ('+'|'-') expr                                 # AddSub
    |   INT                                                 # int
    |   STRING                                              # string
    |   ID                                                  # id
    |   '(' expr ')'                                        # parens
    ;

EQ:     '==';
NEQ:    '!=';
LT:     '<';
GT:     '>';
LE:     '<=';
GE:     '>=';
STRING : '"' (~["\r\n])* '"' ;
MUL : '*' ; // define token for multiplication
DIV : '/' ; // define token for division
ADD : '+' ; // define token for addition
SUB : '-' ; // define token for subtraction
ID  : [a-zA-Z]+ ; // match identifiers
INT : [0-9]+ ; // match integers
NEWLINE:'\r'? '\n' ; // return newlines to parser (is end-statement signal)
WS  : [ \t]+ -> skip ; // toss out whitespace