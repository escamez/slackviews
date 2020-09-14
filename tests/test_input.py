"""
Class with nosetests for Input AbstractBlock in slack_view library
"""
from nose.tools import raises

from slackviews.view import Input, SelectMenu, PlainText, MultiSelectMenu, PlainTextInput

__author__ = 'Agustin Escamez'
__email__ = 'aech22@gmail.com'


class TestInput:

    def setup(self):

        self.expected_label = 'any label'
        self.expected_block_id = 'any block id'
        self.expected_hint = 'any hint'
        self.expected_optional = False

        self.input_instance_required = Input.Builder().label(self.expected_label).element().SelectMenu() \
            .action_id('any action id').placeholder('any placeholder').Option__().text('o text 1').value('o value 1') \
            .up().Option__().text('o text 2').value('o value 2').up().up().build()

        self.expected_selectmenu = SelectMenu.Builder() \
            .action_id('any action id').placeholder('any placeholder').Option__().text('o text 1').value('o value 1') \
            .up().Option__().text('o text 2').value('o value 2').up().build()

        self.input_instance_all = Input.Builder().label(self.expected_label).block_id_(self.expected_block_id) \
            .optional_(self.expected_optional).hint_(self.expected_hint).element().SelectMenu() \
            .action_id('any action id').placeholder('any placeholder').Option__().text('o text 1').value('o value 1') \
            .up().Option__().text('o text 2').value('o value 2').up().up().build()

        self.expected_serialized_dict = {'type': 'input', 'optional': False,
                                         'hint': {'type': 'plain_text', 'text': 'any hint', 'emoji': False},
                                         'block_id': 'any block id',
                                         'element': {'type': 'static_select',
                                                     'options': [{'value': 'o value 1',
                                                                  'text': {'type': 'plain_text',
                                                                           'text': 'o text 1', 'emoji': False}},
                                                                 {'value': 'o value 2',
                                                                  'text': {'type': 'plain_text',
                                                                           'text': 'o text 2', 'emoji': False}}],
                                                     'action_id': 'any action id',
                                                     'placeholder': {'type': 'plain_text',
                                                                     'text': 'any placeholder', 'emoji': False}},
                                         'label': {'type': 'plain_text', 'text': 'any label', 'emoji': False}}


        self.expected_serialized_json = '{"type": "input", "optional": false, "hint": {"type": "plain_text", ' \
                                        '"text": "any hint", "emoji": false}, "block_id": "any block id", ' \
                                        '"element": {"type": "static_select", "options": [{"value": "o value 1",' \
                                        ' "text": {"type": "plain_text", "text": "o text 1", "emoji": false}}, ' \
                                        '{"value": "o value 2", "text": {"type": "plain_text", "text": "o text 2", ' \
                                        '"emoji": false}}], "action_id": "any action id", "placeholder": ' \
                                        '{"type": "plain_text", "text": "any placeholder", "emoji": false}}, ' \
                                        '"label": {"type": "plain_text", "text": "any label", "emoji": false}}'

    def teardown(self):
        Input.__all_slots__ = None

    def test_should_input_builder_provide_a_valid_instance_with_required_values(self):

        # GIVEN
        expected_slots = ['_label', '_element']
        expected_all_slots = ['_block_id', '_hint', '_optional']
        expected_all_slots.extend(expected_slots)

        # WHEN
        instance = self.input_instance_required

        # THEN
        assert isinstance(instance, Input)
        assert hasattr(instance, '__all_slots__')
        assert hasattr(instance, '__slots__')
        for att in expected_slots:
            assert att in getattr(instance, '__slots__')
        for att in expected_all_slots:
            assert att in getattr(instance, '__all_slots__')

        assert isinstance(getattr(instance, '_label'), PlainText)
        assert getattr(getattr(instance, '_label'), '_text') == self.expected_label
        assert isinstance(getattr(instance, '_element'), SelectMenu)
        assert getattr(instance, '_element').__eq__(self.expected_selectmenu)
        assert not hasattr(instance, '_block_id')
        assert not hasattr(instance, '_hint')
        assert not hasattr(instance, '_optional')


    def test_should_input_builder_provide_a_valid_instance_with_all_values(self):

        # GIVEN
        instance = self.input_instance_all

        # THEN
        assert isinstance(getattr(instance, '_label'), PlainText)
        assert getattr(getattr(instance, '_label'), '_text') == self.expected_label
        assert isinstance(getattr(instance, '_element'), SelectMenu)
        assert getattr(instance, '_element').__eq__(self.expected_selectmenu)
        assert isinstance(getattr(instance, '_hint'), PlainText)
        assert getattr(getattr(instance, '_label'), '_text') == self.expected_label
        assert getattr(getattr(instance, '_hint'), '_text') == self.expected_hint
        assert getattr(instance, '_block_id') == self.expected_block_id
        assert not getattr(instance, '_optional')

    @raises(AttributeError)
    def test_should_input_serialize_raise_assertionerror_if_missing_required_fields(self):

        # WHEN
        Input.Builder().label('any').build().serialize()

    def test_should_input_builder_provide_correct_element_type(self):

        # GIVEN
        expectd_multiselect = MultiSelectMenu.Builder().action_id('any').placeholder('any').Option__() \
            .text('any').value('any').up().build()
        expectd_select = SelectMenu.Builder().action_id('any').placeholder('any').Option__() \
            .text('any').value('any').up().build()
        expectd_plaintextinput = PlainTextInput.Builder().action_id('any').build()

        instance_with_multiselectmenu = Input.Builder().element().MultiSelectMenu().action_id('any').placeholder('any') \
            .Option__().text('any').value('any').up().up().build()

        instance_with_selectmenu = Input.Builder().element().SelectMenu().action_id('any').placeholder('any') \
            .Option__().text('any').value('any').up().up().build()

        instance_with_plaintextinput = Input.Builder().element().PlainTextInput().action_id('any').up().build()

        # THEN
        assert isinstance(getattr(instance_with_multiselectmenu, '_element'), MultiSelectMenu)
        assert getattr(instance_with_multiselectmenu, '_element').__eq__(expectd_multiselect)

        assert isinstance(getattr(instance_with_selectmenu, '_element'), SelectMenu)
        assert getattr(instance_with_selectmenu, '_element').__eq__(expectd_select)

        assert isinstance(getattr(instance_with_plaintextinput, '_element'), PlainTextInput)
        assert getattr(instance_with_plaintextinput, '_element').__eq__(expectd_plaintextinput)

    @raises(AssertionError)
    def test_should_input_builder_raise_assertionerror_if_element_is_not_allowed_element(self):

        # GIVEN
        _input = Input.Builder().label('any').build()
        setattr(_input, '_element', object())

        # WHEN
        _input.serialize()

    @raises(AssertionError)
    def test_should_input_serialize_raise_assertionerror_if_optional_not_boolean(self):

        # GIVEN
        _input = Input.Builder().label('any').element().PlainTextInput().action_id('any').up().build()
        setattr(_input, '_optional', object())

        # WHEN
        _input.serialize()

    @raises(AssertionError)
    def test_should_input_element_raise_assertionerror_if_label_is_not_plaintext(self):

        # GIVEN
        _input = Input.Builder().element().PlainTextInput().action_id('any').up().build()
        setattr(_input, '_label', 'any text that is not plaintext')

        # WHEN
        _input.serialize()

    @raises(AssertionError)
    def test_should_input_element_raise_assertionerror_if_hint_is_not_plaintext(self):

        # GIVEN
        _input = Input.Builder().label('any').element().PlainTextInput().action_id('any').up().build()
        setattr(_input, '_hint', 'any text that is not plaintext')

        # WHEN
        _input.serialize()

    def test_should_input_serialize_provide_correct_dict_and_json_data(self):

        # GIVEN
        instance = self.input_instance_all

        # WHEN
        serialized_dict = instance.serialize()
        serialized_json = instance.serialize(as_json=True)

        # THEN
        assert serialized_dict == self.expected_serialized_dict
        assert serialized_json == self.expected_serialized_json

    def test_should_input_deserialize_provide_correct_instances_from_dict_and_json(self):

        # GIVEN
        serialized_dict = self.expected_serialized_dict
        serialized_json = self.expected_serialized_json

        # WHEN
        instance_from_dict = Input.deserialize(serialized_dict)
        instance_from_json = Input.deserialize(serialized_json, from_json=True)

        # THEN
        assert isinstance(instance_from_dict, Input)
        assert isinstance(instance_from_json, Input)
        for instance in (instance_from_dict, instance_from_json):
            assert isinstance(getattr(instance, '_label'), PlainText)
            assert getattr(getattr(instance, '_label'), '_text') == self.expected_label
            assert isinstance(getattr(instance, '_element'), SelectMenu)
            assert getattr(instance, '_element').__eq__(self.expected_selectmenu)
            assert isinstance(getattr(instance, '_hint'), PlainText)
            assert getattr(getattr(instance, '_label'), '_text') == self.expected_label
            assert getattr(getattr(instance, '_hint'), '_text') == self.expected_hint
            assert getattr(instance, '_block_id') == self.expected_block_id
            assert not getattr(instance, '_optional')
