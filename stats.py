from datetime import datetime
from matplotlib import pyplot
from matplotlib import rcParams
import re
import sys
import util

s = util.csv_streams().merge_stream
dates, dates_flt, dates_ids = [], [], []
o = sys.argv[1] if len(sys.argv) > 1 else input("Enter a program ID: ")
rcParams["toolbar"] = "None"

if o == "dateplot":
    for r in s:
        try:
            m = re.search("GMT(\\d{8}-\\d{6})", r["name"])
            if m:
                d = datetime.strptime(m.groups()[0], "%Y%m%d-%H%M%S")
                dates.append(tuple((int(r['video_id']), d)))
        except Exception:
            pass

    dates.sort()
    for [i, d] in dates:
        if not len(dates_flt) or dates_flt[-1] < d:
            dates_ids.append(i)
            dates_flt.append(d)

    p = pyplot.plot_date(dates_flt, dates_ids, "-")
    pyplot.ticklabel_format(axis="y", style="plain")
    pyplot.xticks(rotation=90)
    p[0].figure.tight_layout()
    pyplot.show()

elif o == "diffplot":
    ids = sorted([int(r['video_id']) for r in s])
    p = pyplot.plot(ids[1:], [b - a for a, b in zip(ids, ids[1:])])
    pyplot.ticklabel_format(style="plain")
    p[0].figure.tight_layout()
    pyplot.show()

elif o == "hist":
    ids = sorted([int(r['video_id']) for r in s])
    p = pyplot.hist(ids, 200)
    pyplot.ticklabel_format(style="plain")
    pyplot.show()

elif o == "dateprop":
    ids = sorted([int(r['video_id']) for r in s])
    props = [i / (v - ids[0]) for i, v in enumerate(ids[10:], 10)]
    p = pyplot.plot(ids[10:], props)
    pyplot.ticklabel_format(axis="x", style="plain")
    p[0].figure.tight_layout()
    pyplot.show()

elif o == "dateprop-rev":
    ids = sorted([int(r['video_id']) for r in s], reverse=True)
    props = [i / (ids[0] - v) for i, v in enumerate(ids[10:], 10)]
    p = pyplot.plot(ids[10:], props)
    pyplot.ticklabel_format(axis="x", style="plain")
    p[0].figure.tight_layout()
    pyplot.show()

elif o == "bounds":
    mn, mx = sys.maxsize, 0
    for r in s:
        i = int(r['video_id'])
        if mn > i:
            mn = i
        if mx < i:
            mx = i
    print(mn)
    print(mx)

elif o == "count":
    c = 0
    for _ in s:
        c += 1
    print(c)

elif o == "fraction":
    c, mn, mx = 0, sys.maxsize, 0
    for r in s:
        i = int(r['video_id'])
        if mn > i:
            mn = i
        if mx < i:
            mx = i
        c += 1
    print(c / mx)

elif o == "percent":
    c, mn, mx = 0, sys.maxsize, 0
    for r in s:
        i = int(r['video_id'])
        if mn > i:
            mn = i
        if mx < i:
            mx = i
        c += 1
    print(f"{100 * c / (mx-mn)}%")

for s in f:
    del s
