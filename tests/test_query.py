from unittest import TestCase

from mockfirestore import MockFirestore


class TestStream(TestCase):
    def setUp(self):
        self.store = MockFirestore()
        self.store._data = {
            'foo': {
                'first': {'id': 1, 'value': 'number one'},
                'second': {'id': 2},
            }
        }

    def test_basic(self):
        results = list(self.store.collection('foo').where('id', '==', 1).stream())
        assert len(results) == 1
        assert results[0].to_dict() == {'id': 1, 'value': 'number one'}

    def test_handles_non_equality_mismatch(self):
        # NOTE: This is the closest to non-equality we can do for firestore
        # (source: https://stackoverflow.com/a/48481812/13340678), and is essentially conducting
        # a presence test.
        results = list(self.store.collection('foo').where('value', '>', '').stream())
        assert len(results) == 1
        assert results[0].to_dict() == {'id': 1, 'value': 'number one'}
