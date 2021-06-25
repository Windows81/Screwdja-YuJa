from datetime import datetime
from matplotlib import pyplot
from matplotlib import rcParams
import regex
import csv
import sys
import glob

f = [open(n, "r", encoding="cp850") for n in glob.glob("yuja?.csv")]
g = (str(l) for i, s in enumerate(f) for j, l in enumerate(s) if j > 0 or i == 0)
s = csv.DictReader(g, delimiter=",", quotechar='"')

dates, dates_flt, dates_ids = [], [], []
o = sys.argv[1] if len(sys.argv) > 1 else input("Enter a program ID: ")
rcParams["toolbar"] = "None"

if o == "dateplot":
    for r in s:
        try:
            m = regex.search("GMT(\\d{8}-\\d{6})", r["name"])
            if m:
                d = datetime.strptime(m.groups()[0], "%Y%m%d-%H%M%S")
                dates.append(tuple((int(r["id"]), d)))
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
    ids = sorted([int(r["id"]) for r in s])
    p = pyplot.plot(ids[1:], [b - a for a, b in zip(ids, ids[1:])])
    pyplot.ticklabel_format(style="plain")
    p[0].figure.tight_layout()
    pyplot.show()

elif o == "hist":
    ids = sorted([int(r["id"]) for r in s])
    p = pyplot.hist(ids, 200)
    pyplot.ticklabel_format(style="plain")
    pyplot.show()

elif o == "dateprop":
    ids = sorted([int(r["id"]) for r in s])
    props = [i / (v - ids[0]) for i, v in enumerate(ids[10:], 10)]
    p = pyplot.plot(ids[10:], props)
    pyplot.ticklabel_format(axis="x", style="plain")
    p[0].figure.tight_layout()
    pyplot.show()

elif o == "dateprop-rev":
    ids = sorted([int(r["id"]) for r in s], reverse=True)
    props = [i / (ids[0] - v) for i, v in enumerate(ids[10:], 10)]
    p = pyplot.plot(ids[10:], props)
    pyplot.ticklabel_format(axis="x", style="plain")
    p[0].figure.tight_layout()
    pyplot.show()

elif o == "bounds":
    mn, mx = sys.maxsize, 0
    for r in s:
        i = int(r["id"])
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

for s in f:
    del s
