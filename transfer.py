import util
def transfer(s, q):
    for d in s:
        q.add(util.csv_struct(**d))  # type:ignore

if __name__ == "__main__":
    #l1 = lambda vid: f"yuja{int(vid/5e5)*5:02d}.csv"
    l1 = lambda vid: f"csv/{int(vid)//1_0000:04d}..csv"
    l2 = lambda vid: f"csv/{int(vid)//1_0000:04d}.csv"
    s = util.csv_streams(l1).merge_stream
    q = util.file_queue(l2)
    transfer(s, q)
