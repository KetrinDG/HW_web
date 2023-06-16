from src import selects, update_data


class ServiceBot:
    def __init__(self):
        self.cmd_list = {
            "exit": {"func": self.func_exit, "params": []},
            "help": {"func": self.print_help, "params": []},
            "1": {"func": selects.select_1, "params": []},
            "2": {"func": selects.select_2, "params": ["id subject: "]},
            "3": {"func": selects.select_3, "params": ["id subject: "]},
            "4": {"func": selects.select_4, "params": []},
            "5": {"func": selects.select_5, "params": ["id teacher: "]},
            "6": {"func": selects.select_6, "params": ["id group: "]},
            "7": {"func": selects.select_7, "params": ["id group: ", "id subject: "]},
            "8": {"func": selects.select_8, "params": ["id teacher: "]},
            "9": {"func": selects.select_9, "params": ["id student: "]},
            "10": {
                "func": selects.select_10,
                "params": ["id student: ", "id teacher: "],
            },
            "11": {
                "func": selects.select_11,
                "params": ["id student: ", "id teacher: "],
            },
            "12": {"func": selects.select_12, "params": ["id group: ", "id subject: "]},
            "i-teacher": {
                "func": update_data.insert_teacher,
                "params": ["Name teacher: "],
            },
            "u-teacher": {
                "func": update_data.update_teacher,
                "params": ["id teacher: ", "New name teacher: "],
            },
            "d-teacher": {
                "func": update_data.delete_teacher,
                "params": ["id teacher: "],
            },
            "l-teacher": {"func": update_data.list_teacher, "params": []},
            "i-subject": {
                "func": update_data.insert_subject,
                "params": ["Name subject: ", "id teacher: "],
            },
            "u-subject": {
                "func": update_data.update_subject,
                "params": ["id subject: ", "New name subject: ", "id_teacher: "],
            },
            "d-subject": {
                "func": update_data.delete_subject,
                "params": ["id subject: "],
            },
            "l-subject": {"func": update_data.list_subject, "params": []},
            "i-group": {"func": update_data.insert_group, "params": ["Name group: "]},
            "u-group": {
                "func": update_data.update_group,
                "params": ["id group: ", "New name group: "],
            },
            "d-group": {"func": update_data.delete_group, "params": ["id group: "]},
            "l-group": {"func": update_data.list_group, "params": []},
            "i-student": {
                "func": update_data.insert_student,
                "params": ["Name student: ", "id group: "],
            },
            "u-student": {
                "func": update_data.update_student,
                "params": ["id student: ", "New name student: ", "id_group: "],
            },
            "d-student": {
                "func": update_data.delete_student,
                "params": ["id student: "],
            },
            "l-student": {"func": update_data.list_student, "params": []},
            "i-grade": {
                "func": update_data.insert_grade,
                "params": ["id student: ", "id subject: ", "grade: ", "date: "],
            },
            "u-grade": {
                "func": update_data.update_grade,
                "params": ["id student: ", "id subject: ", "date: ", "New grade: "],
            },
            "d-grade": {
                "func": update_data.delete_grade,
                "params": ["id student: ", "id subject: ", "date: "],
            },
            "l-grade": {"func": update_data.list_grade, "params": []},
        }

    def func_exit(self):
        print("\033[035mGood buy\033[0m")
        quit()

    def print_help(self):
        print(
            " \033[034mSelect the operation you want to perform and enter a specific number:\033[0m"
        )
        print(
            """\033[033m 1) Top 5 students with the highest average grade across all subjects \n 2) Students with the highest average grade in a specific subject (parameters: subject id) \n 3) Average grade in groups for a specific subject (parameters: subject id) \n 4) Average grade in the entire course (all subjects) \n 5) Courses taught by a specific teacher (parameters: teacher id) \n 6) List of students in a specific group (parameters: group id) \n 7) Grades of students in a specific group for a specific subject (parameters: group id, subject id) \n 8) Average grade given by a specific teacher for their subjects (parameters: teacher id) \n 9) List of courses attended by a student (parameters: student id) \n 10) List of courses taught by a specific teacher to a specific student (parameters: student id, teacher id) \n 11) Average grade given by a specific teacher to a specific student (parameters: student id, teacher id) \n 12) Grades of students in a specific group for a specific subject on the last lesson (parameters: group id, subject id)\033[0m """
        )
        print(
            "\033[036m>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> \n\033[32m"
        )
        print(
            " \033[034mIf you want to edit tables with data, do the following: \033[0m"
        )
        print(
            " \033[033mi-teacher (u-teacher, d-teacher) - Add (Change, Delete) a teacher \n i-group (u-group, d-group) - Add (Change, Delete) a group \n i-student (u-student, d-student) - Add (Change, Delete) a student \n i-subject (u-subject, d-subject) - Add (Change, Delete) a subject \n i-grade (u-grade, d-grade) - Add (Change, Delete) a greade. \033[0m "
        )
        print(" \033[034mhelp - Command\033[0m")
        print(" \033[031mexit - Exit\033[0m")

    def cmd(self, cmd):
        if cmd not in self.cmd_list:
            print("\033[035mWrong command.\033[0m")
            return
        args = []
        for el in self.cmd_list[cmd]["params"]:
            param = input(el)
            args.append(param)
        self.cmd_list[cmd]["func"](*args)
