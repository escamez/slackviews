"""
Class with nosetests for Divider AbstractBlock in slack_view library
"""

from slackviews.view import Divider

__author__ = 'Agustin Escamez'
__email__ = 'aech22@gmail.com'


class TestDivider:

    def teardown(self):
        Divider.__all_slots__ = None

    def setup(self):
        self.expected_block_id = 'any block id'
        self.serialized_dict = {'type': 'divider', 'block_id': self.expected_block_id}
        self.serialized_json = f'{{"type": "divider", "block_id": "{self.expected_block_id}"}}'

    def test_should_divider_builder_provide_a_valid_instance(self):

        # GIVEN
        expected_slots = ['_block_id']
        expected_all_slots = expected_slots

        # WHEN
        instance = Divider.Builder().block_id_(self.expected_block_id).build()

        # THEN
        assert hasattr(instance, '__all_slots__')
        assert hasattr(instance, '__slots__')
        for att in expected_slots:
            assert att in getattr(instance, '__slots__')
        for att in expected_all_slots:
            assert att in getattr(instance, '__all_slots__')

        assert isinstance(instance, Divider)
        assert getattr(instance, '_block_id') == self.expected_block_id

    def test_should_divider_serialize_provide_correct_dict_and_json_data(self):

        # GIVEN
        expected_serialized_dict = self.serialized_dict
        expected_serialized_json = self.serialized_json
        instance = Divider.Builder().block_id_(self.expected_block_id).build()

        # WHEN
        serialized_dict = instance.serialize()
        serialized_json = instance.serialize(as_json=True)

        # THEN
        assert serialized_dict == expected_serialized_dict
        assert serialized_json == expected_serialized_json

    def test_should_divider_deserialize_provide_correct_instances_from_dict_and_json(self):

        # GIVEN
        serialized_dict = self.serialized_dict
        serialized_json = self.serialized_json

        # WHEN
        instance_from_dict = Divider.deserialize(serialized_dict)
        instance_from_json = Divider.deserialize(serialized_json, from_json=True)

        # THEN
        assert isinstance(instance_from_dict, Divider) and isinstance(instance_from_json, Divider)
        for instance in (instance_from_dict, instance_from_json):
            assert getattr(instance, '_block_id') == self.expected_block_id
