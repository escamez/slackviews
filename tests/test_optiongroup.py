"""
Class with nosetests for OptionGroup AbstractBlock in slack_view library
"""

from nose.tools import raises

from slackviews.view import OptionGroup, PlainText, Option

__author__ = 'Agustin Escamez'
__email__ = 'aech22@gmail.com'


class TestOptiongroup:

    def setup(self):
        self.expected_label = 'any label'
        self.expected_option0_text = 'option 1 text'
        self.expected_option0_value = 'option 1 value'
        self.expected_option1_text = 'option 2 text'
        self.expected_option1_value = 'option 2 value'

        self.expected_option0 = Option.Builder().text(self.expected_option0_text).value(self.expected_option0_value) \
            .build()
        self.expected_option1 = Option.Builder().text(self.expected_option1_text).value(self.expected_option1_value) \
            .build()

        self.expected_serialized_dict = {'options': [{'value': self.expected_option0_value,
                                                      'text': {'type': 'plain_text', 'text': self.expected_option0_text,
                                                               'emoji': False}},
                                                     {'value': self.expected_option1_value,
                                                      'text': {'type': 'plain_text', 'text': self.expected_option1_text,
                                                               'emoji': False}}],
                                         'label': {'type': 'plain_text', 'text': self.expected_label, 'emoji': False}}

        self.expected_serialized_json = f'{{"options": [{{"value": "{self.expected_option0_value}", ' \
                                        f'"text": {{"type": "plain_text", "text": "{self.expected_option0_text}", ' \
                                        f'"emoji": false}}}}, {{"value": "{self.expected_option1_value}", ' \
                                        f'"text": {{"type": "plain_text", "text": "{self.expected_option1_text}", ' \
                                        f'"emoji": false}}}}], "label": {{"type": "plain_text", ' \
                                        f'"text": "{self.expected_label}", "emoji": false}}}}'

        self.expected_option0 = Option.Builder().text(self.expected_option0_text).value(
            self.expected_option0_value).build()
        self.expected_option1 = Option.Builder().text(self.expected_option1_text).value(
            self.expected_option1_value).build()

        self.expected_options = [self.expected_option0, self.expected_option1]

        _builder = OptionGroup.Builder().label(self.expected_label)
        for opt_ in self.expected_options:
            _builder.Option().text(getattr(getattr(opt_, '_text'), '_text')).value(getattr(opt_, '_value'))
        self.optiongroup_instance = _builder.build()

    def teardown(self):
        OptionGroup.__all_slots__ = None

    def test_should_optiongroup_builder_provide_a_valid_instance_with_required_values(self):

        # GIVEN
        expected_slots = ('_label', '_options')
        expected_all_slots = expected_slots

        # WHEN
        instance = self.optiongroup_instance

        # THEN
        assert isinstance(instance, OptionGroup)
        assert hasattr(instance, '__all_slots__')
        assert hasattr(instance, '__slots__')
        for att in expected_slots:
            assert att in getattr(instance, '__slots__')
        for att in expected_all_slots:
            assert att in getattr(instance, '__all_slots__')

        assert isinstance(getattr(instance, '_label'), PlainText)
        assert getattr(getattr(instance, '_label'), '_text') == self.expected_label

        _options = getattr(instance, '_options')
        assert isinstance(_options, list)
        for _opt in getattr(instance, '_options'):
            assert isinstance(_opt, Option)
            assert isinstance(getattr(_opt, '_text'), PlainText)

        assert getattr(getattr(_options[0], '_text'), '_text') == self.expected_option0_text
        assert getattr(_options[0], '_value') == self.expected_option0_value
        assert getattr(getattr(_options[1], '_text'), '_text') == self.expected_option1_text
        assert getattr(_options[1], '_value') == self.expected_option1_value

    @raises(AttributeError)
    def test_should_optiongroup_serialize_raise_attributeerror_if_trying_to_serialize_without_all_required_slots(self):

        # WHEN
        OptionGroup.Builder().build().serialize()

    def test_should_optiongroup_serialize_provide_correct_dict_and_json_data(self):

        # GIVEN
        instance = self.optiongroup_instance

        # WHEN
        serialized_dict = instance.serialize()
        serialized_json = instance.serialize(as_json=True)

        # THEN
        assert serialized_dict == self.expected_serialized_dict
        assert serialized_json == self.expected_serialized_json

    def test_should_optiongroup_deserialize_provide_correct_instances_from_dict_and_json(self):

        # GIVEN
        serialized_dict = self.expected_serialized_dict
        serialized_json = self.expected_serialized_json

        # WHEN
        instance_from_dict = OptionGroup.deserialize(serialized_dict)
        instance_from_json = OptionGroup.deserialize(serialized_json, from_json=True)

        # THEN
        assert isinstance(instance_from_dict, OptionGroup)
        assert isinstance(instance_from_json, OptionGroup)
        for instance in (instance_from_dict, instance_from_json):
            assert isinstance(getattr(instance, '_label'), PlainText)
            assert getattr(getattr(instance, '_label'), '_text') == self.expected_label

            _options = getattr(instance, '_options')
            assert isinstance(_options, list)
            for _opt in getattr(instance, '_options'):
                assert isinstance(_opt, Option)
                assert isinstance(getattr(_opt, '_text'), PlainText)

            assert getattr(getattr(_options[0], '_text'), '_text') == self.expected_option0_text
            assert getattr(_options[0], '_value') == self.expected_option0_value
            assert getattr(getattr(_options[1], '_text'), '_text') == self.expected_option1_text
            assert getattr(_options[1], '_value') == self.expected_option1_value
