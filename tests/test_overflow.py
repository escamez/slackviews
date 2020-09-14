"""
Class with nosetests for Overflow AbstractBlock in slack_view library
"""
from nose.tools import raises

from slackviews.view import Option, Overflow, Confirmation

__author__ = 'Agustin Escamez'
__email__ = 'aech22@gmail.com'


class TestOverflow:

    def setup(self):

        self.expected_action_id = 'any action id'

        self.expected_option0_text = 'option 1 text'
        self.expected_option0_value = 'option 1 value'
        self.expected_option1_text = 'option 2 text'
        self.expected_option1_value = 'option 2 value'

        self.expected_confirmation_title = 'any title'
        self.expected_confirmation_confirm = 'any cofirm'
        self.expected_confirmation_deny = 'any deny'
        self.expected_confirmation_text = 'any text'

        self.expected_option0 = Option.Builder().text(self.expected_option0_text).value(self.expected_option0_value) \
            .build()
        self.expected_option1 = Option.Builder().text(self.expected_option1_text).value(self.expected_option1_value) \
            .build()
        self.expected_options = [self.expected_option0, self.expected_option1]

        # -- instance with required fields
        _builder = Overflow.Builder().action_id(self.expected_action_id)
        for opt_ in self.expected_options:
            _builder.Option().text(getattr(getattr(opt_, '_text'), '_text')).value(getattr(opt_, '_value'))

        self.overflow_instance_required = _builder.build()

        # -- instance with all fields
        _builder = Overflow.Builder().action_id(self.expected_action_id)
        for opt_ in self.expected_options:
            _builder.Option().text(getattr(getattr(opt_, '_text'), '_text')).value(getattr(opt_, '_value'))

        _builder.Confirm_() \
            .title(self.expected_confirmation_title) \
            .text(self.expected_confirmation_text) \
            .confirm(self.expected_confirmation_confirm) \
            .deny(self.expected_confirmation_deny)

        self.overflow_instance_all = _builder.build()

        self.expected_serialized_dict = {'type': 'overflow', 'confirm': {'deny': {'type': 'plain_text',
                                                                                  'text': 'any deny', 'emoji': False},
                                                                         'confirm': {'type': 'plain_text',
                                                                                     'text': 'any cofirm',
                                                                                     'emoji': False},
                                                                         'text': {'type': 'mrkdwn', 'text': 'any text',
                                                                                  'verbatim': False},
                                                                         'title': {'type': 'plain_text',
                                                                                   'text': 'any title',
                                                                                   'emoji': False}},
                                         'options': [{'value': 'option 1 value', 'text': {'type': 'plain_text',
                                                                                          'text': 'option 1 text',
                                                                                          'emoji': False}},
                                                     {'value': 'option 2 value', 'text': {'type': 'plain_text',
                                                                                          'text': 'option 2 text',
                                                                                          'emoji': False}}],
                                         'action_id': 'any action id'}

        self.expected_serialized_json = f'{{"type": "overflow", '\
                                        f'"confirm": {{"deny": {{"type": "plain_text", ' \
                                        f'"text": "{self.expected_confirmation_deny}", "emoji": false}}, ' \
                                        f'"confirm": {{"type": "plain_text", ' \
                                        f'"text": "{self.expected_confirmation_confirm}", "emoji": false}}, ' \
                                        f'"text": {{"type": "mrkdwn", "text": "{self.expected_confirmation_text}", '\
                                        f'"verbatim": false}}, "title": {{"type": "plain_text", ' \
                                        f'"text": "{self.expected_confirmation_title}", "emoji": false}}}}, ' \
                                        f'"options": [{{"value": "{self.expected_option0_value}", ' \
                                        f'"text": {{"type": "plain_text", "text": "{self.expected_option0_text}", ' \
                                        f'"emoji": false}}}}, {{"value": "{self.expected_option1_value}", ' \
                                        f'"text": {{"type": "plain_text", "text": "{self.expected_option1_text}", ' \
                                        f'"emoji": false}}}}], "action_id": "{self.expected_action_id}"}}'

    def teardown(self):
        Overflow.__all_slots__ = None

    def test_should_overflow_builder_provide_a_valid_instance_with_required_values(self):

        # GIVEN
        expected_slots = ['_action_id', '_options']
        expected_all_slots = ['_confirm']
        expected_all_slots.extend(expected_slots)

        # WHEN
        instance = self.overflow_instance_required

        # THEN
        assert isinstance(instance, Overflow)
        assert hasattr(instance, '__all_slots__')
        assert hasattr(instance, '__slots__')
        for att in expected_slots:
            assert att in getattr(instance, '__slots__')
        for att in expected_all_slots:
            assert att in getattr(instance, '__all_slots__')

        assert getattr(instance, '_action_id') == self.expected_action_id
        assert isinstance(getattr(instance, '_options'), list)
        _options = getattr(instance, '_options')
        assert _options[0].__eq__(self.expected_option0)
        assert _options[1].__eq__(self.expected_option1)

        assert not hasattr(instance, '_confirm')

    def test_should_overflow_builder_provide_a_valid_instance_with_any_values(self):

        # GIVEN
        instance = self.overflow_instance_all

        # THEN
        assert isinstance(getattr(instance, '_confirm'), Confirmation)

        _confirmation = getattr(instance, '_confirm')
        assert getattr(getattr(_confirmation, '_title'), '_text') == self.expected_confirmation_title
        assert getattr(getattr(_confirmation, '_text'), '_text') == self.expected_confirmation_text
        assert getattr(getattr(_confirmation, '_confirm'), '_text') == self.expected_confirmation_confirm
        assert getattr(getattr(_confirmation, '_deny'), '_text') == self.expected_confirmation_deny

        assert isinstance(getattr(instance, '_options'), list)
        _options = getattr(instance, '_options')
        assert _options[0].__eq__(self.expected_option0)
        assert _options[1].__eq__(self.expected_option1)

    @raises(AttributeError)
    def test_should_overflow_serialize_raise_attributeerror_if_serialize_without_action_id(self):

        # WHEN
        Overflow.Builder().Option().text('any').value('any').up().build().serialize()

    @raises(AttributeError)
    def test_should_overflow_serialize_raise_attributeerror_if_serialize_without_options(self):

        # WHEN
        Overflow.Builder().action_id('any').up().build().serialize()

    def test_should_overflow_serialize_provide_correct_dict_and_json_data(self):

        # GIVEN
        instance = self.overflow_instance_all

        # WHEN
        serialized_dict = instance.serialize()
        serialized_json = instance.serialize(as_json=True)

        # THEN
        assert serialized_dict == self.expected_serialized_dict
        assert serialized_json == self.expected_serialized_json

    def test_should_overflow_deserialize_provide_correct_instances_from_dict_and_json(self):

        # GIVEN
        serialized_dict = self.expected_serialized_dict
        serialized_json = self.expected_serialized_json

        # WHEN
        instance_from_dict = Overflow.deserialize(serialized_dict)
        instance_from_json = Overflow.deserialize(serialized_json, from_json=True)

        # THEN
        assert isinstance(instance_from_dict, Overflow)
        assert isinstance(instance_from_json, Overflow)
        for instance in (instance_from_dict, instance_from_json):
            assert getattr(instance, '_action_id') == self.expected_action_id

            assert isinstance(getattr(instance, '_confirm'), Confirmation)
            assert isinstance(getattr(instance, '_options'), list)

            _confirmation = getattr(instance, '_confirm')
            assert getattr(getattr(_confirmation, '_title'), '_text') == self.expected_confirmation_title
            assert getattr(getattr(_confirmation, '_text'), '_text') == self.expected_confirmation_text
            assert getattr(getattr(_confirmation, '_confirm'), '_text') == self.expected_confirmation_confirm
            assert getattr(getattr(_confirmation, '_deny'), '_text') == self.expected_confirmation_deny

            _options = getattr(instance, '_options')
            assert _options[0].__eq__(self.expected_option0)
            assert _options[1].__eq__(self.expected_option1)

