
import csv
from dataclasses import dataclass
from io import TextIOWrapper
import os
import threading
import time
import typing


@dataclass(unsafe_hash=True)
class csv_struct:
    video_id: int
    broadcast_id: int
    class_id: int
    owner_id: int
    class_name: str
    institution: str
    title: str
    auth_code: int
    edit_auth_code: int
    creation: int
    modification: int
    caption_key: str
    thumb_key: str


class file_list(set[csv_struct]):
    stream: TextIOWrapper
    writer: typing.Any

    def __init__(self, path: str) -> None:
        super().__init__()
        self.stream = open(path, 'a', newline="", encoding='utf-8')
        keys = csv_struct.__annotations__.keys()
        self.writer = csv.writer(self.stream)
        if self.stream.tell() == 0:
            self.writer.writerow(keys)
            self.stream.flush()

    def __del__(self) -> None:
        self.stream.close()

    def write(self, stuff: csv_struct) -> None:
        values = list(stuff.__dict__.values())
        for i in [0, 1]:
            values[i] = str(values[i]).rjust(8, '0')
        self.writer.writerow(values)
        self.stream.flush()


def _default_get_index(vid: int, /) -> str:
    return f"csv/{int(vid)//10000:04d}.csv"


class csv_streams:
    get_index: typing.Callable[[int], str]

    def get_paths(self) -> set[str]:
        return set(p for p in set(
            self.get_index(i) for i in range(0, int(1e7), 100))
            if os.path.isfile(p))

    def _gen(self, paths: set[str]) -> typing.Generator[str, None, None]:
        for i, p in enumerate(paths):
            with open(p, 'r', encoding='utf-8') as f:
                for j, l in enumerate(f):
                    if j > 0 or i == 0:
                        yield l

    def __init__(self, get_index: typing.Callable[[int], str] = _default_get_index) -> None:
        self.get_index = get_index
        self.merge_stream = csv.DictReader(
            self._gen(self.get_paths()),
            delimiter=",", quotechar='"'
        )


class file_queue(threading.Thread):
    get_index: typing.Callable[[int], str]
    stuff: dict[str, file_list]
    _thread: threading.Thread
    _join: bool

    def add(self, struct: csv_struct) -> None:
        i = self.get_index(struct.video_id)
        self.stuff.setdefault(i, file_list(i)).add(struct)

    def _empty(self) -> bool:
        values = list(self.stuff.values())
        done = False
        for s in values:
            if s:
                done = True
            for struct in list(s):
                s.write(struct)
                s.discard(struct)
        return done

    def _run_thread(self) -> None:
        while self._join:
            self._empty()

    def __init__(self, get_index: typing.Callable[[int], str] = _default_get_index) -> None:
        self.stuff = {}
        self._join = True
        self.get_index = get_index
        super().__init__(
            target=self._run_thread,
            daemon=True,
        )
        self.start()

    def join(self) -> None:
        self._join = False
        return super().join()
