if __name__ == "__main__":

    import csv
    import os
    from collections import defaultdict

    polygons = defaultdict(dict)

    with open(
        os.getenv("HOME") + "/Desktop/MGRS_100K_AUS Extract_Extract.csv",
        encoding="utf-16",
    ) as csvfile:
        spamreader = csv.reader(csvfile, delimiter="\t")
        for idx, row in enumerate(spamreader):

            if idx > 0:

                zone, mgrs, point_id, polygon_id, sq, type_, dLat, dLng = row

                polygons[zone, sq].update(
                    {point_id: (zone, mgrs, sq, type_, dLat, dLng)}
                )

        import ipdb

        ipdb.set_trace()
