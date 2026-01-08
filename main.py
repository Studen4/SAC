import sac_new
import sac_check
import sac_start
import sac_exit


def main():
    print("Second Army Checker (SAC)")
    print("Created by Kotankyl")
    print("Clan: Second Army\n")

    print("Available commands:")
    print("N / New / 0     - Create new output.csv")
    print("C / Check / 1   - Check input/output files")
    print("S / Start / 2   - Start processing")
    print("E / Exit / 3    - Exit program\n")

    while True:
        user_input = input("Enter command: ").strip().lower()
        if user_input in {"n", "new", "0"}:
            sac_new.run()
        elif user_input in {"c", "check", "1"}:
            sac_check.run()
        elif user_input in {"s", "start", "2"}:
            sac_start.run()
        elif user_input in {"e", "exit", "3"}:
            sac_exit.run()
        else:
            print("Wrong input!")


if __name__ == "__main__":
    main()
