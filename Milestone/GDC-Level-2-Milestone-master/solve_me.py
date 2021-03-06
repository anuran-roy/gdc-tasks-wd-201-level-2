class TasksCommand:
    TASKS_FILE = "tasks.txt"
    COMPLETED_TASKS_FILE = "completed.txt"

    current_items: dict = {}
    completed_items: list = []

    def read_current(self):
        try:
            file = open(self.TASKS_FILE, "r")
            for line in file.readlines():
                item = line[:-1].split(" ")
                self.current_items[int(item[0])] = " ".join(item[1:])
            file.close()
        except Exception:
            pass

    def read_completed(self):
        try:
            file = open(self.COMPLETED_TASKS_FILE, "r")
            self.completed_items = file.readlines()
            file.close()
        except Exception:
            pass

    def write_current(self):
        with open(self.TASKS_FILE, "w+") as f:
            f.truncate(0)
            for key in sorted(self.current_items.keys()):
                f.write(f"{key} {self.current_items[key]}\n")

    def write_completed(self):
        with open(self.COMPLETED_TASKS_FILE, "w+") as f:
            f.truncate(0)
            for item in self.completed_items:
                f.write(f"{item}\n")

    def run(self, command: str, args: list):
        self.read_current()
        self.read_completed()
        if command == "add":
            self.add(args)
        elif command == "done":
            self.done(args)
        elif command == "delete":
            self.delete(args)
        elif command == "ls":
            self.ls()
        elif command == "report":
            self.report()
        elif command == "help":
            self.help()

    def help(self):
        print(
            """Usage :-
$ python tasks.py add 2 hello world # Add a new item with priority 2 and text "hello world" to the list
$ python tasks.py ls # Show incomplete priority list items sorted by priority in ascending order
$ python tasks.py del PRIORITY_NUMBER # Delete the incomplete item with the given priority number
$ python tasks.py done PRIORITY_NUMBER # Mark the incomplete item with the given PRIORITY_NUMBER as complete
$ python tasks.py help # Show usage
$ python tasks.py report # Statistics"""
        )

    def add(self, args: list):
        self.read_current()
        priority = int(args[0])
        if priority not in self.current_items.keys():
            self.current_items[priority] = str(args[1])
        else:
            keys = sorted(
                [[int(args[0]), args[1]]]
                + [[x[0], x[1]] for x in self.current_items.items()],
                key=lambda x: x[0],
            )

            for i in range(len(keys) - 1):
                if keys[i][0] == keys[i + 1][0]:
                    keys[i + 1][0] += 1

            self.current_items = dict(keys)

        print(f'Added task: "{args[1]}" with priority {args[0]}')
        self.write_current()

    def done(self, args: list):
        self.read_current()
        self.read_completed()

        key: int = int(args[0])

        if key in self.current_items.keys():
            value: str = str(self.current_items[key])

            del self.current_items[key]
            self.completed_items += [value]

            for x in self.completed_items:
                x = x.strip("\n")

            print(self.completed_items)
            print("Marked item as done.")
        else:
            print(f"Error: no incomplete item with priority {key} exists.")

        self.write_current()
        self.write_completed()

    def delete(self, args: list):
        self.read_current()
        key = int(args[0])
        if key in self.current_items.keys():
            del self.current_items[key]
            print(f"Deleted item with priority {args[0]}")
        else:
            print(
                f"Error: item with priority {args[0]} does not exist. Nothing deleted."
            )
        self.write_current()

    def ls(self):
        self.read_current()
        for i, key in enumerate(sorted(self.current_items.keys())):
            print(f"{i+1}. {self.current_items[key]} [{key}]")

    def report(self):
        self.read_current()
        self.read_completed()

        while "\n" in self.completed_items:
            self.completed_items.remove("\n")

        while "" in self.completed_items:
            self.completed_items.remove("")

        while " " in self.completed_items:
            self.completed_items.remove(" ")

        print(f"Pending : {len(self.current_items)}")

        for i, key in enumerate(sorted(self.current_items.keys())):
            print(f"{i+1}. {self.current_items[key]} [{key}]")

        print(f"\nCompleted : {len(self.completed_items)}")

        for i in range(len(self.completed_items)):
            print(f"{i+1}. {self.completed_items[i]}")
