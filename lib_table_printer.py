class TablePrinter:
    """
    the main method, print_table() takes a record set (list of tuples)
    and displays them in a ascii table in terminal. Also adds the header row.
    """

    def __init__(self, headings=('Team Name', 'w', 'd', 'l', 'pts')):
        self.headings = headings

    def print_row(self, row):
        """row is a tuple of column name strings"""

        # 24char col width for name col, rest are 1 tab width
        # calc n, how many chars you need to add to name lenght to make 23
        n = 23 - len(row[0])
        print('| ', row[0], ' '*n,
              '| ', row[1], '\t',
              '| ', row[2], '\t',
              '| ', row[3], '\t',
              '| ', row[4], '\t', ' |', sep='')

    def print_headings(self):
        self.print_row(self.headings)

    def print_table_body(self, table):
        for row in table:
            self.print_row(row)

    def print_table(self, table):
        """table is a list of rows (a list of tuples)"""
        # print("\033c")  # clear screen
        self.print_headings()
        self.print_table_body(table)
