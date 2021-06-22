import threading
import requests
import argparse
import html
import re


def process(g):
    for n in g:
        c = requests.get(
            f"https://uci.yuja.com/V/Video?v={n}",
        ).text
        p = re.search(r"https://uci.yuja.com/P/DataPage/BroadcastsThumb/\d+", c)
        if not p:
            continue

        m = re.search(
            r'<meta property="og:title" content="(.+)" />',
            c,
        )
        t = html.unescape(m.group(1))

        v = re.search(
            r"Video-\w{8}-\w{4}-\w{4}-\w{4}-\w{12}",
            requests.head(p.group(0)).headers.get("location", ""),
        )
        if not v:
            continue

        ns = str(n).rjust(7, "0")
        l = f"https://coursecast-chatter.s3.us-west-2.amazonaws.com/{v.group(0)}_processed.mp4"
        yield (ns, l, t)


def write(g):
    for (ns, l, t) in process(g):
        with open(f"yuja{ns[0]}.csv", "a") as f:
            f.write(f'{ns},"{t}","{l}",\n')
            print(ns, l, t, "")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-incr", default=-1, required=False, type=int)
    parser.add_argument("-ss", type=int)
    parser.add_argument("-stop", default=-1, required=False, type=int)
    parser.add_argument("-threads", default=2, required=False, type=int)
    args = parser.parse_args()
    incr, ss, stop, th = args.incr, args.ss, args.stop, args.threads
    ths = tuple(
        threading.Thread(target=write, args=[range(ss + o * incr, stop, incr * th)])
        for o in range(0, th)
    )
    for t in ths:
        t.start()
