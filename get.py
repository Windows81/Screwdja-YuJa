import argparse
import requests
import csv
import util


def get_links(vid: int) -> set[str]:
    f = util.csv_streams()
    dict_obj: dict[str, int | str] = {}
    with open(f.get_index(vid), "r", encoding="utf-8") as f:
        s = csv.DictReader(f, delimiter=",", quotechar='"')
        for d in s:
            if int(d['video_id']) == vid:
                dict_obj = d  # type: ignore
                break
    if not dict_obj:
        return set()

    prefix = f'https://uci.yuja.com/P/Data/VideoSource?video=/P/VideoCaptures/a/1/{dict_obj["broadcast_id"]}/{dict_obj["auth_code"]}&videoPID={dict_obj["video_id"]}'
    urls = [
        f'{prefix}&mp4Only=true',
        f'{prefix}&mp4Only=false',
    ]
    result: set[str] = set()
    for u in urls:
        j = requests.get(u).json()
        result.update(
            m['fileURL']
            for s in j['streams']
            # if not s['isAudioOnly'] and s['hasAudioCodec']
            for m in s['typeAndVideoSourceMap'].values()
        )
        result.update(j['captionURL'].values())

    return set(
        f"https://my.yuja.com{r}"
        if r.startswith('/')
        else r
        for r in result
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('video_id', type=int)
    args = parser.parse_args()
    vid = args.video_id
    for l in get_links(vid):
        print(l)
