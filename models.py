import peewee

database_proxy = peewee.Proxy()


class MeasureUnit(peewee.Model):
    id = peewee.CharField(unique=True, primary_key=True, max_length=3)
    name = peewee.CharField(null=False)

    class Meta:
        database = database_proxy


class TNVED(peewee.Model):
    id = peewee.CharField(unique=True, primary_key=True)
    name = peewee.CharField()

    class Meta:
        database = database_proxy


class Region(peewee.Model):
    id = peewee.CharField(unique=True, primary_key=True, max_length=5)
    name = peewee.CharField(null=False)

    class Meta:
        database = database_proxy


class FederalDistrict(peewee.Model):
    id = peewee.CharField(unique=True, primary_key=True, max_length=2)
    name = peewee.CharField(null=False)

    class Meta:
        database = database_proxy


class Country(peewee.Model):
    id = peewee.CharField(unique=True, primary_key=True, max_length=2)
    name = peewee.CharField(unique=True, null=False)

    class Meta:
        database = database_proxy


class TSVTRecord(peewee.Model):
    export = peewee.BooleanField()
    period = peewee.CharField()
    country = peewee.CharField()
    tnved = peewee.ForeignKeyField(TNVED, backref='tsvt_records')
    measure_unit = peewee.ForeignKeyField(MeasureUnit, backref='tsvt_records')
    cost = peewee.FloatField()
    weight = peewee.FloatField()
    count = peewee.IntegerField()
    region = peewee.ForeignKeyField(Region, backref='tsvt_records')
    federal_district = peewee.ForeignKeyField(FederalDistrict, backref='tsvt_records')

    class Meta:
        database = database_proxy
