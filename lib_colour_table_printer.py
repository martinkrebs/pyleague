from lib_table_printer import TablePrinter
from colorama import Fore, Back, Style


class ColourTablePrinter(TablePrinter):

    # Partial overide
    def print_headings(self):
        print(Fore.YELLOW + Back.BLUE)
        super(ColourTablePrinter, self).print_headings()
        print(Style.RESET_ALL)
