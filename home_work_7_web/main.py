from classes import ServiceBot


def main():
    service_bot = ServiceBot()
    while True:
        print(
            "\033[036m<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\033[0m"
        )
        print('\033[033mUse command "help" to get list of command\033[0m')
        command = input("\033[036mcommand: \033[0m").lower()
        print(
            "\033[033m>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\033[32m"
        )
        service_bot.cmd(command)


if __name__ == "__main__":
    main()
