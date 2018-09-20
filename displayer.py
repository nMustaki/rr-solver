import typing
import unicodedata

import colorama

import constants


class Displayer:
    @staticmethod
    def display(board, goal_to_display: typing.Optional[constants.Goal] = None):
        colorama.init()

        for i in range(16):
            up_line, middle_line = [], []

            for j in range(16):
                up_line.append(Displayer._gen_up_line_case(board, i, j))

                middle_line.append(
                    Displayer._gen_middle_line_case(board, i, j, goal_to_display)
                )

            print("".join(up_line))
            print("".join(middle_line))
        print(("+----" * 16) + "+")

    @staticmethod
    def _gen_middle_line_case(board, i, j, goal_to_display=None):
        content = ""
        if (
            j == 0
            or (constants.Wall.LEFT in board[i][j].walls)
            or (j > 0 and constants.Wall.RIGHT in board[i][j - 1].walls)
        ):
            content += "|"
        else:
            content += " "

        if (7 <= i < 9) and (7 <= j < 9):
            content += "----"
        else:
            content += Displayer._gen_middle_line_case_robot(board[i][j].robot)
            goal = board[i][j].goal
            if goal_to_display and goal != goal_to_display:
                goal = None
            content += Displayer._gen_middle_line_case_goal(goal)

        content += "|" if j == 15 else ""
        return content

    @staticmethod
    def _gen_middle_line_case_goal(goal):
        if goal:
            if goal in constants.GOAL_CIRCLE:
                image = "UPPER RIGHT SHADOWED WHITE CIRCLE"

            elif goal in constants.GOAL_COGS:
                image = "HEAVY TEARDROP-SPOKED PINWHEEL ASTERISK"
            elif goal in constants.GOAL_PLANET:
                image = "PINWHEEL STAR"
            elif goal in constants.GOAL_CROSS:
                image = "OPEN CENTRE CROSS"

            if goal == constants.Goal.ANY:
                image = "RAINBOW"
                color = "MAGENTA"
            else:
                color = goal.name.split("_")[0]

            content = (
                getattr(colorama.Fore, color)
                + colorama.Style.BRIGHT
                + unicodedata.lookup(image)
                + colorama.Style.RESET_ALL
            )
            # if image != "RAINBOW":
            content += " "
        else:
            content = "  "
        return content

    @staticmethod
    def _gen_middle_line_case_robot(robot):
        try:
            return (
                getattr(colorama.Fore, robot.name)
                + colorama.Style.BRIGHT
                + unicodedata.lookup("robot face")
                + colorama.Style.RESET_ALL
                # + " "
            )
        except AttributeError:
            return "  "

    @staticmethod
    def _gen_up_line_case(board, i, j):
        content = ""

        if (constants.Wall.UP in board[i][j].walls) or (
            i > 0 and constants.Wall.DOWN in board[i - 1][j].walls
        ):
            content = "+----"
        else:
            content = "+    "

        if j == 15:
            content += "+"
        return content
