import peewee

database_proxy = peewee.Proxy()


class TNVED(peewee.ModelBase):
    id = peewee.CharField(unique=True)
    measure_unit = peewee.CharField()
    name = peewee.CharField()

    class Meta:
        database = database_proxy


class Region(peewee.ModelBase):
    id = peewee.CharField(unique=True)
    name = peewee.CharField()

    class Meta:
        database = database_proxy


class FederalDistrict(peewee.ModelBase):
    id = peewee.CharField(unique=True)
    name = peewee.CharField()

    class Meta:
        database = database_proxy


class TSVTRecord(peewee.ModelBase):
    export = peewee.BooleanField()
    period = peewee.CharField()
    country = peewee.CharField()
    tnved = peewee.ForeignKeyField(TNVED, backref='tsvt_records')
    cost = peewee.FloatField()
    weight = peewee.FloatField()
    count = peewee.IntegerField()
    region = peewee.ForeignKeyField(Region, backref='tsvt_records')
    federal_district = peewee.ForeignKeyField(FederalDistrict, backref='tsvt_records')

    class Meta:
        database = database_proxy
