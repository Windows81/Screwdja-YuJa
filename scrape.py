import threading
import requests
import argparse
import typing
import json
import util
import sys


def get_info(vid_id: int) -> util.csv_struct | None:
    try:
        url = f'https://my.yuja.com/P/Data/GetVideoListNodeInfo?videoPID={vid_id}'
        res: dict[str, typing.Any] = requests.get(url).json()
        t_broadcast: dict[str, typing.Any] = json.loads(res['broadcast'])
        t_video: dict[str, typing.Any] = json.loads(res['video'])
        # t_node: dict[str, typing.Any] = json.loads(res['node'])

        t_class_infos = json.loads(res.get('classInfo', '[]'))
        t_class: dict[str, typing.Any] = {}
        if len(t_class_infos):
            t_class = t_class_infos[0]

        brd_id = t_broadcast["broadcastPID"]
        auth = t_broadcast.get('authcode', 0)
        if not auth:
            return None
        edit_auth = t_broadcast.get('editorAuthCode', 0)
        thumb_key = t_broadcast.get('thumbKey', '')
        cap_key = t_broadcast.get('captionFileKey', '')
        own_id = t_broadcast.get('ownerPID', 0)

        title = t_video['title']
        create = t_video.get('creationTimestamp', {}).get('seconds', 0)
        modify = t_broadcast.get('lastModifiedTimestamp', {}).get('seconds', 0)

        cls_id = t_class.get('classPID', 0)
        cls_name = t_class.get('className', '')
        ins_name = t_class.get('reducedInstName', '')

        return util.csv_struct(
            video_id=vid_id,
            class_id=cls_id,
            owner_id=own_id,
            thumb_key=thumb_key,
            broadcast_id=brd_id,
            institution=ins_name,
            class_name=cls_name,
            title=title,
            creation=create,
            modification=modify,
            auth_code=auth,
            edit_auth_code=edit_auth,
            caption_key=cap_key,
        )

    except requests.exceptions.JSONDecodeError:
        return None


def process(r: range) -> typing.Generator[util.csv_struct, None, None]:
    for i, base_id in enumerate(r):
        limit = getattr(process, 'limit')
        do_quit = getattr(process, 'quit')
        if do_quit and i > limit:
            break
        if i > limit:
            setattr(process, 'limit', i)
        info = get_info(base_id)
        if info:
            print(base_id)
            yield info


def write(queue: util.file_queue, g: typing.Generator[util.csv_struct, None, None]) -> None:
    for o in g:
        queue.add(o)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-incr", default=-1, required=False, type=int)
    parser.add_argument("-ss", type=int)
    parser.add_argument("-stop", default=-1, required=False, type=int)
    parser.add_argument("-threads", default=2, required=False, type=int)
    args = parser.parse_args()
    incr, ss, stop, th = args.incr, args.ss, args.stop, args.threads
    setattr(write, "debounce", False)
    setattr(process, "quit", False)
    setattr(process, "limit", 0)

    queue = util.file_queue()
    if incr > 0 and stop == -1:
        stop = 88888888
    ths = tuple(
        threading.Thread(
            target=write,
            args=[
                queue,
                process(range(ss + o * incr, stop, incr * th))
            ],
        )
        for o in range(0, th)
    )
    for t in ths:
        t.start()
    input()
    setattr(process, 'quit', True)
