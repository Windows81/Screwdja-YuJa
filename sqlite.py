import csv
import glob
import util
import sqlite3
FILE_NAME = 'yuja.sqlite'


def main() -> None:
    connection = sqlite3.connect(FILE_NAME)
    cursor = connection.cursor()
    f = [open(n, "r", encoding="utf-8") for n in glob.glob("yuja*.csv")]
    g = (str(l) for i, s in enumerate(f) for j, l in enumerate(s) if j > 0 or i == 0)
    s = csv.DictReader(g, delimiter=",", quotechar='"')

    annotations = {
        f: {int: "integer", str: "string"}.get(t, '')
        for f, t in util.csv_struct.__annotations__.items()
    }
    annotations['video_id'] += ' primary key'
    annotations['creation'] = 'timestamp'
    annotations['modification'] = 'timestamp'

    annotation_keys = list(annotations.keys())
    #create_names = [f'{f} {t}' for f, t in annotations.items()]
    #create_table = f'CREATE TABLE IF NOT EXISTS yuja({",".join(create_names)})'
    #cursor.execute('DROP TABLE yuja')
    # cursor.execute(create_table)
    insert_records = f"REPLACE INTO yuja({','.join(annotation_keys)}) VALUES({','.join(f':{n}' for n in annotation_keys)})"
    cursor.executemany(insert_records, s)
    connection.commit()
    connection.close()


if __name__ == '__main__':
    main()
