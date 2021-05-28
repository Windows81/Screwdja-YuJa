from datetime import datetime
from matplotlib import pyplot
from matplotlib import rcParams
import regex
import csv

with open("yuja.csv", "r", encoding="cp850") as f:
    s = csv.DictReader(f, delimiter=",", quotechar='"')
    rcParams["toolbar"] = "None"
    dates, dates_flt, dates_ids = [], [], []
    o = input("Enter a program ID: ")

    if o == "0":
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

        p = pyplot.plot_date(dates_flt, dates_ids, "b-")
        pyplot.ticklabel_format(axis="y", style="plain")
        pyplot.xticks(rotation=90)
        p[0].figure.tight_layout()
        pyplot.show()

    elif o == "1":
        ids = sorted([int(r["id"]) for r in s])
        p = pyplot.plot(ids[1:], [b - a for a, b in zip(ids, ids[1:])])
        pyplot.ticklabel_format(style="plain")
        p[0].figure.tight_layout()
        pyplot.show()

    elif o == "2":
        ids = sorted([int(r["id"]) for r in s])
        p = pyplot.hist(ids, 200)
        pyplot.ticklabel_format(style="plain")
        pyplot.show()

    elif o == "3":
        ids = sorted([int(r["id"]) for r in s])
        props = [i / (v - ids[0]) for i, v in enumerate(ids[10:], 10)]
        p = pyplot.plot(ids[10:], props)
        pyplot.ticklabel_format(axis="x", style="plain")
        p[0].figure.tight_layout()
        pyplot.show()

    elif o == "3.5":
        ids = sorted([int(r["id"]) for r in s], reverse=True)
        props = [i / (ids[0] - v) for i, v in enumerate(ids[10:], 10)]
        p = pyplot.plot(ids[10:], props)
        pyplot.ticklabel_format(axis="x", style="plain")
        p[0].figure.tight_layout()
        pyplot.show()
