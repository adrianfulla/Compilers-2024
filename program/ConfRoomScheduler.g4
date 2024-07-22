grammar ConfRoomScheduler;

prog: stat+ ;

stat: reserve NEWLINE                # reserveStat
    | cancel NEWLINE                 # cancelStat
    | NEWLINE                        # blank
    ;

reserve: 'RESERVAR' ID 'PARA' DATE 'DE' TIME 'A' TIME
        |'RESERVAR' ID 'PARA' DATE 'DE' TIME 'A' TIME 'POR' NAME 
        ; 

cancel: 'CANCELAR' ID 'PARA' DATE 'DE' TIME 'A' TIME ; 

DATE: DIGIT DIGIT '/' DIGIT DIGIT '/' DIGIT DIGIT DIGIT DIGIT ; 
TIME: DIGIT DIGIT ':' DIGIT DIGIT ;
NAME: [a-zA-Z]+; 
ID  : [a-zA-Z0-9]+ ; 
NEWLINE: '\r'? '\n' ; 
WS  : [ \t]+ -> skip ; 

fragment DIGIT : [0-9] ;
