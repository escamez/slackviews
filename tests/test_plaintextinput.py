"""
Class with nosetests for PlainTextInput AbstractBlock in slack_view library
"""
from nose.tools import raises

from slackviews.view import PlainTextInput, PlainText

__author__ = 'Agustin Escamez'
__email__ = 'aech22@gmail.com'


class TestPlainTextInput:

    def setup(self):

        self.expected_action_id = 'any action id'
        self.expected_placeholder = 'any place holder'
        self.expected_multiline = True
        self.expected_initial_value = 'any initial value'
        self.expected_min_length = 1
        self.expected_max_length = 2

        self.plaintextinput_instance_required = PlainTextInput.Builder().action_id(self.expected_action_id).build()
        self.plaintextinput_instance_all = PlainTextInput.Builder().action_id(self.expected_action_id) \
            .placeholder_(self.expected_placeholder).multiline_(self.expected_multiline) \
            .initial_value_(self.expected_initial_value).min_length_(self.expected_min_length) \
            .max_length_(self.expected_max_length).build()

        self.expected_serialized_dict = {'type': 'plain_text_input', 'max_length': self.expected_max_length,
                                         'min_length': self.expected_min_length, 'multiline': self.expected_multiline,
                                         'initial_value': self.expected_initial_value,
                                         'placeholder': {'type': 'plain_text', 'text': self.expected_placeholder,
                                                         'emoji': False}, 'action_id': self.expected_action_id}

        self.expected_serialized_json = f'{{"type": "plain_text_input", "max_length": {self.expected_max_length}, ' \
                                        f'"min_length": {self.expected_min_length}, ' \
                                        f'"multiline": {str(self.expected_multiline).lower()}, ' \
                                        f'"initial_value": "{self.expected_initial_value}", ' \
                                        f'"placeholder": {{"type": "plain_text", ' \
                                        f'"text": "{self.expected_placeholder}", "emoji": false}}, ' \
                                        f'"action_id": "{self.expected_action_id}"}}'

    def teardown(self):
        PlainTextInput.__all_slots__ = None

    def test_should_plaintextinput_builder_provide_a_valid_instance_with_required_values(self):

        # GIVEN
        expected_slots = ['_action_id']
        expected_all_slots = ['_placeholder', '_initial_value', '_multiline', '_min_length', '_max_length']
        expected_all_slots.extend(expected_slots)

        # WHEN
        instance = self.plaintextinput_instance_required

        # THEN
        assert isinstance(instance, PlainTextInput)
        assert hasattr(instance, '__all_slots__')
        assert hasattr(instance, '__slots__')
        for att in expected_slots:
            assert att in getattr(instance, '__slots__')
        for att in expected_all_slots:
            assert att in getattr(instance, '__all_slots__')

        assert getattr(instance, '_action_id') == self.expected_action_id
        assert not hasattr(instance, '_placeholder')
        assert not hasattr(instance, '_initial_value')
        assert not hasattr(instance, '_multiline')
        assert not hasattr(instance, '_min_length')
        assert not hasattr(instance, '_max_length')

    def test_should_plaintextinput_builder_provide_a_valid_instance_with_any_values(self):

        # GIVEN
        instance = self.plaintextinput_instance_all

        # THEN
        assert getattr(instance, '_action_id') == self.expected_action_id
        assert isinstance(getattr(instance, '_placeholder'), PlainText)
        assert getattr(getattr(instance, '_placeholder'), '_text') == self.expected_placeholder
        assert getattr(instance, '_initial_value') == self.expected_initial_value
        assert getattr(instance, '_multiline') == self.expected_multiline
        assert getattr(instance, '_min_length') == self.expected_min_length
        assert getattr(instance, '_max_length') == self.expected_max_length

    @raises(AttributeError)
    def test_should_plaintextinput_serialize_raise_attributeerror_if_serialize_without_action_id(self):

        # WHEN
        PlainTextInput.Builder().build().serialize()

    @raises(AssertionError)
    def test_should_plaintextinput_serialize_raise_assertionerror_if_multiline_is_not_boolean(self):

        # WHEN
        PlainTextInput.Builder().action_id('any').multiline_('1').build().serialize()

    @raises(AssertionError)
    def test_should_plaintextinput_serialize_raise_assertionerror_if_min_length_is_not_integer(self):

        # WHEN
        PlainTextInput.Builder().action_id('any').min_length_('1').build().serialize()

    @raises(AssertionError)
    def test_should_plaintextinput_serialize_raise_assertionerror_if_max_length_is_not_integer(self):

        # WHEN
        PlainTextInput.Builder().action_id('any').max_length_('1').build().serialize()

    def test_should_plaintextinput_serialize_provide_correct_dict_and_json_data(self):

        # GIVEN
        instance = self.plaintextinput_instance_all

        # WHEN
        serialized_dict = instance.serialize()
        serialized_json = instance.serialize(as_json=True)

        # THEN
        assert serialized_dict == self.expected_serialized_dict
        assert serialized_json == self.expected_serialized_json

    def test_should_plaintextinput_deserialize_provide_correct_instances_from_dict_and_json(self):

        # GIVEN
        serialized_dict = self.expected_serialized_dict
        serialized_json = self.expected_serialized_json

        # WHEN
        instance_from_dict = PlainTextInput.deserialize(serialized_dict)
        instance_from_json = PlainTextInput.deserialize(serialized_json, from_json=True)

        # THEN
        assert isinstance(instance_from_dict, PlainTextInput)
        assert isinstance(instance_from_json, PlainTextInput)
        for instance in (instance_from_dict, instance_from_json):
            assert getattr(instance, '_action_id') == self.expected_action_id
            assert isinstance(getattr(instance, '_placeholder'), PlainText)
            assert getattr(getattr(instance, '_placeholder'), '_text') == self.expected_placeholder
            assert getattr(instance, '_initial_value') == self.expected_initial_value
            assert getattr(instance, '_multiline') == self.expected_multiline
            assert getattr(instance, '_min_length') == self.expected_min_length
            assert getattr(instance, '_max_length') == self.expected_max_length
