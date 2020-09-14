"""
Class with nosetests for Option AbstractBlock in slack_view library
"""

from nose.tools import raises

from slackviews.view import Option, PlainText

__author__ = 'Agustin Escamez'
__email__ = 'aech22@gmail.com'


class TestOption:

    def teardown(self):
        Option.__all_slots__ = None

    def test_should_option_builder_provide_a_valid_instance_with_required_values(self):

        # GIVEN
        expected_slots = ['_text', '_value']
        expected_all_slots = ['_description', '_url']
        expected_all_slots.extend(expected_slots)
        expected_text = 'any text'
        expected_value = 'any value'

        # WHEN
        instance = Option.Builder().text(expected_text).value(expected_value).build()

        # THEN
        assert hasattr(instance, '__all_slots__')
        assert hasattr(instance, '__slots__')
        for att in expected_slots:
            assert att in getattr(instance, '__slots__')
        for att in expected_all_slots:
            assert att in getattr(instance, '__all_slots__')

        assert not hasattr(instance, '_description')
        assert not hasattr(instance, '_url')
        assert isinstance(getattr(instance, '_text'), PlainText)
        assert getattr(getattr(instance, '_text'), '_text') == expected_text
        assert getattr(instance, '_value') == expected_value

    @raises(AttributeError)
    def test_should_option_serialize_raise_attributeerror_if_trying_to_serialize_without_all_required_slots(self):

        # WHEN
        Option.Builder().build().serialize()

    def test_should_option_builder_provide_a_valid_instance_with_supplied_values(self):

        # GIVEN
        expected_text = 'any text'
        expected_value = 'any value'
        expected_description = 'any description'
        expected_url = 'any url'

        # WHEN
        instance = Option.Builder().text(expected_text).value(expected_value).description_(expected_description) \
            .url_(expected_url).build()

        # THEN
        assert isinstance(getattr(instance, '_text'), PlainText)
        assert getattr(getattr(instance, '_text'), '_text') == expected_text
        assert isinstance(getattr(instance, '_description'), PlainText)
        assert getattr(getattr(instance, '_description'), '_text') == expected_description
        assert getattr(instance, '_value') == expected_value
        assert getattr(instance, '_url') == expected_url

    def test_should_option_serialize_provide_correct_dict_and_json_data(self):

        # GIVEN
        expected_text = 'any text'
        expected_value = 'any value'
        expected_description = 'any description'
        expected_url = 'any url'

        expected_serialized_dict = {'url': expected_url, 'description': {'type': 'plain_text',
                                                                         'text': expected_description, 'emoji': False},
                                    'value': expected_value, 'text': {'type': 'plain_text', 'text': expected_text,
                                                                      'emoji': False}}

        expected_serialized_json = f'{{"url": "{expected_url}", "description": {{"type": "plain_text", ' \
                                   f'"text": "{expected_description}", "emoji": false}}, "value": "{expected_value}", ' \
                                   f'"text": {{"type": "plain_text", "text": "{expected_text}", "emoji": false}}}}'

        instance = Option.Builder().text(expected_text).value(expected_value).description_(expected_description) \
            .url_(expected_url).build()

        # WHEN
        serialized_dict = instance.serialize()
        serialized_json = instance.serialize(as_json=True)

        # THEN
        assert serialized_dict == expected_serialized_dict
        assert serialized_json == expected_serialized_json

    def test_should_option_deserialize_provide_correct_instances_from_dict_and_json(self):

        # GIVEN
        expected_text = 'any text'
        expected_value = 'any value'
        expected_description = 'any description'
        expected_url = 'any url'

        serialized_dict = {'url': expected_url, 'description': {'type': 'plain_text',
                                                                'text': expected_description, 'emoji': False},
                           'value': expected_value, 'text': {'type': 'plain_text', 'text': expected_text,
                                                             'emoji': False}}

        serialized_json = f'{{"url": "{expected_url}", "description": {{"type": "plain_text", ' \
                          f'"text": "{expected_description}", "emoji": false}}, "value": "{expected_value}", ' \
                          f'"text": {{"type": "plain_text", "text": "{expected_text}", "emoji": false}}}}'

        # WHEN
        instance_from_dict = Option.deserialize(serialized_dict)
        instance_from_json = Option.deserialize(serialized_json, from_json=True)

        # THEN
        assert isinstance(instance_from_dict, Option)
        assert isinstance(instance_from_json, Option)
        for instance in (instance_from_dict, instance_from_json):
            assert isinstance(getattr(instance, '_text'), PlainText)
            assert getattr(getattr(instance, '_text'), '_text') == expected_text
            assert isinstance(getattr(instance, '_description'), PlainText)
            assert getattr(getattr(instance, '_description'), '_text') == expected_description
            assert getattr(instance, '_value') == expected_value
            assert getattr(instance, '_url') == expected_url

    def test_should_option_eq_compare_to_instances_correctly(self):

        # GIVEN
        expected_text = 'any text'
        expected_value = 'any value'

        option1 = Option.Builder().text(expected_text).value(expected_value).build()
        option2 = Option.Builder().text(expected_text).value(expected_value).build()

        # WHEN
        result = option1.__eq__(option2)

        # THEN
        assert result
