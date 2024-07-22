grammar ConfRoomScheduler;

prog: stat+ ;

stat: reserve NEWLINE                # reserveStat
    | cancel NEWLINE                 # cancelStat
    | reprogram NEWLINE              # reprogramStat
    | NEWLINE                        # blank
    ;

reserve: 'RESERVAR' ID 'PARA' DATE 'DE' TIME 'A' TIME ('POR' NAME)? ('COMO' type)? ('DESCRIPCION' DESCRIPTION)?
        ; 

cancel: 'CANCELAR' ID 'PARA' DATE 'DE' TIME 'A' TIME ; 

reprogram: 'REPROGRAMAR' ID 'EN' DATE 'DE' TIME 'A' TIME 'PARA' (DATE 'DE')? TIME 'A' TIME ;

type:   'JUNTAS' 
    |   'CAPACITACION'
    |   'AUDITORIO'
    |   'CONVENCION'
    ;

DATE: DIGIT DIGIT '/' DIGIT DIGIT '/' DIGIT DIGIT DIGIT DIGIT ; 
TIME: DIGIT DIGIT ':' DIGIT DIGIT ;
NAME: [a-zA-Z]+; 
DESCRIPTION: '"' (~["\r\n])* '"' ;
ID  : [a-zA-Z0-9]+ ; 
NEWLINE: '\r'? '\n' ; 
WS  : [ \t]+ -> skip ; 

fragment DIGIT : [0-9] ;
