import sys
import datetime
from antlr4 import *
from ConfRoomSchedulerLexer import ConfRoomSchedulerLexer
from ConfRoomSchedulerParser import ConfRoomSchedulerParser
from ConfRoomSchedulerListener import ConfRoomSchedulerListener


class Reservation:
    def __init__(self, room_id, date, start_time, end_time):
        self.room_id = room_id
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.max_hours = 2


    def overlaps_with(self, other):
        if self.room_id == other.room_id and self.date == other.date:
            return self.start_time < other.end_time and self.end_time > other.start_time
        return False

    def check_max_hours(self):
        return (self.end_time - self.start_time).seconds / 3600 < self.max_hours

class ConfRoomSchedulerSemanticChecker(ConfRoomSchedulerListener):
    def __init__(self):
        self.reservations = []
        
    def enterReserveStat(self, ctx):
        try:
            print("\n")
            dates = self.validateDateAndTime(ctx)
            self.validateOverlapReservation(ctx=ctx, dates=dates)
        except:
            pass
        
    def enterReprogramStat(self, ctx):
    # Obtener los datos de la reprogramación
        room_id = ctx.getChild(0).ID().getText()
        original_date = ctx.getChild(0).DATE(0).getText()
        original_start_time = ctx.getChild(0).TIME(0).getText()
        original_end_time = ctx.getChild(0).TIME(1).getText()
        new_date = ctx.getChild(0).DATE(1).getText() if len(ctx.getChild(0).DATE()) > 1 else original_date
        new_start_time = ctx.getChild(0).TIME(2).getText()
        new_end_time = ctx.getChild(0).TIME(3).getText()

        # Buscar la reserva original
        original_res = None
        for res in self.reservations:
            if (res.room_id == room_id and
                res.date.strftime('%d/%m/%Y') == original_date and
                res.start_time.strftime('%H:%M') == original_start_time and
                res.end_time.strftime('%H:%M') == original_end_time):
                original_res = res
                break

        if not original_res:
            print("No se encontró la reserva original para reprogramar.")
            return

        try:
            new_date_obj = datetime.datetime.strptime(new_date, '%d/%m/%Y')
            new_start_time_obj = datetime.datetime.strptime(new_start_time, '%H:%M')
            new_end_time_obj = datetime.datetime.strptime(new_end_time, '%H:%M')

            if new_start_time_obj >= new_end_time_obj:
                print(f"Error: La nueva hora de inicio debe ser anterior a la nueva hora de fin.")
                return

            new_reservation = Reservation(room_id, new_date_obj, new_start_time_obj, new_end_time_obj)
            for res in self.reservations:
                if res != original_res and res.overlaps_with(new_reservation):
                    print(f"Error: La nueva reserva de {room_id} está solapada con otra existente.")
                    return

            original_res.date = new_date_obj
            original_res.start_time = new_start_time_obj
            original_res.end_time = new_end_time_obj
            print(f"Reserva de {room_id} reprogramada para {new_date} de {new_start_time} a {new_end_time} correctamente.")

        except ValueError as e:
            print(f"Error en la entrada de fecha o tiempo: {str(e)}")

    
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
                return [date_obj,start_time_obj, end_time_obj]
        except ValueError as e:
            print(f"Error en reserva {ctx.getChild(0).getText()} con la entrada de fecha o tiempo")
     
    def validateOverlapReservation(self, ctx, dates):
        child = ctx.getChild(0)
        new_reservation = Reservation(child.ID().getText(), dates[0],dates[1],dates[2])
        for reservation in self.reservations:
            if reservation.overlaps_with(new_reservation):
                print(f"Error: La reserva para el salón {child.getText()} está solapada con otra reserva.")
                return 
        if not new_reservation.check_max_hours():
            print(f"Error: La reserva para el salón {child.getText()} excede el máximo de horas permitido.")
            return
        self.reservations.append(new_reservation)
        print(f"Reserva agregada correctamente para el salón {child.getText()}.")

    
    
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