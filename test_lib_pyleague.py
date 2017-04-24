import lib_pyleague
import os
import sqlite3
import unittest
# import pdb

"""
run all with: $ python -m unittest test_lib_pyleague.py -v
run specific with: $ python -m unittest test_lib_pyleague.<class>.<method> -v
"""

test_db = 'lib_pyleague_test.db'


class TestLibPyleague(unittest.TestCase):
    """
    Test lib_pyleague.py
    """

    def setUp(self):
        # pdb.set_trace()
        self.maxDiff = None

        # set pyleague.db global to test database
        db = sqlite3.connect(test_db)
        lib_pyleague.db.close()
        lib_pyleague.db = db

        # Setup db connection for tests to use
        conn = sqlite3.connect(test_db)
        cursor = conn.cursor()

        # Create the db table
        query = """
        CREATE TABLE IF NOT EXISTS league_table(
            name TEXT,
            w INTEGER,
            d INTEGER,
            l INTEGER,
            pts INTEGER
        )
        """
        cursor.execute(query)

        cursor.executemany(
            "INSERT INTO league_table VALUES (?, ?, ?, ?, ?)",
            self.result_set()
        )

        # save to the database
        conn.commit()
        cursor.close()
        conn.close()

    def tearDown(self):
        """
        Delete the database
        """
        os.remove(test_db)

    def test_get_record_by_name(self):
        """
        confirm:
        Get a record by name, returns <class 'tuple'> or None
        eg: ('chelsea', 24, 3, 5, 75) or None
        """
        expected = self.result_set()[0]
        # use function under test to get record from db
        actual = lib_pyleague.get_record_by_name(self.result_set()[0][0])

        self.assertEqual(expected, actual)

    def test_create_record(self):
        """
        confirm:
        Creates a new team record from tuple (name, w, d, l, pts)
        """
        conn = sqlite3.connect(test_db)
        cursor = conn.cursor()

        team_name = 'letchworth rovers'
        expected = (team_name, 10, 3, 5, 36)
        # use function under test to write a record to the db
        lib_pyleague.create_record(expected)

        # Read back the saved record from the db
        cursor.execute("SELECT * FROM league_table WHERE name=?", (team_name,))
        actual = cursor.fetchone()

        self.assertEqual(expected, actual)

        cursor.close()
        conn.close()

    def test_update_record(self):
        """
        confirm:
        Updates an existing record, from a tuple (name, w, d, l, pts)
        & all remaining records are unchanged
        """
        conn = sqlite3.connect(test_db)
        cursor = conn.cursor()

        # Use chelsea from result set- already in test db
        record = self.result_set()[0]

        # chelsea just won a game with an opponent, the update tuple is :
        update_tuple = ('chelsea', 1, 0, 0, 3)

        # create our expected result record
        l_record = list(record)
        l_record[1] += 1
        l_record[4] += 3
        record = tuple(l_record)

        # use the function under test to update db so we can check result
        lib_pyleague.update_record(update_tuple)

        # Create our expected result set
        expected = self.result_set()
        expected[0] = record

        # Read all records back in check the one we updated has changed
        # as expected and all the others have not changed
        cursor.execute("SELECT * FROM league_table")
        actual = cursor.fetchall()
        self.assertEqual(expected, actual)

        cursor.close()
        conn.close()

    def test_save_record(self):
        """
        Creates a new record if it does not exist or updates existing one
        """
        # pdb.set_trace()
        conn = sqlite3.connect(test_db)
        cursor = conn.cursor()

        # Update and existing record, use chelsea, and create a new one
        new_record = ('letchworth rovers', 4, 5, 23, 17)
        update_tuple = ('chelsea', 1, 0, 0, 3)
        updated_record = ('chelsea', 25, 3, 5, 78)

        # use function under test to create and update records
        lib_pyleague.save_record(new_record)
        lib_pyleague.save_record(update_tuple)

        # Create our expected result set
        expected = self.result_set()
        expected.append(new_record)  # UNEXPECTED, this updates RESULT_SET
        expected[0] = updated_record

        # Read all records back in check they match our expected results set
        cursor.execute("SELECT * FROM league_table")
        actual = cursor.fetchall()
        self.assertEqual(expected, actual)

        cursor.close()
        conn.close()

    def test_team_game_results(self):
        """
        confirm:
        Returns [w, d, l, pts] - results for a game played with an opponent
        team, eg. if the team won the tuple would be (1 ,0 ,0, 3) for +1 win
        & +3 points
        """
        # Function under test, expected return values
        expected_win = [1, 0, 0, 3]
        expected_draw = [0, 1, 0, 2]
        expected_loss = [0, 0, 1, 0]

        # Win
        actual = lib_pyleague.team_game_results(2, 1)
        self.assertEqual(expected_win, actual)

        # draw
        actual = lib_pyleague.team_game_results(1, 1)
        self.assertEqual(expected_draw, actual)

        # loss
        actual = lib_pyleague.team_game_results(1, 2)
        self.assertEqual(expected_loss, actual)

    def test_update_game_results(self):
        """
        confirm:
        Takes the results of a game and saves each teams record in the db.
        """
        # pdb.set_trace()
        conn = sqlite3.connect(test_db)
        cursor = conn.cursor()

        # Add results for a game with an existing team (chelsea winner) and a
        # new team that is not in the database yet (letcworth rovers looser)
        # letchworth rovers, new team, first game, they lost:
        new_record = ('letchworth rovers', 0, 0, 1, 0)
        # chelsea, updated with 1 win
        updated_record = ('chelsea', 25, 3, 5, 78)

        # Create expected result set
        # Create our expected result set
        expected = self.result_set()
        expected.append(new_record)
        expected[0] = updated_record

        # Use function under test to add the game results
        # update_game_results(home_team_name, home_team_goals,
        #                     away_team_name, away_team_goals):
        lib_pyleague.update_game_results('chelsea', 2, 'letchworth rovers', 1)

        # Read all records back in check they match our expected results set
        cursor.execute("SELECT * FROM league_table")
        actual = cursor.fetchall()
        self.assertEqual(expected, actual)

        cursor.close()
        conn.close()

    def test_create_table_if_not_exists(self):
        """
        confirm the create_table_if_not_exists method creates the expected
        table in the db
        """
        conn = sqlite3.connect(test_db)
        cursor = conn.cursor()

        # First remove the table created by the test setUp() method
        # and confirm the table no longer exists
        cursor.execute('DROP TABLE IF EXISTS league_table')
        conn.commit()
        query = """
        SELECT COUNT(*) FROM sqlite_master
        WHERE type='table'
        AND name='league_table'
        """
        cursor.execute(query)
        count = cursor.fetchone()[0]
        self.assertEqual(0, count, 'Assert table does not exist')

        # Now use function under test to create the table again,
        # and then confirmm it exists
        lib_pyleague.create_table_if_not_exists()
        cursor.execute(query)
        count = cursor.fetchone()[0]
        self.assertEqual(1, count, 'Assert table does exist')

        cursor.close()
        conn.close()

    def test_delete_table(self):
        """
        confirm function under test deletes the table
        """
        conn = sqlite3.connect(test_db)
        cursor = conn.cursor()

        query = """
        SELECT COUNT(*) FROM sqlite_master
        WHERE type='table'
        AND name='league_table'
        """

        # first check the table exists
        cursor.execute(query)
        count = cursor.fetchone()[0]
        self.assertEqual(1, count, 'Assert table does exist')

        # use function under test to delete the table
        lib_pyleague.delete_table()

        # confirm the table now does not exist
        cursor.execute(query)
        count = cursor.fetchone()[0]
        self.assertEqual(0, count, 'Assert table does exist')

    def result_set(self):
        """
        Return our test result set.
        Encapsulating in a method prevents the result set from being
        modified.
        If you used a global RESULT_SET, then did this:
        expected = RESULT_SET
        Any modifications to 'expected' would modify RESULT_SET, as 'expected'
        points to the same list that 'RESULT_SET' does.
        """
        return [
            ('chelsea', 24, 3, 5, 75),
            ('tottenham', 21, 8, 3, 71),
            ('watford', 11, 7, 14, 40),
            ('stoke', 10, 9, 14, 39),
            ('leicester', 10, 7, 15, 37),
            ('west ham', 10, 7, 16, 37),
            ('man united', 16, 12, 3, 60),
            ('arsenal', 17, 6, 8, 57),
            ('bournmouth', 9, 8, 16, 35),
            ('hull', 8, 6, 19, 30),
            ('swansea', 8, 4, 21, 28),
            ('liverpool', 19, 9, 5, 66),
            ('man city', 19, 7, 6, 64),
            ('middlesbrough', 4, 12, 16, 24),
            ('everton', 16, 9, 8, 57),
            ('west brom', 12, 8, 13, 44),
            ('southampton', 11, 7, 13, 40),
            ('burnley', 10, 6, 17, 36),
            ('crystal palace', 10, 5, 17, 35),
            ('sunderland', 5, 6, 21, 21)
        ]
