# Welcome to YuJa Heaven!

This is a scraper built to collect lectures, meetings, and relevant third-party vieos uploaded by mostly-US institutions onto YuJa's cloud-storage program. A previous version existed which only worked with ~35% of available videos. Remember kids: **security through obscurity is _not_ really security.** It's insecurity and conceitedness in disguise.

Once you have built a C.S.V. collection, run `sqlite.py` to generate a SQLite database (complete with views and schemas) that you can navigate through. You can also use Excel and make an access database with the files.

```
https://uci.yuja.com/P/Data/VideoSource?video=/P/VideoCaptures/a/1/{broadcast_id}/{auth}&videoPID={video_id}&mp4Only=true&includeThumbnails=false
```
