import util
s = util.csv_streams(lambda vid: f"yuja{int(vid/5e5)*5:02d}.csv").merge_stream
q = util.file_queue(lambda vid: f"csv/{int(vid)//1_0000:04d}.csv")
for d in s:
    q.add(util.csv_struct(**d))  # type:ignore
