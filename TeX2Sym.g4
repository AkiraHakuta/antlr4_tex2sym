// antlr4env.bat
// antlr4py3 -visitor -no-listener -o gen TeX2Sym.g4

grammar TeX2Sym; 

prog:   stat ;

stat:   expr NEWLINE                            # printExpr   
    |   expr EQUAL expr NEWLINE                 # equal
    |   expr op=(LT|GT|LEQQ|GEQQ) expr NEWLINE  # relation
    ;

expr:   FLOAT                                           # float
    |   INT                                             # int
    |   SEQ_TERM L_BRACE expr R_BRACE                   # seqterm
    |   gz=(GAMMAF|ZETAF) expr R_PAREN                  # gammaf_zetaf
    |   FUNCTION expr R_PAREN                           # function
    |   const=(PI|IMAGINARY_UNIT|NAPIER_CONSTANT|INFTY) # mathconst
    |   GREEK                                           # greek
    |   ALPHABET                                        # alphabet  
    |   expr FACTORIAL                                  # factrial
    |   expr CARET  expr                                # power
    |   MINUS expr                                      # MinusExpr
    |   PLUS expr                                       # PlusExpr
    |   expr DIV expr                                   # div
    |   expr MULT expr                                  # mult
    |   expr op=( PLUS | MINUS ) expr                   # AddSub     
    |   expr expr                                       # mull
    |   func=(SQRT|SIN|COS|TAN|LOG)  L_BRACE expr R_BRACE                       # func
    |   func=(SIN|COS|TAN) CARET  L_BRACE expr R_BRACE  L_BRACE expr R_BRACE    # trign
    |   SQRT L_BRACKET expr R_BRACKET L_BRACE expr R_BRACE                      # sqrtn
    |   LOG UB L_BRACE expr R_BRACE L_BRACE expr R_BRACE                        # logub
    |   L_PIPE expr R_PIPE                                                      # abs
    |   DIFF  R_BRACE  L_BRACE dxg=(DX|DGREEK) R_BRACE L_BRACE expr R_BRACE     # diff
    |   L_PAREN DIFF  R_BRACE  L_BRACE dxg=(DX|DGREEK) R_BRACE R_PAREN CARET L_BRACE expr R_BRACE L_BRACE expr R_BRACE              # diffn1
    |   DIFF CARET L_BRACE expr R_BRACE R_BRACE  L_BRACE dxg=(DX|DGREEK) CARET L_BRACE expr R_BRACE R_BRACE  L_BRACE expr R_BRACE   # diffn2
    |   INTEGRATE L_BRACE expr dxg=(DX|DGREEK) R_BRACE                                                                              # integrate
    |   INTEGRATE UB L_BRACE expr R_BRACE CARET L_BRACE expr R_BRACE  L_BRACE expr dxg=(DX|DGREEK) R_BRACE                          # dintegrate
    |   LIM UB L_BRACE expr TO expr R_BRACE L_BRACE expr R_BRACE                                                                    # lim
    |   FRAC L_BRACE expr R_BRACE L_BRACE expr R_BRACE                                                                              # frac
    |   SUM  UB L_BRACE expr EQUAL expr R_BRACE CARET L_BRACE expr R_BRACE L_BRACE expr R_BRACE                                     # sum  
    |   UB L_BRACE expr R_BRACE cp=(COMBI|PERMU) UB L_BRACE expr R_BRACE                                                            # combi_permu
    |   '(' expr ')'                                    # parens
    |   '{' expr '}'                                    # braces    
    ;


GREEK : ('aalpha'|'bbeta'|'ggamma'|'ddelta'|'eepsilon'|'eeta'|'ttheta'|'iiota'|'kkappa'|'llambda'|'mmu'|'nnu'|
                            'xxi'|'pppi'|'rrho'|'ssigma'|'ttau'|'uupsilon'|'pphi'|'cchi'|'ppsi'|'oomega') ; // except zeta, omicron
ALPHABET :   [a-zA-DFGHJ-RT-Z] ;
FLOAT :  [0-9]* '.'[0-9]+ ;
INT :   [0-9]+ ;
NEWLINE:'\r'? '\n' ;     // return newlines to parser (is end-statement signal)
WS  :   [ \t]+ -> skip ; // toss out whitespace

// math constant
PI : '\\ppi';
IMAGINARY_UNIT : '\\ii';
NAPIER_CONSTANT : '\\ee' ;

L_PAREN: '(';
R_PAREN: ')';
L_BRACE: '{';
R_BRACE: '}';
L_BRACKET: '[';
R_BRACKET: ']';  
L_PIPE : '\\left|' ;
R_PIPE : '\\right|' ;
    
MULT :   ('*'|'\\times'|'\\cdot') ;
DIV :     '\\div' ;
PLUS :   '+' ;
MINUS :   '-' ;
CARET : '^';
UB : '_' ;
FACTORIAL : '!' ;

DIFF : '\\frac{d';
INTEGRATE : '\\int' ;
DX : [d][a-z] ;
DGREEK : [d]GREEK ;

SQRT : '\\sqrt' ;
SIN  : '\\sin' ;
COS  : '\\cos' ;
TAN  : '\\tan' ;
LOG  : '\\log' ;

FRAC : '\\frac' ;
SUM : '\\sum' ;
LIM : '\\lim'  ;
TO  : '\\to' ;
INFTY : '\\infty' ;

COMBI : '\\C' ;
PERMU : '\\P' ;
SEQ_TERM : [a-z] '_' ;
FUNCTION : 'f(' ;
GAMMAF: '\\Gamma(' ;
ZETAF : '\\zeta(' ;

EQUAL : '=' ;
LT: '<';
LEQQ: '\\leqq';
GT: '>';
GEQQ: '\\geqq';
