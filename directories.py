import abc
import argparse
import dataclasses
from enum import StrEnum
from typing import Iterable, Optional, Tuple


@dataclasses.dataclass
class Directory(dict):
    name: str
    parent: "Directory" = None

    def add_child(self, path: Iterable[str]):
        if isinstance(path, str):
            self.setdefault(path, Directory(path, self))

        else:
            walker = self
            for name in path:
                walker = walker.setdefault(name, Directory(name, walker))

    def get_child(self, path: Iterable[str]) -> Tuple[str, Optional["Directory"]]:
        if isinstance(path, str):
            return path, self.get(path)

        walker = self
        name = path
        for name in path:
            walker = walker.get(name)

            if walker is None:
                break

        return name, walker

    def __repr__(self):
        return self.name


class CmdType(StrEnum):
    CREATE = "CREATE"
    DELETE = "DELETE"
    MOVE = "MOVE"
    LIST = "LIST"


class Cmd:
    @abc.abstractmethod
    def __call__(self, directories: dict, *args: str):
        pass

    @staticmethod
    def split(path) -> Iterable[str]:
        return path.split("/")


class CreateCmd(Cmd):
    def __call__(self, root: Directory, *args: str):
        if not args:
            print("CREATE command does not have an argument")
            return

        root.add_child(self.split(args[0]))


class DeleteCmd(Cmd):
    def __call__(self, root: Directory, *args: str):
        if not args:
            print("DELETE command does not have an argument")
            return

        path = args[0]
        name, child = root.get_child(self.split(path))

        if child is None:
            print(f"Cannot delete {path} - {name} does not exist")
            return

        child.parent.pop(child.name)


class MoveCmd(Cmd):
    def __call__(self, root: Directory, *args: str):
        args_len = len(args)
        if args_len != 2:
            print(f"MOVE command has {args_len} arguments, but 2 arguments needed")
            return

        from_path, to_path = args
        name, source = root.get_child(self.split(from_path))

        if source is None:
            print(f"Cannot move from {from_path} - {name} does not exist")
            return

        name, destination = root.get_child(self.split(to_path))

        if destination is None:
            print(f"Cannot move to {to_path} - {name} does not exist")
            return

        destination[source.name] = source
        source.parent.pop(source.name)


def print_dict_recursive(d: dict, indent: int):
    for k, v in sorted(d.items()):
        print(f'{" " * indent}{k}')
        if v:
            print_dict_recursive(v, indent + 1)


class ListCmd(Cmd):
    def __call__(self, root: Directory, *args: str):
        print_dict_recursive(root, 0)


class CmdsFromFile(Iterable[str]):
    def __init__(self, filename):
        self.filename = filename

    def __iter__(self):
        with open(self.filename) as fr:
            for line in fr:
                line = line.replace("\n", "")
                print(line)
                yield line


def cmds_from_input():
    while True:
        try:
            yield input()
        except KeyboardInterrupt:
            break


class FileSystem:
    def __init__(self, root: Directory):
        self.root = root
        self.cmd_by_cmd_type = {
            CmdType.CREATE: CreateCmd(),
            CmdType.DELETE: DeleteCmd(),
            CmdType.MOVE: MoveCmd(),
            CmdType.LIST: ListCmd(),
        }

    def create(self, path: str):
        self.cmd_by_cmd_type[CmdType.CREATE](self.root, path)

    def delete(self, path: str):
        self.cmd_by_cmd_type[CmdType.DELETE](self.root, path)

    def move(self, from_path: str, to_path: str):
        self.cmd_by_cmd_type[CmdType.MOVE](self.root, from_path, to_path)

    def list(self):
        self.cmd_by_cmd_type[CmdType.LIST](self.root)

    def run_cmds(self, cmds: Iterable[str]):
        for cmd in cmds:
            cmd_type, *args = cmd.split(" ")
            cmd = self.cmd_by_cmd_type.get(cmd_type)
            cmd and cmd(self.root, *args)


def main(filename):
    if filename:
        cmds = CmdsFromFile(filename)

    else:
        cmds = cmds_from_input()

    root = Directory("")
    fs = FileSystem(root)
    fs.run_cmds(cmds)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file")
    args = parser.parse_args()

    try:
        main(args.file)
    except EOFError:
        pass
