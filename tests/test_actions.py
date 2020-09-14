"""
Class with nosetests for Actions AbstractBlock in slack_view library
"""
from nose.tools import raises

from slackviews.view import Actions, Button, \
    SelectMenu, Overflow

__author__ = 'Agustin Escamez'
__email__ = 'aech22@gmail.com'


class TestActions:

    def setup(self):

        self.expected_block_id = 'any block id'
        self.expected_button_text = 'any button text'
        self.expected_button_action_id = 'any action id'

        self.expected_button_serialized = Button.Builder().text(self.expected_button_text) \
            .action_id(self.expected_button_action_id).build().serialize()

        self.actions_instance_required = Actions.Builder().element().Button().text(self.expected_button_text) \
            .action_id(self.expected_button_action_id).up().build()

        self.actions_instance_all = Actions.Builder().block_id_(self.expected_block_id).element().Button() \
            .text(self.expected_button_text).action_id(self.expected_button_action_id).up().build()

        self.expected_serialized_dict = {'type': 'actions', 'block_id': 'any block id',
                                         'elements': [{'type': 'button', 'action_id': 'any action id',
                                                       'text': {'type': 'plain_text', 'text': 'any button text',
                                                                'emoji': False}}]}

        self.expected_serialized_json = f'{{"type": "actions", "block_id": "{self.expected_block_id}", ' \
                                        f'"elements": [{{"type": "button", ' \
                                        f'"action_id": "{self.expected_button_action_id}", ' \
                                        f'"text": {{"type": "plain_text", "text": "{self.expected_button_text}", ' \
                                        f'"emoji": false}}}}]}}'


    def teardown(self):
        Actions.__all_slots__ = None

    def test_should_actions_builder_provide_a_valid_instance_with_required_values(self):

        # GIVEN
        expected_slots = ['_elements']
        expected_all_slots = ['_block_id']
        expected_all_slots.extend(expected_slots)

        # WHEN
        instance = self.actions_instance_required

        # THEN
        assert isinstance(instance, Actions)
        assert hasattr(instance, '__all_slots__')
        assert hasattr(instance, '__slots__')
        for att in expected_slots:
            assert att in getattr(instance, '__slots__')
        for att in expected_all_slots:
            assert att in getattr(instance, '__all_slots__')

        assert isinstance(getattr(instance, '_elements'), list)
        assert not hasattr(instance, '_block_id')

        _button = getattr(instance, '_elements')[0]
        assert isinstance(_button, Button)
        assert getattr(getattr(_button, '_text'), '_text') == self.expected_button_text
        assert getattr(_button, '_action_id') == self.expected_button_action_id
        assert _button.serialize() == self.expected_button_serialized

    def test_should_actions_builder_provide_a_valid_instance_with_all_values(self):

        # GIVEN
        instance = self.actions_instance_all

        # THEN
        assert isinstance(getattr(instance, '_elements'), list)
        _button = getattr(instance, '_elements')[0]
        assert isinstance(_button, Button)
        assert getattr(getattr(_button, '_text'), '_text') == self.expected_button_text
        assert getattr(_button, '_action_id') == self.expected_button_action_id
        assert _button.serialize() == self.expected_button_serialized
        assert getattr(instance, '_block_id') == self.expected_block_id

    @raises(AttributeError)
    def test_should_actions_serialize_raise_assertionerror_if_missing_required_fields(self):

        # WHEN
        Actions.Builder().block_id_('any').build().serialize()

    def test_should_actions_builder_provide_correct_element_type(self):

        # GIVEN
        instance_with_button = Actions.Builder().element().Button().text('any').action_id('any').up().build()

        instance_with_selectmenu = Actions.Builder().element().SelectMenu().action_id('any').placeholder('any') \
            .Option__().text('any').value('any').up().up().build()

        instance_with_overflow = Actions.Builder().element().Overflow().action_id('any') \
            .Option().text('any').value('any').up().up().build()

        # THEN
        assert isinstance(getattr(instance_with_button, '_elements'), list)
        assert isinstance(getattr(instance_with_button, '_elements')[0], Button)

        assert isinstance(getattr(instance_with_selectmenu, '_elements'), list)
        assert isinstance(getattr(instance_with_selectmenu, '_elements')[0], SelectMenu)

        assert isinstance(getattr(instance_with_overflow, '_elements'), list)
        assert isinstance(getattr(instance_with_overflow, '_elements')[0], Overflow)

    @raises(AssertionError)
    def test_should_actions_builder_raise_assertionerror_if_elements_is_not_a_list(self):

        # GIVEN
        _actions = Actions.Builder().build()
        setattr(_actions, '_elements', object())

        # WHEN
        _actions.serialize()

    @raises(AssertionError)
    def test_should_actions_serialize_raise_assertionerror_if_more_than_6_elements_are_provided(self):

        # GIVEN
        _actions = Actions.Builder().build()
        setattr(_actions, '_elements', [object() for i in range(6)])

        # WHEN
        _actions.serialize()

    @raises(AttributeError)
    def test_should_actions_element_raise_attributeerror_if_trying_to_add_another_element_when_max_is_reached(self):

        # GIVEN
        _builder = Actions.Builder()
        for i in range(5):
            _builder.element().Button().text(f'any_{i}').action_id(f'action_{i}')

        # WHEN
        _builder.element().Button().text('any_6').action_id('action_6')

    def test_should_actions_serialize_provide_correct_dict_and_json_data(self):

        # GIVEN
        instance = self.actions_instance_all

        # WHEN
        serialized_dict = instance.serialize()
        serialized_json = instance.serialize(as_json=True)

        # THEN
        assert serialized_dict == self.expected_serialized_dict
        assert serialized_json == self.expected_serialized_json

    def test_should_actions_deserialize_provide_correct_instances_from_dict_and_json(self):

        # GIVEN
        serialized_dict = self.expected_serialized_dict
        serialized_json = self.expected_serialized_json

        # WHEN
        instance_from_dict = Actions.deserialize(serialized_dict)
        instance_from_json = Actions.deserialize(serialized_json, from_json=True)

        # THEN
        assert isinstance(instance_from_dict, Actions)
        assert isinstance(instance_from_json, Actions)
        for instance in (instance_from_dict, instance_from_json):
            assert isinstance(getattr(instance, '_elements'), list)
            _button = getattr(instance, '_elements')[0]
            assert isinstance(_button, Button)
            assert getattr(getattr(_button, '_text'), '_text') == self.expected_button_text
            assert getattr(_button, '_action_id') == self.expected_button_action_id
            assert _button.serialize() == self.expected_button_serialized
            assert getattr(instance, '_block_id') == self.expected_block_id
