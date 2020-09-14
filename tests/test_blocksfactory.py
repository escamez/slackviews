"""
Class with nosetests for BlocksFactory in slack_view library
"""
from nose.tools import raises

from slackviews.view import PlainText, BlocksFactory, Actions, Button, Context, Confirmation, Divider, Header, Image, \
    MarkDown, Option, MultiSelectMenu, OptionGroup, Overflow, PlainTextInput, Section, SelectMenu, Input

__author__ = 'Agustin Escamez'
__email__ = 'aech22@gmail.com'


class TestPlainText:

    def teardown(self):
        PlainText.__all_slots__ = None

    @raises(AssertionError)
    def test_should_of_raise_assertionerror_if_supplied_arg_is_not_dict_from_json_is_false(self):
        # WHEN
        BlocksFactory.of(object())

    @raises(AssertionError)
    def test_should_of_raise_assertionerror_if_supplied_arg_is_not_str_and_from_json_is_true(self):
        # WHEN
        BlocksFactory.of({'any': 'dict'}, from_json=True)

    @raises(TypeError)
    def test_should_of_raise_typeerror_if_supplied_arg_is_not_a_dict_of_abstractblock(self):
        # WHEN
        BlocksFactory.of({'any': 'unknown dict'})

    def test_should_blocksfactory_provide_correct_plaintext_instance_from_serialized_dict_and_json(self):
        # GIVEN
        serialized_dict = {'type': 'plain_text', 'text': 'any text', 'emoji': False}
        serialized_json = '{"type": "plain_text", "text": "any text", "emoji": false}'

        # WHEN
        instance_from_dict = BlocksFactory.of(serialized_dict)
        instance_from_json = BlocksFactory.of(serialized_json, from_json=True)

        # THEN
        assert isinstance(instance_from_dict, PlainText)
        assert isinstance(instance_from_json, PlainText)

    def test_should_blocksfactory_provide_correct_confirmation_instance_from_serialized_dict_and_json(self):
        # GIVEN
        serialized_dict = {'deny': {'type': 'plain_text', 'text': 'any deny', 'emoji': False},
                           'confirm': {'type': 'plain_text', 'text': 'any confirm', 'emoji': False},
                           'text': {'type': 'mrkdwn', 'text': 'any text', 'verbatim': False},
                           'title': {'type': 'plain_text', 'text': 'any title', 'emoji': False}}

        serialized_json = '{"deny": {"type": "plain_text", "text": "any deny", "emoji": false},' \
                          ' "confirm": {"type": "plain_text", "text": "any confirm", "emoji": false}, ' \
                          '"text": {"type": "mrkdwn", "text": "any text", "verbatim": false}, ' \
                          '"title": {"type": "plain_text", "text": "any title", "emoji": false}}'

        # WHEN
        instance_from_dict = BlocksFactory.of(serialized_dict)
        instance_from_json = BlocksFactory.of(serialized_json, from_json=True)

        # THEN
        assert isinstance(instance_from_dict, Confirmation)
        assert isinstance(instance_from_json, Confirmation)

    def test_should_blocksfactory_provide_correct_divider_instance_from_serialized_dict_and_json(self):
        # GIVEN
        expected_block_id = 'any block id'
        serialized_dict = {'type': 'divider', 'block_id': expected_block_id}
        serialized_json = f'{{"type": "divider", "block_id": "{expected_block_id}"}}'

        # WHEN
        instance_from_dict = BlocksFactory.of(serialized_dict)
        instance_from_json = BlocksFactory.of(serialized_json, from_json=True)

        # THEN
        assert isinstance(instance_from_dict, Divider)
        assert isinstance(instance_from_json, Divider)

    def test_should_blocksfactory_provide_correct_header_instance_from_serialized_dict_and_json(self):
        # GIVEN
        serialized_dict = {'type': 'header', 'block_id': 'any block_id',
                           'text': {'type': 'plain_text', 'text': 'any text', 'emoji': False}}
        serialized_json = '{"type": "header", "block_id": "any block_id", ' \
                          '"text": {"type": "plain_text", "text": "any text", "emoji": false}}'

        # WHEN
        instance_from_dict = BlocksFactory.of(serialized_dict)
        instance_from_json = BlocksFactory.of(serialized_json, from_json=True)

        # THEN
        assert isinstance(instance_from_dict, Header)
        assert isinstance(instance_from_json, Header)

    def test_should_blocksfactory_provide_correct_button_instance_from_serialized_dict_and_json(self):
        # GIVEN
        serialized_dict = {'type': 'button', 'confirm': {'deny': {'type': 'plain_text', 'text': 'any deny',
                                                                  'emoji': False},
                                                         'confirm': {'type': 'plain_text', 'text': 'any confirm',
                                                                     'emoji': False},
                                                         'text': {'type': 'mrkdwn', 'text': 'any text',
                                                                  'verbatim': False},
                                                         'title': {'type': 'plain_text', 'text': 'any title',
                                                                   'emoji': False}}, 'style': 'any style',
                           'value': 'any value', 'url': 'any url', 'action_id': 'any action id',
                           'text': {'type': 'plain_text',
                                    'text': 'any text', 'emoji': False}}

        serialized_json = '{"type": "button", "confirm": {"deny": {"type": "plain_text", "text": "any deny", ' \
                          '"emoji": false}, "confirm": {"type": "plain_text", "text": "any confirm", "emoji": false},' \
                          ' "text": {"type": "mrkdwn", "text": "any text", "verbatim": false}, ' \
                          '"title": {"type": "plain_text", "text": "any title", "emoji": false}},' \
                          ' "style": "any style", "value": "any value", "url": "any url", ' \
                          '"action_id": "any action id", ' \
                          '"text": {"type": "plain_text", "text": "any text", "emoji": false}}'

        # WHEN
        instance_from_dict = BlocksFactory.of(serialized_dict)
        instance_from_json = BlocksFactory.of(serialized_json, from_json=True)

        # THEN
        assert isinstance(instance_from_dict, Button)
        assert isinstance(instance_from_json, Button)

    def test_should_blocksfactory_provide_correct_actions_instance_from_serialized_dict_and_json(self):
        # GIVEN
        expected_block_id = 'any block id'
        expected_button_text = 'any button text'
        expected_button_action_id = 'any action id'

        serialized_dict = {'type': 'actions', 'block_id': 'any block id',
                           'elements': [{'type': 'button', 'action_id': 'any action id',
                                         'text': {'type': 'plain_text', 'text': 'any button text',
                                                  'emoji': False}}]}

        serialized_json = f'{{"type": "actions", "block_id": "{expected_block_id}", ' \
                          f'"elements": [{{"type": "button", ' \
                          f'"action_id": "{expected_button_action_id}", ' \
                          f'"text": {{"type": "plain_text", "text": "{expected_button_text}", ' \
                          f'"emoji": false}}}}]}}'

        # WHEN
        instance_from_dict = BlocksFactory.of(serialized_dict)
        instance_from_json = BlocksFactory.of(serialized_json, from_json=True)

        # THEN
        assert isinstance(instance_from_dict, Actions)
        assert isinstance(instance_from_json, Actions)

    def test_should_blocksfactory_provide_correct_context_instance_from_serialized_dict_and_json(self):
        # GIVEN
        expected_block_id = 'any block id'
        expected_image_alt_text = 'any alt text'
        expected_image_url = 'any url'

        serialized_dict = {'type': 'context', 'block_id': expected_block_id,
                           'elements': [{'type': 'image', 'alt_text': expected_image_alt_text,
                                         'image_url': expected_image_url}]}

        serialized_json = f'{{"type": "context", "block_id": "{expected_block_id}", ' \
                          f'"elements": [{{"type": "image", ' \
                          f'"alt_text": "{expected_image_alt_text}", ' \
                          f'"image_url": "{expected_image_url}"}}]}}'

        # WHEN
        instance_from_dict = BlocksFactory.of(serialized_dict)
        instance_from_json = BlocksFactory.of(serialized_json, from_json=True)

        # THEN
        assert isinstance(instance_from_dict, Context)
        assert isinstance(instance_from_json, Context)

    def test_should_blocksfactory_provide_correct_image_instance_from_serialized_dict_and_json(self):
        # GIVEN
        serialized_dict = {'type': 'image', 'alt_text': 'any text', 'image_url': 'any url'}
        serialized_json = '{"type": "image", "alt_text": "any text", "image_url": "any url"}'

        # WHEN
        instance_from_dict = BlocksFactory.of(serialized_dict)
        instance_from_json = BlocksFactory.of(serialized_json, from_json=True)

        # THEN
        assert isinstance(instance_from_dict, Image)
        assert isinstance(instance_from_json, Image)

    def test_should_blocksfactory_provide_correct_markdown_instance_from_serialized_dict_and_json(self):
        # GIVEN
        serialized_dict = {'type': 'mrkdwn', 'text': 'any text', 'verbatim': False}
        serialized_json = '{"type": "mrkdwn", "text": "any text", "verbatim": false}'

        # WHEN
        instance_from_dict = BlocksFactory.of(serialized_dict)
        instance_from_json = BlocksFactory.of(serialized_json, from_json=True)

        # THEN
        assert isinstance(instance_from_dict, MarkDown)
        assert isinstance(instance_from_json, MarkDown)

    def test_should_blocksfactory_provide_correct_option_instance_from_serialized_dict_and_json(self):
        # GIVEN
        serialized_dict = {'url': 'any url', 'description': {'type': 'plain_text', 'text': 'any description',
                                                             'emoji': False},
                           'value': 'any value', 'text': {'type': 'plain_text', 'text': 'any text', 'emoji': False}}

        serialized_json = '{"url": "any url", "description": {"type": "plain_text", "text": "any description", ' \
                          '"emoji": false}, "value": "any value", "text": {"type": "plain_text", "text": "any text", ' \
                          '"emoji": false}}'

        # WHEN
        instance_from_dict = BlocksFactory.of(serialized_dict)
        instance_from_json = BlocksFactory.of(serialized_json, from_json=True)

        # THEN
        assert isinstance(instance_from_dict, Option)
        assert isinstance(instance_from_json, Option)

    def test_should_blocksfactory_provide_correct_optiongroup_instance_from_serialized_dict_and_json(self):
        # GIVEN
        expected_label = 'any label'
        expected_option0_text = 'option 1 text'
        expected_option0_value = 'option 1 value'
        expected_option1_text = 'option 2 text'
        expected_option1_value = 'option 2 value'

        expected_serialized_dict = {'options': [{'value': expected_option0_value,
                                                 'text': {'type': 'plain_text', 'text': expected_option0_text,
                                                          'emoji': False}},
                                                {'value': expected_option1_value,
                                                 'text': {'type': 'plain_text', 'text': expected_option1_text,
                                                          'emoji': False}}],
                                    'label': {'type': 'plain_text', 'text': expected_label, 'emoji': False}}

        expected_serialized_json = f'{{"options": [{{"value": "{expected_option0_value}", ' \
                                   f'"text": {{"type": "plain_text", "text": "{expected_option0_text}", ' \
                                   f'"emoji": false}}}}, {{"value": "{expected_option1_value}", ' \
                                   f'"text": {{"type": "plain_text", "text": "{expected_option1_text}", ' \
                                   f'"emoji": false}}}}], "label": {{"type": "plain_text", ' \
                                   f'"text": "{expected_label}", "emoji": false}}}}'

        serialized_dict = expected_serialized_dict
        serialized_json = expected_serialized_json

        # WHEN
        instance_from_dict = BlocksFactory.of(serialized_dict)
        instance_from_json = BlocksFactory.of(serialized_json, from_json=True)

        # THEN
        assert isinstance(instance_from_dict, OptionGroup)
        assert isinstance(instance_from_json, OptionGroup)

    def test_should_blocksfactory_provide_correct_multiselectmenu_instance_from_serialized_dict_and_json(self):
        # GIVEN
        expected_action_id = 'any action id'
        expected_placeholder = 'any placeholder'

        expected_option0_text = 'option 1 text'
        expected_option0_value = 'option 1 value'
        expected_option1_text = 'option 2 text'
        expected_option1_value = 'option 2 value'

        expected_confirmation_title = 'any title'
        expected_confirmation_confirm = 'any cofirm'
        expected_confirmation_deny = 'any deny'
        expected_confirmation_text = 'any text'

        expected_max_selected_items = 2

        serialized_dict = {'type': 'multi_static_select',
                           'confirm': {'deny': {'type': 'plain_text',
                                                'text': expected_confirmation_deny, 'emoji': False},
                                       'confirm': {'type': 'plain_text',
                                                   'text': expected_confirmation_confirm,
                                                   'emoji': False},
                                       'text': {'type': 'mrkdwn', 'text': expected_confirmation_text,
                                                'verbatim': False},
                                       'title': {'type': 'plain_text',
                                                 'text': expected_confirmation_title,
                                                 'emoji': False}},
                           'initial_option': {'value': expected_option0_value,
                                              'text': {'type': 'plain_text',
                                                       'text': expected_option0_text,
                                                       'emoji': False}},
                           'options': [{'value': expected_option0_value,
                                        'text': {'type': 'plain_text',
                                                 'text': expected_option0_text,
                                                 'emoji': False}},
                                       {'value': expected_option1_value,
                                        'text': {'type': 'plain_text',
                                                 'text': expected_option1_text,
                                                 'emoji': False}}],
                           'action_id': expected_action_id,
                           'placeholder': {'type': 'plain_text', 'text': expected_placeholder,
                                           'emoji': False},
                           'max_selected_items': expected_max_selected_items}

        serialized_json = f'{{"type": "multi_static_select", "confirm": {{"deny": ' \
                          f'{{"type": "plain_text", "text": "{expected_confirmation_deny}", ' \
                          f'"emoji": false}}, "confirm": {{"type": "plain_text", ' \
                          f'"text": "{expected_confirmation_confirm}", "emoji": false}}, ' \
                          f'"text": {{"type": "mrkdwn", "text": "{expected_confirmation_text}", ' \
                          f'"verbatim": false}}, "title": {{"type": "plain_text", ' \
                          f'"text": "{expected_confirmation_title}", "emoji": false}}}}, ' \
                          f'"initial_option": {{"value": "{expected_option0_value}", ' \
                          f'"text": {{"type": "plain_text", "text": "{expected_option0_text}", ' \
                          f'"emoji": false}}}}, "options": [{{"value": "{expected_option0_value}", ' \
                          f'"text": {{"type": "plain_text", "text": "{expected_option0_text}", ' \
                          f'"emoji": false}}}}, {{"value": "{expected_option1_value}", ' \
                          f'"text": {{"type": "plain_text", "text": "{expected_option1_text}", ' \
                          f'"emoji": false}}}}], "action_id": "{expected_action_id}", ' \
                          f'"placeholder": {{"type": "plain_text", ' \
                          f'"text": "{expected_placeholder}", "emoji": false}}, ' \
                          f'"max_selected_items": {expected_max_selected_items}}}'

        # WHEN
        instance_from_dict = BlocksFactory.of(serialized_dict)
        instance_from_json = BlocksFactory.of(serialized_json, from_json=True)

        # THEN
        assert isinstance(instance_from_dict, MultiSelectMenu)
        assert isinstance(instance_from_json, MultiSelectMenu)

    def test_should_blocksfactory_provide_correct_overflow_instance_from_serialized_dict_and_json(self):
        # GIVEN
        expected_action_id = 'any action id'

        expected_option0_text = 'option 1 text'
        expected_option0_value = 'option 1 value'
        expected_option1_text = 'option 2 text'
        expected_option1_value = 'option 2 value'

        expected_confirmation_title = 'any title'
        expected_confirmation_confirm = 'any cofirm'
        expected_confirmation_deny = 'any deny'
        expected_confirmation_text = 'any text'

        serialized_dict = {'type': 'overflow', 'confirm': {'deny': {'type': 'plain_text',
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

        serialized_json = f'{{"type": "overflow", ' \
                          f'"confirm": {{"deny": {{"type": "plain_text", ' \
                          f'"text": "{expected_confirmation_deny}", "emoji": false}}, ' \
                          f'"confirm": {{"type": "plain_text", ' \
                          f'"text": "{expected_confirmation_confirm}", "emoji": false}}, ' \
                          f'"text": {{"type": "mrkdwn", "text": "{expected_confirmation_text}", ' \
                          f'"verbatim": false}}, "title": {{"type": "plain_text", ' \
                          f'"text": "{expected_confirmation_title}", "emoji": false}}}}, ' \
                          f'"options": [{{"value": "{expected_option0_value}", ' \
                          f'"text": {{"type": "plain_text", "text": "{expected_option0_text}", ' \
                          f'"emoji": false}}}}, {{"value": "{expected_option1_value}", ' \
                          f'"text": {{"type": "plain_text", "text": "{expected_option1_text}", ' \
                          f'"emoji": false}}}}], "action_id": "{expected_action_id}"}}'

        # WHEN
        instance_from_dict = BlocksFactory.of(serialized_dict)
        instance_from_json = BlocksFactory.of(serialized_json, from_json=True)

        # THEN
        assert isinstance(instance_from_dict, Overflow)
        assert isinstance(instance_from_json, Overflow)

    def test_should_blocksfactory_provide_correct_plaintextinput_instance_from_serialized_dict_and_json(self):
        # GIVEN
        expected_action_id = 'any action id'
        expected_placeholder = 'any place holder'
        expected_multiline = True
        expected_initial_value = 'any initial value'
        expected_min_length = 1
        expected_max_length = 2

        serialized_dict = {'type': 'plain_text_input', 'max_length': expected_max_length,
                           'min_length': expected_min_length, 'multiline': expected_multiline,
                           'initial_value': expected_initial_value,
                           'placeholder': {'type': 'plain_text', 'text': expected_placeholder,
                                           'emoji': False}, 'action_id': expected_action_id}

        serialized_json = f'{{"type": "plain_text_input", "max_length": {expected_max_length}, ' \
                          f'"min_length": {expected_min_length}, ' \
                          f'"multiline": {str(expected_multiline).lower()}, ' \
                          f'"initial_value": "{expected_initial_value}", ' \
                          f'"placeholder": {{"type": "plain_text", ' \
                          f'"text": "{expected_placeholder}", "emoji": false}}, ' \
                          f'"action_id": "{expected_action_id}"}}'

        # WHEN
        instance_from_dict = BlocksFactory.of(serialized_dict)
        instance_from_json = BlocksFactory.of(serialized_json, from_json=True)

        # THEN
        assert isinstance(instance_from_dict, PlainTextInput)
        assert isinstance(instance_from_json, PlainTextInput)

    def test_should_blocksfactory_provide_correct_section_instance_from_serialized_dict_and_json(self):
        # GIVEN
        expected_text = 'any text'
        expected_block_id = 'any block id'

        serialized_dict = {'type': 'section',
                           'accessory': {'type': 'image', 'alt_text': 'any alt text',
                                         'image_url': 'any url'}, 'block_id': expected_block_id,
                           'text': {'type': 'mrkdwn', 'text': expected_text, 'verbatim': False}}

        serialized_json = f'{{"type": "section", "accessory": {{"type": "image", "alt_text": ' \
                          f'"any alt text", "image_url": "any url"}}, ' \
                          f'"block_id": "{expected_block_id}", "text": {{"type": "mrkdwn", ' \
                          f'"text": "any text", "verbatim": false}}}}'

        # WHEN
        instance_from_dict = BlocksFactory.of(serialized_dict)
        instance_from_json = BlocksFactory.of(serialized_json, from_json=True)

        # THEN
        assert isinstance(instance_from_dict, Section)
        assert isinstance(instance_from_json, Section)

    def test_should_blocksfactory_provide_correct_selectmenu_instance_from_serialized_dict_and_json(self):
        # GIVEN
        expected_action_id = 'any action id'
        expected_placeholder = 'any placeholder'

        expected_option0_text = 'option 1 text'
        expected_option0_value = 'option 1 value'
        expected_option1_text = 'option 2 text'
        expected_option1_value = 'option 2 value'

        expected_confirmation_title = 'any title'
        expected_confirmation_confirm = 'any cofirm'
        expected_confirmation_deny = 'any deny'
        expected_confirmation_text = 'any text'

        serialized_dict = {'type': 'static_select',
                           'confirm': {'deny': {'type': 'plain_text',
                                                'text': expected_confirmation_deny, 'emoji': False},
                                       'confirm': {'type': 'plain_text',
                                                   'text': expected_confirmation_confirm,
                                                   'emoji': False},
                                       'text': {'type': 'mrkdwn', 'text': expected_confirmation_text,
                                                'verbatim': False},
                                       'title': {'type': 'plain_text',
                                                 'text': expected_confirmation_title,
                                                 'emoji': False}},
                           'initial_option': {'value': expected_option0_value,
                                              'text': {'type': 'plain_text',
                                                       'text': expected_option0_text,
                                                       'emoji': False}},
                           'options': [{'value': expected_option0_value,
                                        'text': {'type': 'plain_text',
                                                 'text': expected_option0_text,
                                                 'emoji': False}},
                                       {'value': expected_option1_value,
                                        'text': {'type': 'plain_text',
                                                 'text': expected_option1_text,
                                                 'emoji': False}}],
                           'action_id': expected_action_id,
                           'placeholder': {'type': 'plain_text', 'text': expected_placeholder,
                                           'emoji': False}}

        serialized_json = f'{{"type": "static_select", "confirm": {{"deny": {{"type": "plain_text", ' \
                          f'"text": "{expected_confirmation_deny}", "emoji": false}}, ' \
                          f'"confirm": {{"type": "plain_text", ' \
                          f'"text": "{expected_confirmation_confirm}", "emoji": false}}, ' \
                          f'"text": {{"type": "mrkdwn", "text": "{expected_confirmation_text}", ' \
                          f'"verbatim": false}}, "title": {{"type": "plain_text", ' \
                          f'"text": "{expected_confirmation_title}", "emoji": false}}}}, ' \
                          f'"initial_option": {{"value": "{expected_option0_value}", ' \
                          f'"text": {{"type": "plain_text", "text": "{expected_option0_text}", ' \
                          f'"emoji": false}}}}, "options": [{{"value": "{expected_option0_value}", ' \
                          f'"text": {{"type": "plain_text", "text": "{expected_option0_text}", ' \
                          f'"emoji": false}}}}, {{"value": "{expected_option1_value}", ' \
                          f'"text": {{"type": "plain_text", "text": "{expected_option1_text}", ' \
                          f'"emoji": false}}}}], "action_id": "{expected_action_id}", ' \
                          f'"placeholder": {{"type": "plain_text", ' \
                          f'"text": "{expected_placeholder}", "emoji": false}}}}'

        # WHEN
        instance_from_dict = BlocksFactory.of(serialized_dict)
        instance_from_json = BlocksFactory.of(serialized_json, from_json=True)

        # THEN
        assert isinstance(instance_from_dict, SelectMenu)
        assert isinstance(instance_from_json, SelectMenu)

    def test_should_blocksfactory_provide_correct_input_instance_from_serialized_dict_and_json(self):
        # GIVEN
        expected_label = 'any label'
        expected_block_id = 'any block id'
        expected_hint = 'any hint'
        expected_optional = False
        expected_instance = Input.Builder().label(expected_label).block_id_(expected_block_id) \
            .optional_(expected_optional).hint_(expected_hint).element().SelectMenu() \
            .action_id('any action id').placeholder('any placeholder').Option__().text('o text 1').value('o value 1') \
            .up().Option__().text('o text 2').value('o value 2').up().up().build()

        serialized_dict = {'type': 'input', 'optional': False,
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

        serialized_json = '{"type": "input", "optional": false, "hint": {"type": "plain_text", ' \
                          '"text": "any hint", "emoji": false}, "block_id": "any block id", ' \
                          '"element": {"type": "static_select", "options": [{"value": "o value 1",' \
                          ' "text": {"type": "plain_text", "text": "o text 1", "emoji": false}}, ' \
                          '{"value": "o value 2", "text": {"type": "plain_text", "text": "o text 2", ' \
                          '"emoji": false}}], "action_id": "any action id", "placeholder": ' \
                          '{"type": "plain_text", "text": "any placeholder", "emoji": false}}, ' \
                          '"label": {"type": "plain_text", "text": "any label", "emoji": false}}'

        # WHEN
        instance_from_dict = BlocksFactory.of(serialized_dict)
        instance_from_json = BlocksFactory.of(serialized_json, from_json=True)

        # THEN
        assert isinstance(instance_from_dict, Input)
        assert isinstance(instance_from_json, Input)
        assert instance_from_dict.__eq__(expected_instance)
        assert instance_from_json.__eq__(expected_instance)
