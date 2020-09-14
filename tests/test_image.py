"""
Class with nosetests for Image AbstractBlock in slack_view library
"""

from nose.tools import raises

from slackviews.view import Image

__author__ = 'Agustin Escamez'
__email__ = 'aech22@gmail.com'


class TestImage:

    def teardown(self):
        Image.__all_slots__ = None

    def test_should_image_builder_provide_a_valid_instance_with_required_values(self):

        # GIVEN
        expected_slots = ['_image_url', '_alt_text']
        expected_all_slots = expected_slots
        expected_alt_text = 'any text'
        expected_image_url = 'image url'

        # WHEN
        instance = Image.Builder().alt_text(expected_alt_text).image_url(expected_image_url).build()

        # THEN
        assert hasattr(instance, '__all_slots__')
        assert hasattr(instance, '__slots__')
        for att in expected_slots:
            assert att in getattr(instance, '__slots__')
        for att in expected_all_slots:
            assert att in getattr(instance, '__all_slots__')

        assert getattr(instance, '_image_url') == expected_image_url
        assert getattr(instance, '_alt_text') == expected_alt_text


    @raises(AttributeError)
    def test_should_image_serialize_raise_attributeerror_if_trying_to_serialize_without_all_required_slots(self):

        # WHEN
        Image.Builder().build().serialize()

    def test_should_image_serialize_provide_correct_dict_and_json_data(self):

        # GIVEN
        expected_serialized_dict = {'type': 'image', 'alt_text': 'any text', 'image_url': 'any url'}
        expected_serialized_json = '{"type": "image", "alt_text": "any text", "image_url": "any url"}'

        instance = Image.Builder().alt_text('any text').image_url('any url').build()

        # WHEN
        serialized_dict = instance.serialize()
        serialized_json = instance.serialize(as_json=True)

        # THEN
        assert serialized_dict == expected_serialized_dict
        assert serialized_json == expected_serialized_json

    def test_should_image_deserialize_provide_correct_instances_from_dict_and_json(self):

        # GIVEN
        serialized_dict = {'type': 'image', 'alt_text': 'any text', 'image_url': 'any url'}
        serialized_json = '{"type": "image", "alt_text": "any text", "image_url": "any url"}'

        # WHEN
        instance_from_dict = Image.deserialize(serialized_dict)
        instance_from_json = Image.deserialize(serialized_json, from_json=True)

        # THEN
        assert isinstance(instance_from_dict, Image) and isinstance(instance_from_json, Image)
        assert getattr(instance_from_dict, '_alt_text') == 'any text'
        assert getattr(instance_from_dict, '_image_url') == 'any url'
        assert getattr(instance_from_json, '_alt_text') == 'any text'
        assert getattr(instance_from_json, '_image_url') == 'any url'
