"""
Class with nosetests for Header AbstractBlock in slack_view library
"""

from nose.tools import raises

from slackviews.view import Header, PlainText

__author__ = 'Agustin Escamez'
__email__ = 'aech22@gmail.com'


class TestHeader:

    def teardown(self):
        Header.__all_slots__ = None

    def test_should_header_builder_provide_a_valid_instance_with_required_values(self):

        # GIVEN
        expected_slots = ['_text']
        expected_all_slots = ['_text', '_block_id']
        expected_all_slots.extend(expected_slots)
        expected_text = 'any text'

        # WHEN
        instance = Header.Builder().text(expected_text).build()

        # THEN
        assert hasattr(instance, '__all_slots__')
        assert hasattr(instance, '__slots__')
        for att in expected_slots:
            assert att in getattr(instance, '__slots__')
        for att in expected_all_slots:
            assert att in getattr(instance, '__all_slots__')

        assert not hasattr(instance, '_block_id')
        assert isinstance(getattr(instance, '_text'), PlainText)
        assert getattr(getattr(instance, '_text'), '_text') == expected_text


    @raises(AttributeError)
    def test_should_header_serialize_raise_attributeerror_if_trying_to_serialize_without_all_required_slots(self):

        # WHEN
        Header.Builder().build().serialize()

    def test_should_header_builder_provide_a_valid_instance_with_supplied_values(self):

        # GIVEN
        expected_text = 'any text'
        expected_block_id = 'any block id'

        # WHEN
        instance = Header.Builder().text(expected_text).block_id_(expected_block_id).build()

        # THEN
        assert getattr(instance, '_block_id') is expected_block_id
        assert getattr(getattr(instance, '_text'), '_text') == expected_text

    def test_should_header_serialize_provide_correct_dict_and_json_data(self):

        # GIVEN
        expected_serialized_dict = {'type': 'header', 'block_id': 'any block_id',
                                    'text': {'type': 'plain_text', 'text': 'any text', 'emoji': False}}
        expected_serialized_json = '{"type": "header", "block_id": "any block_id", ' \
                                   '"text": {"type": "plain_text", "text": "any text", "emoji": false}}'
        instance = Header.Builder().text('any text').block_id_('any block_id').build()

        # WHEN
        serialized_dict = instance.serialize()
        serialized_json = instance.serialize(as_json=True)

        # THEN
        assert serialized_dict == expected_serialized_dict
        assert serialized_json == expected_serialized_json

    def test_should_header_deserialize_provide_correct_instances_from_dict_and_json(self):

        # GIVEN
        serialized_dict = {'type': 'header', 'block_id': 'any block_id',
                                    'text': {'type': 'plain_text', 'text': 'any text', 'emoji': False}}
        serialized_json = '{"type": "header", "block_id": "any block_id", ' \
                                   '"text": {"type": "plain_text", "text": "any text", "emoji": false}}'

        # WHEN
        instance_from_dict = Header.deserialize(serialized_dict)
        instance_from_json = Header.deserialize(serialized_json, from_json=True)

        # THEN
        assert isinstance(instance_from_dict, Header) and isinstance(instance_from_json, Header)
        assert isinstance(getattr(instance_from_dict, '_text'), PlainText)
        assert getattr(getattr(instance_from_dict, '_text'), '_text') == 'any text'
        assert getattr(instance_from_dict, '_block_id') == 'any block_id'
        assert isinstance(getattr(instance_from_json, '_text'), PlainText)
        assert getattr(getattr(instance_from_json, '_text'), '_text') == 'any text'
        assert getattr(instance_from_json, '_block_id') == 'any block_id'
