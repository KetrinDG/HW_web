from classes import Univer


def main(univer):
    univer.create_table()
    univer.fill_DB()
    univer.print_help()
    while True:
        print(
            "\033[036m<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\033[0m"
        )
        command = input("\033[033mcommand: \033[0m").lower()
        print(
            "\033[033m>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\033[32m"
        )
        if command == "exit":
            break
        if command == "help":
            univer.print_help()
        else:
            univer.query(*command.strip().split(" "))


if __name__ == "__main__":
    db = Univer()
    with db as univer:
        main(univer)

    print("Good buy!")
