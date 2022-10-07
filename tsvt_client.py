import requests
import zipfile
import csv
from typing import *
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, fields
from io import BytesIO, StringIO


@dataclass
class TSVTInfo(object):
    export: bool
    period: str
    country: str
    tnved: int
    measure_unit: str
    cost: float
    weight: float
    count: int
    region: str
    federal_district: str


class _FileType(Enum):
    csv = "Csv"
    dbf = "Dbf"


class TSVTReader(object):
    def __init__(self, file_like):
        data_str = StringIO(file_like.read().decode('utf-8-sig'))
        self._reader = csv.reader(data_str, delimiter='\t')
        next(self._reader)  # skip title

    def __iter__(self):
        return self

    def __next__(self):
        record = next(self._reader)
        data = {field.name: record[i] for i, field in enumerate(fields(TSVTInfo))}
        data["export"] = data["export"] == 'ЭК'
        return TSVTInfo(**data)


class TSVTScraper(object):
    _UNLOAD_DATA_ENDPOINT = "http://stat.customs.gov.ru/api/DataAnalysis/UnloadData"

    def __init__(self):
        self._session = requests.Session()

    def _download_data(self,
                       period: Tuple[datetime, datetime],
                       federal_districts: Optional[List] = list(),
                       regions: Optional[List] = list(),
                       tnved_level: int = 2,
                       _file_type: _FileType = _FileType.csv) -> BytesIO:
        payload = {
            "exportType": _file_type.value,
            "tnved": [],
            "tnvedLevel": tnved_level,
            "federalDistricts": federal_districts,
            "subjects": regions,
            "direction": "",
            "period": [
                {
                    "start": period[0].strftime("%Y-%m-%d"),
                    "end": period[1].strftime("%Y-%m-%d")
                }
            ]
        }

        response = self._session.post(url=self._UNLOAD_DATA_ENDPOINT, json=payload)
        assert response.status_code == 200

        archive_file_like = BytesIO(response.content)
        archive = zipfile.ZipFile(archive_file_like)

        archive_filenames = archive.namelist()
        assert len(archive_filenames) == 1

        data = archive.open(archive_filenames[0]).read()

        return BytesIO(data)

    def get_reader(self, **kwargs) -> TSVTReader:
        data = self._download_data(**kwargs)
        return TSVTReader(data)
