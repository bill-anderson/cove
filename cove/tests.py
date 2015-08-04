import pytest
import cove.views as v
import os
import json
from cove.input.models import SuppliedData
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile, UploadedFile


def test_get_releases_aggregates():
    assert v.get_releases_aggregates({}) == {
        'count': 0,
        'unique_ocids': [],
        'earliest_release_date': None,
        'latest_release_date': None
    }
    assert v.get_releases_aggregates({'releases': []}) == {
        'count': 0,
        'unique_ocids': set([]),
        'earliest_release_date': None,
        'latest_release_date': None
    }
    assert v.get_releases_aggregates({'releases': [{}, {}, {}]}) == {
        'count': 3,
        'unique_ocids': set([]),
        'earliest_release_date': None,
        'latest_release_date': None
    }


def test_get_file_type_xlsx():
    with open(os.path.join('cove', 'fixtures', 'basic.xlsx')) as fp:
        assert v.get_file_type(UploadedFile(fp, 'basic.xlsx')) == 'xlsx'


def test_get_file_type_csv():
    assert v.get_file_type(SimpleUploadedFile('test.csv', b'a,b')) == 'csv'


def test_get_file_type_json():
    assert v.get_file_type(SimpleUploadedFile('test.json', b'{}')) == 'json'


def test_get_file_type_json_noextension():
    assert v.get_file_type(SimpleUploadedFile('test', b'{}')) == 'json'


def test_get_file_unrecognised_file_type():
    with pytest.raises(v.UnrecognisedFileType):
        v.get_file_type(SimpleUploadedFile('test', b'test'))


@pytest.mark.xfail
def test_get_schema_validation_errors():
    schema_url = 'http://ocds.open-contracting.org/standard/r/1__0__RC/release-package-schema.json'
    with open(os.path.join('cove', 'fixtures', 'tenders_releases_2_releases.json')) as fp:
        error_list = v.get_schema_validation_errors(json.load(fp), schema_url)
        assert len(error_list) == 0
    with open(os.path.join('cove', 'fixtures', 'tenders_releases_2_releases_invalid.json')) as fp:
        error_list = v.get_schema_validation_errors(json.load(fp), schema_url)
        assert len(error_list) > 0


@pytest.mark.django_db
def test_explore_page(client):
    data = SuppliedData.objects.create()
    data.original_file.save('test.json', ContentFile('{}'))
    resp = client.get(data.get_absolute_url())
    assert resp.status_code == 200
    assert resp.context['conversion'] == 'flatten'


@pytest.mark.django_db
def test_explore_page_csv(client):
    data = SuppliedData.objects.create()
    data.original_file.save('test.csv', ContentFile('a,b'))
    resp = client.get(data.get_absolute_url())
    assert resp.status_code == 200
    assert resp.context['conversion'] == 'unflatten'


@pytest.mark.django_db
def test_explore_not_json(client):
    data = SuppliedData.objects.create()
    with open(os.path.join('cove', 'fixtures', 'tenders_releases_2_releases_not_json.json')) as fp:
        data.original_file.save('test.json', UploadedFile(fp))
    resp = client.get(data.get_absolute_url())
    assert resp.status_code == 200
    assert b'not well formed JSON' in resp.content
