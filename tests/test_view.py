"""
Class with nosetests for View AbstractBlock in slack_view library
"""
from nose.tools import raises

from slackviews.view import PlainText, View, Section, BlocksArray, Divider, Modal, Home

__author__ = 'Agustin Escamez'
__email__ = 'aech22@gmail.com'


class TestView:

    def setup(self):

        self.expected_callback_id = 'any callback_id'
        self.expected_clear_on_close = True
        self.expected_close = 'any close text'
        self.expected_external_id = 'any external id'
        self.expected_notify_on_close = True
        self.expected_private_metadata = 'any metadata'
        self.expected_submit = 'any submit text'
        self.expected_title = 'any title text'

        self.expected_section = Section.Builder().text__('any text').build()

        self.view_instance_required = View.Builder().title(self.expected_title).Blocks().Section() \
            .text__('any text').up().up().build()

        self.view_instance_all = self.expected_view_required = View.Builder() \
            .callback_id_(self.expected_callback_id) \
            .clear_on_close_(self.expected_clear_on_close) \
            .close_(self.expected_close) \
            .external_id_(self.expected_external_id) \
            .notify_on_close_(self.expected_notify_on_close) \
            .private_metadata_(self.expected_private_metadata) \
            .submit_(self.expected_submit) \
            .title(self.expected_title) \
            .Blocks().Section().text__('any text').up().up().build()

        self.expected_serialized_dict = {'title': {'type': 'plain_text', 'text': 'any title text', 'emoji': False},
                                         'submit': {'type': 'plain_text', 'text': 'any submit text', 'emoji': False},
                                         'private_metadata': 'any metadata', 'notify_on_close': True,
                                         'external_id': 'any external id',
                                         'close': {'type': 'plain_text', 'text': 'any close text', 'emoji': False},
                                         'clear_on_close': True, 'callback_id': 'any callback_id',
                                         'blocks': [{'type': 'section', 'text': {'type': 'mrkdwn',
                                                                                 'text': 'any text',
                                                                                 'verbatim': False}}]}

        self.expected_serialized_json = '{"title": {"type": "plain_text", "text": "any title text", "emoji": false}, ' \
                                        '"submit": {"type": "plain_text", "text": "any submit text", "emoji": false},' \
                                        ' "private_metadata": "any metadata", "notify_on_close": true, ' \
                                        '"external_id": "any external id", "close": {"type": "plain_text", ' \
                                        '"text": "any close text", "emoji": false}, "clear_on_close": true, ' \
                                        '"callback_id": "any callback_id", "blocks": [{"type": "section", "text": ' \
                                        '{"type": "mrkdwn", "text": "any text", "verbatim": false}}]}'

    def teardown(self):
        View.__all_slots__ = None

    def test_should_view_builder_provide_a_valid_instance_with_required_values(self):

        # GIVEN
        expected_slots = ['_title', '_blocks']
        expected_all_slots = ['_callback_id', '_clear_on_close', '_close', '_external_id', '_notify_on_close',
                              '_private_metadata', '_submit']
        expected_all_slots.extend(expected_slots)

        # WHEN
        instance = self.view_instance_required

        # THEN
        assert isinstance(instance, View)
        assert hasattr(instance, '__all_slots__')
        assert hasattr(instance, '__slots__')
        for att in expected_slots:
            assert att in getattr(instance, '__slots__')
        for att in expected_all_slots:
            assert att in getattr(instance, '__all_slots__')

        assert isinstance(getattr(instance, '_title'), PlainText)
        assert getattr(getattr(instance, '_title'), '_text') == self.expected_title
        assert isinstance(getattr(instance, '_blocks'), BlocksArray)

        _section = getattr(getattr(instance, '_blocks'), '_blocks')[0]
        assert isinstance(_section, Section)
        assert _section.__eq__(self.expected_section)
        assert not hasattr(instance, '_callback_id')
        assert not hasattr(instance, '_clear_on_close')
        assert not hasattr(instance, '_close')
        assert not hasattr(instance, '_external_id')
        assert not hasattr(instance, '_notify_on_close')
        assert not hasattr(instance, '_private_metadata')
        assert not hasattr(instance, '_submit')

    def test_should_view_builder_provide_a_valid_instance_with_any_values(self):

        # GIVEN
        instance = self.view_instance_all

        # THEN
        assert isinstance(getattr(instance, '_title'), PlainText)
        assert getattr(getattr(instance, '_title'), '_text') == self.expected_title
        assert isinstance(getattr(instance, '_blocks'), BlocksArray)

        _section = getattr(getattr(instance, '_blocks'), '_blocks')[0]
        assert isinstance(_section, Section)
        assert _section.__eq__(self.expected_section)
        assert isinstance(getattr(instance, '_close'), PlainText)
        assert getattr(getattr(instance, '_close'), '_text') == self.expected_close
        assert isinstance(getattr(instance, '_submit'), PlainText)
        assert getattr(getattr(instance, '_submit'), '_text') == self.expected_submit
        assert getattr(instance, '_callback_id') == self.expected_callback_id
        assert getattr(instance, '_clear_on_close') == self.expected_clear_on_close
        assert getattr(instance, '_external_id') == self.expected_external_id
        assert getattr(instance, '_notify_on_close') == self.expected_notify_on_close
        assert getattr(instance, '_private_metadata') == self.expected_private_metadata

    @raises(AttributeError)
    def test_should_view_serialize_raise_attributeerror_if_trying_to_serialize_without_all_required_slots(self):

        # WHEN
        View.Builder().Blocks().Section().text__('any').up().up().build().serialize()

    def test_should_view_serialize_provide_correct_dict_and_json_data(self):

        # GIVEN
        instance = self.view_instance_all

        # WHEN
        serialized_dict = instance.serialize()
        serialized_json = instance.serialize(as_json=True)

        # THEN
        assert serialized_dict == self.expected_serialized_dict
        assert serialized_json == self.expected_serialized_json

    def test_should_view_deserialize_provide_correct_instances_from_dict_and_json(self):

        # GIVEN
        serialized_dict = self.expected_serialized_dict
        serialized_json = self.expected_serialized_json

        # WHEN
        instance_from_dict = View.deserialize(serialized_dict)
        instance_from_json = View.deserialize(serialized_json, from_json=True)

        # THEN
        assert isinstance(instance_from_dict, View)
        assert isinstance(instance_from_json, View)
        for instance in (instance_from_dict, instance_from_json):
            assert isinstance(getattr(instance, '_title'), PlainText)
            assert getattr(getattr(instance, '_title'), '_text') == self.expected_title
            assert isinstance(getattr(instance, '_blocks'), list)

            _section = getattr(instance, '_blocks')[0]
            assert isinstance(_section, Section)
            assert _section.__eq__(self.expected_section)
            assert isinstance(getattr(instance, '_close'), PlainText)
            assert getattr(getattr(instance, '_close'), '_text') == self.expected_close
            assert isinstance(getattr(instance, '_submit'), PlainText)
            assert getattr(getattr(instance, '_submit'), '_text') == self.expected_submit
            assert getattr(instance, '_callback_id') == self.expected_callback_id
            assert getattr(instance, '_clear_on_close') == self.expected_clear_on_close
            assert getattr(instance, '_external_id') == self.expected_external_id
            assert getattr(instance, '_notify_on_close') == self.expected_notify_on_close
            assert getattr(instance, '_private_metadata') == self.expected_private_metadata

    @raises(AssertionError)
    def test_should_serialize_raise_assertionerror_if_supplied_title_is_not_plaintext(self):

        # GIVEN
        instance = View.Builder().Blocks().Divider().up().up().build()
        setattr(instance, '_title', 'string that is not PlainText')

        # WHEN
        instance.serialize()

    @raises(AssertionError)
    def test_should_serialize_raise_assertionerror_if_supplied_title_lenght_is_longer_that_24(self):

        # GIVEN
        instance = View.Builder().title('0123456789012345678912345').Blocks().Divider().up().up().build()

        # WHEN
        instance.serialize()

    @raises(AssertionError)
    def test_should_serialize_raise_assertionerror_if_supplied_submit_is_not_plaintext(self):

        # GIVEN
        instance = View.Builder().title('any title').Blocks().Divider().up().up().build()
        setattr(instance, '_submit', 'string that is not PlainText')

        # WHEN
        instance.serialize()

    @raises(AssertionError)
    def test_should_serialize_raise_assertionerror_if_supplied_submit_lenght_is_longer_that_24(self):

        # GIVEN
        instance = View.Builder().title('any title').submit_('0123456789012345678912345') \
            .Blocks().Divider().up().up().build()

        # WHEN
        instance.serialize()

    @raises(AssertionError)
    def test_should_serialize_raise_assertionerror_if_supplied_close_is_not_plaintext(self):

        # GIVEN
        instance = View.Builder().title('any title').Blocks().Divider().up().up().build()
        setattr(instance, '_close', 'string that is not PlainText')

        # WHEN
        instance.serialize()

    @raises(AssertionError)
    def test_should_serialize_raise_assertionerror_if_supplied_close_lenght_is_longer_that_24(self):

        # GIVEN
        instance = View.Builder().title('any title').close_('1' * 25) \
            .Blocks().Divider().up().up().build()

        # WHEN
        instance.serialize()

    @raises(AssertionError)
    def test_should_serialize_raise_assertionerror_if_blocks_is_not_list_or_blocksarray(self):

        # GIVEN
        instance = View.Builder().title('any').build()
        setattr(instance, '_blocks', object())

        # WHEN
        instance.serialize()

    @raises(AssertionError)
    def test_should_serialize_raise_assertionerror_if_num_blocks_more_than_100(self):

        # GIVEN
        instance = View.Builder().title('any').build()
        setattr(instance, '_blocks', [Divider.Builder().build() for i in range(101)])

        # WHEN
        instance.serialize()

    @raises(AttributeError)
    def test_should_serialize_raise_assertionerror_if_blocks_contains_an_input_but_submit_is_not_set(self):

        # GIVEN
        instance = View.Builder().title('any').Blocks().Input().label('any').element() \
            .PlainTextInput().action_id('any').up().up().up().build()

        # WHEN
        instance.serialize()

    @raises(AssertionError)
    def test_should_serialize_raise_assertionerror_if_private_metadata_length_is_longer_than_3000(self):

        # GIVEN
        instance = View.Builder().title('any').Blocks().Divider().up().up().build()
        setattr(instance, '_private_metadata', '1' * 3001)

        # WHEN
        instance.serialize()

    @raises(AssertionError)
    def test_should_serialize_raise_assertionerror_if_callback_id_length_is_longer_than_255(self):

        # GIVEN
        instance = View.Builder().title('any').Blocks().Divider().up().up().build()
        setattr(instance, '_callback_id', '1' * 256)

        # WHEN
        instance.serialize()

    def test_should_modal_instance_create_view_with_corret_type(self):

        # GIVEN
        expected_type = 'modal'
        instance = Modal.Builder().title('any').Blocks().Divider().up().up().build()

        # THEN
        assert getattr(instance, '__type__') == expected_type

    def test_should_home_instance_create_view_with_corret_type(self):

        # GIVEN
        expected_type = 'home'
        instance = Home.Builder().title('any').Blocks().Divider().up().up().build()

        # THEN
        assert getattr(instance, '__type__') == expected_type

