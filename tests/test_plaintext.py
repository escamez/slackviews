"""
Class with nosetests for PlainText AbstractBlock in slack_view library
"""

from nose.tools import raises

from slackviews.view import PlainText

__author__ = 'Agustin Escamez'
__email__ = 'aech22@gmail.com'


class TestPlainText:

    def teardown(self):
        PlainText.__all_slots__ = None

    def test_should_plaintext_builder_provide_a_valid_instance_with_required_values(self):

        # GIVEN
        expected_slots = ['_emoji']
        expected_all_slots = ['_text']
        expected_all_slots.extend(expected_slots)

        # WHEN
        instance = PlainText.Builder().build()

        # THEN
        assert hasattr(instance, '__all_slots__')
        assert hasattr(instance, '__slots__')
        for att in expected_slots:
            assert att in getattr(instance, '__slots__')
        for att in expected_all_slots:
            assert att in getattr(instance, '__all_slots__')

        assert getattr(instance, '_emoji') is False

    @raises(AttributeError)
    def test_should_plaintext_serialize_raise_attributeerror_if_trying_to_serialize_without_all_required_slots(self):

        # WHEN
        PlainText.Builder().build().serialize()

    def test_should_plaintext_builder_provide_a_valid_instance_with_supplied_values(self):

        # GIVEN
        expected_text = 'any text'
        expected_emoji = True

        # WHEN
        instance = PlainText.Builder().text(expected_text).emoji_(expected_emoji).build()

        # THEN
        assert getattr(instance, '_emoji') is expected_emoji
        assert getattr(instance, '_text') is expected_text

    def test_should_plaintext_serialize_provide_correct_dict_and_json_data(self):

        # GIVEN
        expected_serialized_dict = {'type': 'plain_text', 'text': 'any text', 'emoji': False}
        expected_serialized_json = '{"type": "plain_text", "text": "any text", "emoji": false}'
        instance = PlainText.Builder().text('any text').build()

        # WHEN
        serialized_dict = instance.serialize()
        serialized_json = instance.serialize(as_json=True)

        # THEN
        assert serialized_dict == expected_serialized_dict
        assert serialized_json == expected_serialized_json

    def test_should_plaintext_deserialize_provide_correct_instances_from_dict_and_json(self):

        # GIVEN
        serialized_dict = {'type': 'plain_text', 'text': 'any text', 'emoji': False}
        serialized_json = '{"type": "plain_text", "text": "any text", "emoji": false}'

        # WHEN
        instance_from_dict = PlainText.deserialize(serialized_dict)
        instance_from_json = PlainText.deserialize(serialized_json, from_json=True)

        # THEN
        assert isinstance(instance_from_dict, PlainText) and isinstance(instance_from_json, PlainText)
        assert getattr(instance_from_dict, '_text') == 'any text'
        assert getattr(instance_from_json, '_text') == 'any text'
        assert getattr(instance_from_dict, '_emoji') is False
        assert getattr(instance_from_json, '_emoji') is False
