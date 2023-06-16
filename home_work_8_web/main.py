from mongo import fetch_authors, fetch_quotes


def func_help():
    print("\033[036mCommands:\033[0m")
    print("\033[033m - name:<name>[, <name>,...] - Search authors\033[0m")
    print("\033[033m - tag:<tag>[, <tag>,...] - Search quotes\033[0m")
    print("\033[033m - exit - Close programm\033[0m")
    print("\033[033m - help\033[0m")


def func_exit():
    print("\033[031mGood buy!\033[0m")

    quit()


def get_authors(name):
    if isinstance(name, list):
        name_select = "|".join([el.strip() for el in name])
    elif isinstance(name, str):
        name_select = name.strip()
    else:
        print("\033[035mWrong type of parametr\033[0m")
        return None

    result = fetch_authors(name_select)

    print_author(result)


def get_quotes(tags):
    if isinstance(tags, list):
        tags_select = "|".join([el.strip() for el in tags])
    elif isinstance(tags, str):
        tags_select = tags.strip()
    else:
        print("\033[035mWrong type of parametr\033[0m")
        return None

    result = fetch_quotes(tags_select)

    print_quotes(result)


def print_author(author):
    for el in author:
        print("\033[034mName: ", el["fullname"])
        print("\033[034mBorn date: ", el["born_date"])
        print("\033[034mBorn location: ", el["born_location"])
        print("\033[034mDescription: ", el["description"])
        print(
            "\033[032m--------------------------------------------------------------------------------------\033[0m"
        )


def print_quotes(quotes):
    for el in quotes:
        print("\033[032mTags: ", ", ".join(el["tags"]))
        print("\033[032mAuthor: ", el["author"])
        print("\033[032mQuote: ", el["quote"])
        print(
            "\033[032m--------------------------------------------------------------------------------------\033[0m"
        )


commands = {
    "name": get_authors,
    "tag": get_quotes,
    "exit": func_exit,
    "help": func_help,
}


def main():
    while True:
        print(
            "\033[032m-------------------------------------------------------------------------\033[0m"
        )
        cmd = input(
            "\033[036mEnter command (enter 'help' if you don't know commands): \033[0m"
        )
        print(
            "\033[032m-------------------------------------------------------------------------\033[0m"
        )
        cmd_list = cmd.split(":")
        if not cmd_list or len(cmd_list) > 2 or cmd_list[0] not in commands:
            print("\033[035mWrong command\033[0m")
        else:
            if len(cmd_list) >= 2:
                commands[cmd_list[0]](cmd_list[1].split(","))
            else:
                commands[cmd_list[0]]()


if __name__ == "__main__":
    # seeds()
    main()
