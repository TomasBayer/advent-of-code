from advent_of_code.solutions import day_2023_16


class TestDay16:

    def test_day_16(self):
        assert day_2023_16.get_part1_solution(r"..|..") == 3
        assert day_2023_16.get_part1_solution(r"..-..") == 5
        assert day_2023_16.get_part1_solution(r"../..""\n"r".....") == 3
        assert day_2023_16.get_part1_solution(r"..\..""\n"r".....") == 4
        assert day_2023_16.get_part1_solution(r"..|..""\n"r".....") == 4

        test_data = r"""
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
        assert day_2023_16.get_part1_solution(test_data) == 46
