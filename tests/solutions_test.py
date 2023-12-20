from advent_of_code.solutions import day_16


class TestDay16:

    def test_day_16(self):
        test_data = """
            .|...\....
            |.-.\.....
            .....|-...
            ........|.
            ..........
            .........\
            ..../.\\..
            .-.-/..|..
            .|....-|.\
            ..//.|....
        """
        assert day_16.get_solution(test_data) == 46
