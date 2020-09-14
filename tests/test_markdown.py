"""
Class with nosetests for MarkDown AbstractBlock in slack_view library
"""

from nose.tools import raises

from slackviews.view import MarkDown

__author__ = 'Agustin Escamez'
__email__ = 'aech22@gmail.com'


class TestMarkDown:

    def teardown(self):
        MarkDown.__all_slots__ = None

    def test_should_markdown_builder_provide_a_valid_instance_with_required_values(self):

        # GIVEN
        expected_slots = ['_verbatim']
        expected_all_slots = ['_text']
        expected_all_slots.extend(expected_slots)

        # WHEN
        instance = MarkDown.Builder().build()

        # THEN
        assert hasattr(instance, '__all_slots__')
        assert hasattr(instance, '__slots__')
        for att in expected_slots:
            assert att in getattr(instance, '__slots__')
        for att in expected_all_slots:
            assert att in getattr(instance, '__all_slots__')

        assert getattr(instance, '_verbatim') is False

    @raises(AttributeError)
    def test_should_markdown_serialize_raise_attributeerror_if_trying_to_serialize_without_all_required_slots(self):

        # WHEN
        MarkDown.Builder().build().serialize()

    def test_should_markdown_builder_provide_a_valid_instance_with_supplied_values(self):

        # GIVEN
        expected_text = 'any text'
        expected_verbatim = True

        # WHEN
        instance = MarkDown.Builder().text(expected_text).verbatim_(expected_verbatim).build()

        # THEN
        assert getattr(instance, '_verbatim') is expected_verbatim
        assert getattr(instance, '_text') is expected_text

    def test_should_markdown_serialize_provide_correct_dict_and_json_data(self):

        # GIVEN
        expected_serialized_dict = {'type': 'mrkdwn', 'text': 'any text', 'verbatim': False}
        expected_serialized_json = '{"type": "mrkdwn", "text": "any text", "verbatim": false}'
        instance = MarkDown.Builder().text('any text').build()

        # WHEN
        serialized_dict = instance.serialize()
        serialized_json = instance.serialize(as_json=True)

        # THEN
        assert serialized_dict == expected_serialized_dict
        assert serialized_json == expected_serialized_json

    def test_should_markdown_deserialize_provide_correct_instances_from_dict_and_json(self):

        # GIVEN
        serialized_dict = {'type': 'mrkdwn', 'text': 'any text', 'verbatim': False}
        serialized_json = '{"type": "mrkdwn", "text": "any text", "verbatim": false}'

        # WHEN
        instance_from_dict = MarkDown.deserialize(serialized_dict)
        instance_from_json = MarkDown.deserialize(serialized_json, from_json=True)

        # THEN
        assert isinstance(instance_from_dict, MarkDown) and isinstance(instance_from_json, MarkDown)
        assert getattr(instance_from_dict, '_text') == 'any text'
        assert getattr(instance_from_json, '_text') == 'any text'
        assert getattr(instance_from_dict, '_verbatim') is False
        assert getattr(instance_from_json, '_verbatim') is False
