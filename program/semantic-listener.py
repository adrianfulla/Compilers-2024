import sys
import datetime
from antlr4 import *
from ConfRoomSchedulerLexer import ConfRoomSchedulerLexer
from ConfRoomSchedulerParser import ConfRoomSchedulerParser
from ConfRoomSchedulerListener import ConfRoomSchedulerListener

class ConfRoomSchedulerSemanticChecker(ConfRoomSchedulerListener):
    def enterReserveStat(self, ctx):
        
        
        self.validateDateAndTime(ctx)
        
        pass
    
    def validateDateAndTime(self,ctx):
        try:
            date_token = ctx.getChild(0).DATE().getText()
            start_time_token = ctx.getChild(0).TIME(0).getText()
            end_time_token = ctx.getChild(0).TIME(1).getText()
            date_obj = datetime.datetime.strptime(date_token, '%d/%m/%Y')

            start_time_obj = datetime.datetime.strptime(start_time_token, '%H:%M')
            end_time_obj = datetime.datetime.strptime(end_time_token, '%H:%M')

            if start_time_obj >= end_time_obj:
                print(f"Error en reserva {ctx.getChild(0).getText()}: La hora de inicio {start_time_token} debe ser anterior a la hora de fin {end_time_token}.")
            else:
                print("Reserva válida para la fecha y horas ingresadas.")
        except ValueError as e:
            print(f"Error en reserva {ctx.getChild(0).getText()} con la entrada de fecha o tiempo")

def main():
    input_stream = FileStream(sys.argv[1])
    lexer = ConfRoomSchedulerLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ConfRoomSchedulerParser(stream)
    tree = parser.prog()
    
    semantic_checker = ConfRoomSchedulerSemanticChecker()
    walker = ParseTreeWalker()
    walker.walk(semantic_checker, tree)

if __name__ == '__main__':
    main()