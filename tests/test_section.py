"""
Class with nosetests for Section AbstractBlock in slack_view library
"""
from nose.tools import raises

from slackviews.view import PlainText, Section, MarkDown, Image, Button, \
    SelectMenu, MultiSelectMenu, PlainTextInput, Overflow

__author__ = 'Agustin Escamez'
__email__ = 'aech22@gmail.com'


class TestSection:

    def setup(self):

        __slots__ = ('_text', '_block_id', '_fields', '_accessory')

        self.expected_text = 'any text'
        self.expected_block_id = 'any block id'

        self.section_instance_required = Section.Builder().text__(self.expected_text).build()

        self.expected_accessory_class = Image
        self.section_instance_all = Section.Builder().block_id_(self.expected_block_id).text__(self.expected_text) \
            .accessory_().Image().image_url('any url').alt_text('any alt text').up().build()

        self.expected_serialized_dict = {'type': 'section',
                                         'accessory': {'type': 'image', 'alt_text': 'any alt text',
                                                       'image_url': 'any url'}, 'block_id': self.expected_block_id,
                                         'text': {'type': 'mrkdwn', 'text': self.expected_text, 'verbatim': False}}

        self.expected_serialized_json = f'{{"type": "section", "accessory": {{"type": "image", "alt_text": ' \
                                        f'"any alt text", "image_url": "any url"}}, ' \
                                        f'"block_id": "{self.expected_block_id}", "text": {{"type": "mrkdwn", ' \
                                        f'"text": "any text", "verbatim": false}}}}'

    def teardown(self):
        Section.__all_slots__ = None

    def test_should_section_builder_provide_a_valid_instance_with_required_values_using_text(self):

        # GIVEN
        expected_slots = ['_text']
        expected_all_slots = ['_block_id', '_fields', '_accessory']
        expected_all_slots.extend(expected_slots)

        # WHEN
        instance = self.section_instance_required

        # THEN
        assert isinstance(instance, Section)
        assert hasattr(instance, '__all_slots__')
        assert hasattr(instance, '__slots__')
        for att in expected_slots:
            assert att in getattr(instance, '__slots__')
        for att in expected_all_slots:
            assert att in getattr(instance, '__all_slots__')

        assert isinstance(getattr(instance, '_text'), MarkDown)
        assert getattr(getattr(instance, '_text'), '_text') == self.expected_text
        assert not hasattr(instance, '_block_id')
        assert not hasattr(instance, '_fields')
        assert not hasattr(instance, '_accessory')

    def test_should_section_builder_provide_a_valid_instance_with_required_values_using_fields(self):

        # GIVEN
        expected_field_text = 'any field text'
        instance = Section.Builder().field__(expected_field_text).build()

        # THEN
        assert isinstance(instance, Section)

        assert isinstance(getattr(instance, '_fields'), list)
        _fields = getattr(instance, '_fields')
        assert isinstance(_fields[0], MarkDown)
        assert getattr(_fields[0], '_text') == expected_field_text

        assert not hasattr(instance, '_text')
        assert not hasattr(instance, '_block_id')
        assert not hasattr(instance, '_accessory')

    def test_should_section_builder_provide_a_valid_instance_with_all_values(self):

        # GIVEN
        instance = self.section_instance_all

        # THEN
        assert isinstance(getattr(instance, '_text'), MarkDown)
        assert getattr(getattr(instance, '_text'), '_text') == self.expected_text
        assert getattr(instance, '_block_id') == self.expected_block_id
        assert isinstance(getattr(instance, '_accessory'), self.expected_accessory_class)

    @raises(AssertionError)
    def test_should_section_serialize_raise_assertionerror_if_mutually_exclusive_options_are_provided(self):

        # WHEN
        Section.Builder().text__('any').field__('any').build().serialize()

    def test_should_section_builder_provide_correct_accessory_type(self):

        # GIVEN
        instance_with_button = Section.Builder().text__('any').accessory_() \
            .Button().text('any').action_id('any').up().build()

        instance_with_selectmenu = Section.Builder().text__('any').accessory_() \
            .SelectMenu().action_id('any').placeholder('any').Option__().text('any').value('any').up().up().build()

        instance_with_multiselectmenu = Section.Builder().text__('any').accessory_() \
            .MultiSelectMenu().action_id('any').placeholder('any').Option__().text('any') \
            .value('any').up().up().build()

        instance_with_plaintextinput = Section.Builder().text__('any').accessory_() \
            .PlainTextInput().action_id('any').up().build()

        instance_with_image = Section.Builder().text__('any').accessory_() \
            .Image().image_url('any').alt_text('any').up().build()

        instance_with_overflow = Section.Builder().text__('any').accessory_() \
            .Overflow().action_id('any').Option().text('any').value('any').up().up().build()

        # THEN
        assert isinstance(getattr(instance_with_button, '_accessory'), Button)
        assert isinstance(getattr(instance_with_selectmenu, '_accessory'), SelectMenu)
        assert isinstance(getattr(instance_with_multiselectmenu, '_accessory'), MultiSelectMenu)
        assert isinstance(getattr(instance_with_plaintextinput, '_accessory'), PlainTextInput)
        assert isinstance(getattr(instance_with_image, '_accessory'), Image)
        assert isinstance(getattr(instance_with_overflow, '_accessory'), Overflow)

    @raises(AttributeError)
    def test_should_section_builder_raise_attributeerror_if_more_than_10_fields_are_provided(self):

        # GIVEN
        _builder = Section.Builder()
        for i in range(11):
            _builder.field__(f'any field text {i}')

    @raises(AssertionError)
    def test_should_section_serialize_raise_assertionerror_if_more_than_10_fields_are_provided(self):

        # GIVEN
        instance = Section.Builder().build()
        _fields = []
        for i in range(11):
            _fields.append(MarkDown.Builder().text(f'any field text {i}').build())
        setattr(instance, '_fields', _fields)

        # WHEN
        instance.serialize()

    @raises(AssertionError)
    def test_should_section_serialize_raise_assertionerror_if_field_is_not_markdown(self):

        # GIVEN
        instance = Section.Builder().build()
        _fields = [PlainText.Builder().text(f'any field text').build()]
        setattr(instance, '_fields', _fields)

        # WHEN
        instance.serialize()

    @raises(AssertionError)
    def test_should_section_serialize_raise_assertionerror_if_serialize_without_text_or_fields(self):

        # WHEN
        Section.Builder().build().serialize()

    def test_should_section_serialize_provide_correct_dict_and_json_data(self):

        # GIVEN
        instance = self.section_instance_all

        # WHEN
        serialized_dict = instance.serialize()
        serialized_json = instance.serialize(as_json=True)

        # THEN
        assert serialized_dict == self.expected_serialized_dict
        assert serialized_json == self.expected_serialized_json

    def test_should_section_deserialize_provide_correct_instances_from_dict_and_json(self):

        # GIVEN
        serialized_dict = self.expected_serialized_dict
        serialized_json = self.expected_serialized_json

        # WHEN
        instance_from_dict = Section.deserialize(serialized_dict)
        instance_from_json = Section.deserialize(serialized_json, from_json=True)

        # THEN
        assert isinstance(instance_from_dict, Section)
        assert isinstance(instance_from_json, Section)
        for instance in (instance_from_dict, instance_from_json):
            assert isinstance(getattr(instance, '_text'), MarkDown)
            assert getattr(getattr(instance, '_text'), '_text') == self.expected_text
            assert getattr(instance, '_block_id') == self.expected_block_id
            assert isinstance(getattr(instance, '_accessory'), self.expected_accessory_class)
