import json
from os import system, name, path
from sys import stdout
from time import sleep

home_dir = path.expanduser("~")
save_file = f"{home_dir}/hacker_factory.json"


colors = {
    "yellow": "\033[1;33",
    "header": "\033[95m",
    "blue": "\033[94m",
    "cyan": "\033[96m",
    "green": "\033[92m",
    "purple": "\033[35m",
    "warning": "\033[93m",
    "red": "\033[91m",
    "reset": "\033[0m",
    "bold": "\033[1m",
    "underline": "\033[4m",
}


def progressbar(
    length=10,
    char="#",
    sleeptime=0.04,
    text="Progress:",
    fill_char=".",
    color=colors["green"],
    background_color="",
    header_color=colors["blue"],
    fail_color=colors["red"],
    fail_message="Aborted...",
):
    try:
        stdout.write("Progress: ")
        char_length = 0

        while length > 0:
            stdout.write(
                f"\r{header_color}{text}{colors['reset']} [{color}{char * (char_length)}{background_color}{fill_char * (length - char_length)}{colors['reset']}]"
            )

            stdout.flush()

            char_length += 1

            if char_length > length:
                return True

            sleep(sleeptime)

    except KeyboardInterrupt:
        print(f"{fail_color}{fail_message}{colors['reset']}")

        return "fail"


def get_input(text=""):
    response = input(text).strip().lower()

    if response == "n":
        return "next_batch"


def clear():
    """A function to clear the screen depending on the system."""
    if name == "nt":
        system("cls")

    elif name == "posix":
        system("clear")


def banner():
    print(
        f"""{colors['cyan']}
  _    _            _             _       ______         _
 | |  | |          | |           ( )     |  ____|       | |
 | |__| | __ _  ___| | _____ _ __|/ ___  | |__ __ _  ___| |_ ___  _ __ _   _
 |  __  |/ _` |/ __| |/ / _ \ '__| / __| |  __/ _` |/ __| __/ _ \| '__| | | |
 | |  | | (_| | (__|   <  __/ |    \__ \ | | | (_| | (__| || (_) | |  | |_| |
 |_|  |_|\__,_|\___|_|\_\___|_|    |___/ |_|  \__,_|\___|\__\___/|_|   \__, |
                                                                        __/ |
                                                                       |___/
    {colors['reset']}"""
    )


# Read the data and then break, else, create data, restart the loop.
while True:
    try:
        with open(save_file, "r") as f:
            data = json.load(f)
            build_time = data["build_time"]
            quantity = data["quantity"]
            items = data["items"]
            upgrade_num = data["upgrade_num"]
            item_name = data["item_name"]

        break

    except:
        with open(save_file, "w") as f:
            player_data = {
                "build_time": 5,
                "quantity": 1,
                "items": 0,
                "upgrade_num": 5,
                "item_name": "cookies",
            }

            json.dump(player_data, f)


def build():
    print(f"Action: Making {quantity} {item_name}\n")

    result = progressbar(
        length=quantity,
        char="█",
        sleeptime=build_time,
        text=f"Making {item_name}",
        fill_char="░",
        fail_color=colors["red"],
        fail_message="Current batch canceled...",
    )

    if result != "fail":
        return items + quantity
    else:
        return items


if __name__ == "__main__":
    while True:
        banner()

        print(
            f"{colors['green']}(n)ext batch, (qu)antity upgrade, (sp)eed upgrade: ({upgrade_num} needed to upgrade.){colors['reset']}",
        )
        print(f"{items} {item_name}.")

        command = input(f"{colors['cyan']}COMMAND: {colors['reset']}")

        if command == "n":
            items = build()

        elif command == "qu":
            if items >= upgrade_num:
                quantity += 2
                items -= upgrade_num
                upgrade_num += 5
            else:
                print("NOT ENOUGH TO UPGRADE... PRESS [ENTER]")
                input()

        elif command == "sp":
            if items >= upgrade_num:
                if 0 >= (build_time - 0.10):
                    build_time = 0

                build_time -= 0.10
                items -= upgrade_num
                upgrade_num += 5
            else:
                print("NOT ENOUGH TO UPGRADE... PRESS [ENTER]")
                input()

        clear()

        data = {
                "build_time": build_time,
                "quantity": quantity,
                "items": items,
                "upgrade_num": upgrade_num,
                "item_name": item_name,
            }

        with open(save_file, "w") as f:
            json.dump(data, f)

