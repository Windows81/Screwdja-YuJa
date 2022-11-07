import argparse
import requests
import glob
import csv
import util

f = [open(n, "r", encoding="utf-8") for n in glob.glob("yuja*.csv")]
g = (str(l) for i, s in enumerate(f) for j, l in enumerate(s) if j > 0 or i == 0)
s = csv.DictReader(g, delimiter=",", quotechar='"')


def get_links(vid: int) -> set[str]:
    with open(util.get_index(vid), "r", encoding="utf-8") as f:
        s = csv.DictReader(f, delimiter=",", quotechar='"')
        for d in s:
            if int(d['video_id']) == vid:
                prefix = f'https://uci.yuja.com/P/Data/VideoSource?video=/P/VideoCaptures/a/1/{d["broadcast_id"]}/{d["auth_code"]}&videoPID={d["video_id"]}'
                urls = [
                    f'{prefix}&mp4Only=true',
                    f'{prefix}&mp4Only=false',
                ]
                return set(
                    m['fileURL']
                    for u in urls
                    for s in requests.get(u).json()['streams']
                    if not s['isAudioOnly'] and s['hasAudioCodec']
                    for m in s['typeAndVideoSourceMap'].values()
                )
    return set()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('video_id', type=int)
    args = parser.parse_args()
    vid = args.video_id  # int(sys.argv[1])
    for l in get_links(vid):
        print(l)
