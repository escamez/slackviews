"""
Class with nosetests for Context AbstractBlock in slack_view library
"""
from nose.tools import raises

from slackviews.view import Context, Image, MarkDown

__author__ = 'Agustin Escamez'
__email__ = 'aech22@gmail.com'


class TestContext:

    def setup(self):
        self.expected_block_id = 'any block id'
        self.expected_image_alt_text = 'any alt text'
        self.expected_image_url = 'any url'

        self.expected_image_serialized = Image.Builder().alt_text(self.expected_image_alt_text) \
            .image_url(self.expected_image_url).build().serialize()

        self.context_instance_required = Context.Builder().element().Image().alt_text(self.expected_image_alt_text) \
            .image_url(self.expected_image_url).up().build()

        self.context_instance_all = Context.Builder().block_id_(self.expected_block_id).element() \
            .Image().alt_text(self.expected_image_alt_text).image_url(self.expected_image_url).up().build()

        self.expected_serialized_dict = {'type': 'context', 'block_id': self.expected_block_id,
                                         'elements': [{'type': 'image', 'alt_text': self.expected_image_alt_text,
                                                       'image_url': self.expected_image_url}]}

        self.expected_serialized_json = f'{{"type": "context", "block_id": "{self.expected_block_id}", ' \
                                        f'"elements": [{{"type": "image", ' \
                                        f'"alt_text": "{self.expected_image_alt_text}", ' \
                                        f'"image_url": "{self.expected_image_url}"}}]}}'

    def teardown(self):
        Context.__all_slots__ = None

    def test_should_context_builder_provide_a_valid_instance_with_required_values(self):

        # GIVEN
        expected_slots = ['_elements']
        expected_all_slots = ['_block_id']
        expected_all_slots.extend(expected_slots)

        # WHEN
        instance = self.context_instance_required

        # THEN
        assert isinstance(instance, Context)
        assert hasattr(instance, '__all_slots__')
        assert hasattr(instance, '__slots__')
        for att in expected_slots:
            assert att in getattr(instance, '__slots__')
        for att in expected_all_slots:
            assert att in getattr(instance, '__all_slots__')

        assert isinstance(getattr(instance, '_elements'), list)
        assert not hasattr(instance, '_block_id')

        _image = getattr(instance, '_elements')[0]
        assert isinstance(_image, Image)
        assert getattr(_image, '_alt_text') == self.expected_image_alt_text
        assert getattr(_image, '_image_url') == self.expected_image_url
        assert _image.serialize() == self.expected_image_serialized

    def test_should_context_builder_provide_a_valid_instance_with_all_values(self):

        # GIVEN
        instance = self.context_instance_all

        # THEN
        assert isinstance(getattr(instance, '_elements'), list)
        _image = getattr(instance, '_elements')[0]
        assert isinstance(_image, Image)
        assert getattr(_image, '_alt_text') == self.expected_image_alt_text
        assert getattr(_image, '_image_url') == self.expected_image_url
        assert _image.serialize() == self.expected_image_serialized
        assert getattr(instance, '_block_id') == self.expected_block_id

    @raises(AttributeError)
    def test_should_context_serialize_raise_assertionerror_if_missing_required_fields(self):

        # WHEN
        Context.Builder().block_id_('any').build().serialize()

    def test_should_context_builder_provide_correct_element_type(self):

        # GIVEN
        isinstance_with_image = Context.Builder().element().Image().alt_text('any').image_url('any').up().build()

        isinstance_with_text = Context.Builder().element().Text().text('any').up().build()

        # THEN
        assert isinstance(getattr(isinstance_with_image, '_elements'), list)
        assert isinstance(getattr(isinstance_with_image, '_elements')[0], Image)

        assert isinstance(getattr(isinstance_with_text, '_elements'), list)
        assert isinstance(getattr(isinstance_with_text, '_elements')[0], MarkDown)

    @raises(AssertionError)
    def test_should_context_builder_raise_assertionerror_if_elements_is_not_a_list(self):

        # GIVEN
        _context = Context.Builder().build()
        setattr(_context, '_elements', object())

        # WHEN
        _context.serialize()

    @raises(AssertionError)
    def test_should_context_builder_raise_assertionerror_if_element_is_not_an_allowed_element(self):

        # GIVEN
        _context = Context.Builder().build()
        setattr(_context, '_elements', [object()])

        # WHEN
        _context.serialize()

    @raises(AssertionError)
    def test_should_context_serialize_raise_assertionerror_if_more_than_6_elements_are_provided(self):

        # GIVEN
        _context = Context.Builder().build()
        setattr(_context, '_elements', [object() for i in range(6)])

        # WHEN
        _context.serialize()

    @raises(AttributeError)
    def test_should_actions_element_raise_attributeerror_if_trying_to_add_another_element_when_max_is_reached(self):

        # GIVEN
        _builder = Context.Builder()
        for i in range(5):
            _builder.element().Image().image_url(f'url_{i}').alt_text(f'alt_text_{i}')

        # WHEN
        _builder.element().Image().image_url('url_6').alt_text('alt_text_6')

    def test_should_context_serialize_provide_correct_dict_and_json_data(self):

        # GIVEN
        instance = self.context_instance_all

        # WHEN
        serialized_dict = instance.serialize()
        serialized_json = instance.serialize(as_json=True)

        # THEN
        assert serialized_dict == self.expected_serialized_dict
        assert serialized_json == self.expected_serialized_json

    def test_should_context_deserialize_provide_correct_instances_from_dict_and_json(self):

        # GIVEN
        serialized_dict = self.expected_serialized_dict
        serialized_json = self.expected_serialized_json

        # WHEN
        instance_from_dict = Context.deserialize(serialized_dict)
        instance_from_json = Context.deserialize(serialized_json, from_json=True)

        # THEN
        assert isinstance(instance_from_dict, Context)
        assert isinstance(instance_from_json, Context)
        for instance in (instance_from_dict, instance_from_json):
            assert isinstance(getattr(instance, '_elements'), list)
            _image = getattr(instance, '_elements')[0]
            assert isinstance(_image, Image)
            assert getattr(_image, '_alt_text') == self.expected_image_alt_text
            assert getattr(_image, '_image_url') == self.expected_image_url
            assert _image.serialize() == self.expected_image_serialized
            assert getattr(instance, '_block_id') == self.expected_block_id
