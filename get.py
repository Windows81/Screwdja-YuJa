import requests
import glob
import csv

f = [open(n, "r", encoding="utf-8") for n in glob.glob("yuja*.csv")]
g = (str(l) for i, s in enumerate(f) for j, l in enumerate(s) if j > 0 or i == 0)
s = csv.DictReader(g, delimiter=",", quotechar='"')


def get_json(d) -> str:
    url = f'https://uci.yuja.com/P/Data/VideoSource?video=/P/VideoCaptures/a/1/{d["broadcast_id"]}/{d["auth_code"]}&videoPID={d["video_id"]}&mp4Only=true&includeThumbnails=false'
    return requests.get(url).json()['streams'][0]['typeAndVideoSourceMap']['MP4']['fileURL']


for d in s:
    if 'uci' == d['institution'] and 'ics' in d['title'].lower():
        # print(get_json(d))
        print(d)
