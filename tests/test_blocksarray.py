"""
Class with nosetests for BlocksArray AbstractBlock in slack_view library
"""

from nose.tools import raises

from slackviews.view import BlocksArray, AbstractBlock, Input, Divider, Section, Actions, \
    Context, Header

__author__ = 'Agustin Escamez'
__email__ = 'aech22@gmail.com'


class TestBlocksArray:

    def setup(self):

        _builder = BlocksArray.Builder()

        self.instance = BlocksArray.Builder() \
            .Input().label('any').element().PlainTextInput().action_id('any').up().up() \
            .Divider().up() \
            .Section().text__('any').up() \
            .Actions().element().Button().action_id('any').text('any').up().up() \
            .Context().element().Image().image_url('any').alt_text('any').up().up() \
            .build()

        self.serialized_dict = [{'type': 'input', 'element': {'type': 'plain_text_input', 'action_id': 'any'},
                                 'label': {'type': 'plain_text', 'text': 'any', 'emoji': False}},
                                {'type': 'divider'}, {'type': 'section', 'text': {'type': 'mrkdwn',
                                                                                  'text': 'any', 'verbatim': False}},
                                {'type': 'actions',
                                 'elements': [{'type': 'button', 'action_id': 'any',
                                               'text': {'type': 'plain_text', 'text': 'any', 'emoji': False}}]},
                                {'type': 'context', 'elements': [{'type': 'image',
                                                                  'alt_text': 'any', 'image_url': 'any'}]}]

        self.serialized_json = '[{"type": "input", "element": {"type": "plain_text_input", "action_id": "any"}, ' \
                               '"label": {"type": "plain_text", "text": "any", "emoji": false}}, ' \
                               '{"type": "divider"}, {"type": "section", "text": {"type": "mrkdwn", "text": "any", ' \
                               '"verbatim": false}}, {"type": "actions", "elements": [{"type": "button", ' \
                               '"action_id": "any", "text": {"type": "plain_text", "text": "any", ' \
                               '"emoji": false}}]}, {"type": "context", "elements": [{"type": "image",' \
                               ' "alt_text": "any", "image_url": "any"}]}]'

    def test_should_builder_provide_a_valid_instance(self):

        # GIVEN
        expected_slots = ['_blocks']

        # WHEN
        instance = BlocksArray.Builder().Divider().up().build()

        # THEN
        assert hasattr(instance, '__slots__')
        for att in expected_slots:
            assert att in getattr(instance, '__slots__')

        assert isinstance(instance, BlocksArray)
        assert isinstance(getattr(instance, '_blocks'), list)
        for block_ in getattr(instance, '_blocks'):
            assert isinstance(block_, AbstractBlock)

    def test_should_builder_create_correct_instance_type_of_abstractblock(self):

        # GIVEN
        _builder = BlocksArray.Builder()

        expected_input = Input.Builder().label('any').element().PlainTextInput().action_id('any').up().build()
        expected_divider = Divider.Builder().build()
        expected_header = Header.Builder().text('any').build()
        expected_section = Section.Builder().text__('any').build()
        expected_actions = Actions.Builder().element().Button().action_id('any').text('any').up().build()
        expected_context = Context.Builder().element().Image().image_url('any').alt_text('any').up().build()

        # WHEN
        _input = _builder.Input().label('any').element().PlainTextInput().action_id('any').up().build()
        _divider = _builder.Divider().build()
        _header = _builder.Header().text('any').build()
        _section = _builder.Section().text__('any').build()
        _actions = _builder.Actions().element().Button().action_id('any').text('any').up().build()
        _context = _builder.Context().element().Image().image_url('any').alt_text('any').up().build()

        # THEN
        assert isinstance(_input, Input)
        assert isinstance(_divider, Divider)
        assert isinstance(_header, Header)
        assert isinstance(_section, Section)
        assert isinstance(_actions, Actions)
        assert isinstance(_context, Context)

        assert _input.__eq__(expected_input)
        assert _divider.__eq__(expected_divider)
        assert _header.__eq__(expected_header)
        assert _section.__eq__(expected_section)
        assert _actions.__eq__(expected_actions)
        assert _context.__eq__(expected_context)

    def test_should_has_input_block_return_true_or_false_if_has_an_input_abstractblock_in_list_of_blocks(self):

        # GIVEN
        expected_instance_with_no_input = BlocksArray.Builder().Divider().up().build()
        expected_instance_with_input = BlocksArray.Builder().Input().label('any').element() \
            .PlainTextInput().action_id('any').up().up().build()

        # WHEN
        no_input = expected_instance_with_no_input.has_input_block()
        input = expected_instance_with_input.has_input_block()

        # THEN
        assert not no_input
        assert input

    def test_should_num_blocks_provide_correct_size_of_blocks_array(self):

        # GIVEN
        expected_blocks_size = 17
        instance = BlocksArray()
        setattr(instance, '_blocks', [Divider.Builder().build() for i in range(expected_blocks_size)])

        # WHEN
        assert len(getattr(instance, '_blocks')) == expected_blocks_size

    def test_should_serialize_provide_correct_output(self):

        # GIVEN
        expected_dict = self.serialized_dict
        expected_json = self.serialized_json

        # WHEN
        serialized_dict = self.instance.serialize()
        serialized_json = self.instance.serialize(as_json=True)

        # THEN
        assert expected_dict == serialized_dict
        assert serialized_json == expected_json

    def test_should_of_provide_correct_instance(self):

        # GIVEN
        serialized_dict = self.serialized_dict
        serialized_json = self.serialized_json

        # WHEN
        instance_from_dict = BlocksArray.of(serialized_dict)
        instance_from_json = BlocksArray.of(serialized_json, from_json=True)

        # THEN
        assert instance_from_dict.serialize() == serialized_dict
        assert instance_from_json.serialize(as_json=True) == serialized_json

    @raises(AssertionError)
    def test_should_of_raise_assertion_error_if_supplied_arg_is_not_a_list(self):

        # WHEN
        BlocksArray.of(object())

    @raises(AssertionError)
    def test_should_of_raise_assertion_error_if_supplied_array_of_dicts_contain_a_non_abstractblock_element(self):

        # WHEN
        BlocksArray.of([Divider.Builder().build(), object()])
