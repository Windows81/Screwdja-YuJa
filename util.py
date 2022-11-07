
import csv
from dataclasses import dataclass
from io import TextIOWrapper
import threading
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


def get_index(vid: int) -> str:
    return f"yuja{int(vid/5e5)*5:02d}.csv"


class file_queue:
    stuff: dict[str, file_list]
    _thread: threading.Thread

    def add(self, struct: csv_struct) -> None:
        i = get_index(struct.video_id)
        if i in self.stuff:
            self.stuff[i].add(struct)
            return
        self.stuff[i] = file_list(i)

    def _run_thread(self) -> None:
        while True:
            values = list(self.stuff.values())
            for s in values:
                for struct in list(s):
                    s.write(struct)
                    s.remove(struct)

    def __init__(self) -> None:
        self.stuff = {}
        self._thread = threading.Thread(
            target=self._run_thread,
            daemon=True,
        )
        self._thread.start()
