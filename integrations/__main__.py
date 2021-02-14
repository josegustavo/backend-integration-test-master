# -*- coding: utf-8 -*-
from config.args import Args
from richart_wholesale_club.ingestion import Ingestion

if __name__ == "__main__":
    args = Args()
    app = Ingestion(args)
    app.process_csv_files()