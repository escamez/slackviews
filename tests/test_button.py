"""
Class with nosetests for Button AbstractBlock in slack_view library
"""

from nose.tools import raises

from slackviews.view import Button, PlainText, Confirmation

__author__ = 'Agustin Escamez'
__email__ = 'aech22@gmail.com'


class TestConfirmation:

    def teardown(self):
        Button.__all_slots__ = None

    def test_should_button_builder_provide_a_valid_instance_with_required_values(self):

        # GIVEN
        expected_slots = ['_text', '_action_id']
        expected_all_slots = ['_url', '_value', '_style', '_confirm']
        expected_all_slots.extend(expected_slots)
        expected_text = 'any text'
        expected_action_id = 'any action id'

        # WHEN
        instance = Button.Builder().text(expected_text).action_id(expected_action_id).build()

        # THEN
        assert hasattr(instance, '__all_slots__')
        assert hasattr(instance, '__slots__')
        for att in expected_slots:
            assert att in getattr(instance, '__slots__')
        for att in expected_all_slots:
            assert att in getattr(instance, '__all_slots__')

        assert isinstance(getattr(instance, '_text'), PlainText)
        assert getattr(getattr(instance, '_text'), '_text') == expected_text
        assert getattr(instance, '_action_id') == expected_action_id

        assert not hasattr(instance, '_url')
        assert not hasattr(instance, '_value')
        assert not hasattr(instance, '_style')
        assert not hasattr(instance, '_confirm')

    def test_should_button_builder_provide_a_valid_instance_with_any_values(self):

        # GIVEN
        expected_text = 'any text'
        expected_action_id = 'any action id'
        expected_url = 'any url'
        expected_value = 'any value'
        expected_style = 'any style'
        expected_confirm_text = 'any text'
        expected_confirm_title = 'any title'
        expected_confirm_confirm = 'any confirm'
        expected_confirm_deny = 'any deny'

        # WHEN
        instance = Button.Builder().text(expected_text).action_id(expected_action_id).url_(expected_url) \
            .value_(expected_value).style_(expected_style).Confirm_().text(expected_confirm_text) \
            .title(expected_confirm_title).confirm(expected_confirm_confirm).deny(expected_confirm_deny) \
            .up().build()

        _confirmation = getattr(instance, '_confirm')

        # THEN
        assert isinstance(getattr(instance, '_text'), PlainText)
        assert getattr(getattr(instance, '_text'), '_text') == expected_text
        assert getattr(instance, '_action_id') == expected_action_id
        assert getattr(instance, '_url') == expected_url
        assert getattr(instance, '_value') == expected_value
        assert getattr(instance, '_style') == expected_style
        assert getattr(instance, '_action_id') == expected_action_id

        assert isinstance(_confirmation, Confirmation)
        assert isinstance(getattr(_confirmation, '_title'), PlainText)
        assert isinstance(getattr(_confirmation, '_confirm'), PlainText)
        assert isinstance(getattr(_confirmation, '_deny'), PlainText)
        assert getattr(getattr(_confirmation, '_title'), '_text') == expected_confirm_title
        assert getattr(getattr(_confirmation, '_confirm'), '_text') == expected_confirm_confirm
        assert getattr(getattr(_confirmation, '_deny'), '_text') == expected_confirm_deny
        assert getattr(getattr(_confirmation, '_text'), '_text') == expected_confirm_text
        assert not hasattr(_confirmation, '_style')

    @raises(AttributeError)
    def test_should_button_serialize_raise_attributeerror_if_trying_to_serialize_without_all_required_slots(self):

        # WHEN
        Button.Builder().build().serialize()

    def test_should_button_serialize_provide_correct_dict_and_json_data(self):

        # GIVEN
        expected_text = 'any text'
        expected_action_id = 'any action id'
        expected_url = 'any url'
        expected_value = 'any value'
        expected_style = 'any style'
        expected_confirm_text = 'any text'
        expected_confirm_title = 'any title'
        expected_confirm_confirm = 'any confirm'
        expected_confirm_deny = 'any deny'

        expected_serialized_dict = {'type': 'button', 'confirm':
            {'deny': {'type': 'plain_text', 'text': expected_confirm_deny, 'emoji': False},
             'confirm': {'type': 'plain_text', 'text': expected_confirm_confirm, 'emoji': False},
             'text': {'type': 'mrkdwn', 'text': expected_confirm_text, 'verbatim': False},
             'title': {'type': 'plain_text', 'text': expected_confirm_title, 'emoji': False}}, 'style': expected_style,
                                    'value': expected_value, 'url': expected_url, 'action_id': expected_action_id,
                                    'text': {'type': 'plain_text', 'text': expected_text, 'emoji': False}}

        expected_serialized_json = f'{{"type": "button", "confirm": {{"deny": {{"type": "plain_text",' \
                                   f' "text": "{expected_confirm_deny}", "emoji": false}}, ' \
                                   f'"confirm": {{"type": "plain_text", "text": "{expected_confirm_confirm}", ' \
                                   f'"emoji": false}}, "text": {{"type": "mrkdwn", "text": "{expected_confirm_text}", ' \
                                   f'"verbatim": false}}, "title": {{"type": "plain_text", ' \
                                   f'"text": "{expected_confirm_title}", "emoji": false}}}}, ' \
                                   f'"style": "{expected_style}", "value": "{expected_value}", ' \
                                   f'"url": "{expected_url}", "action_id": "{expected_action_id}", ' \
                                   f'"text": {{"type": "plain_text", "text": "{expected_text}", ' \
                                   f'"emoji": false}}}}'

        instance = Button.Builder().text(expected_text).action_id(expected_action_id).url_(expected_url) \
            .value_(expected_value).style_(expected_style).Confirm_().text(expected_confirm_text) \
            .title(expected_confirm_title).confirm(expected_confirm_confirm).deny(expected_confirm_deny) \
            .up().build()

        # WHEN
        serialized_dict = instance.serialize()
        serialized_json = instance.serialize(as_json=True)

        # THEN
        assert serialized_dict == expected_serialized_dict
        assert serialized_json == expected_serialized_json

    def test_should_button_deserialize_provide_correct_instances_from_dict_and_json(self):

        # GIVEN
        expected_text = 'any text'
        expected_action_id = 'any action id'
        expected_url = 'any url'
        expected_value = 'any value'
        expected_style = 'any style'
        expected_confirm_text = 'any text'
        expected_confirm_title = 'any title'
        expected_confirm_confirm = 'any confirm'
        expected_confirm_deny = 'any deny'

        serialized_dict = {'type': 'button', 'confirm':
            {'deny': {'type': 'plain_text', 'text': expected_confirm_deny, 'emoji': False},
             'confirm': {'type': 'plain_text', 'text': expected_confirm_confirm, 'emoji': False},
             'text': {'type': 'mrkdwn', 'text': expected_confirm_text, 'verbatim': False},
             'title': {'type': 'plain_text', 'text': expected_confirm_title, 'emoji': False}}, 'style': expected_style,
                           'value': expected_value, 'url': expected_url, 'action_id': expected_action_id,
                           'text': {'type': 'plain_text', 'text': expected_text, 'emoji': False}}

        serialized_json = f'{{"type": "button", "confirm": {{"deny": {{"type": "plain_text",' \
                          f' "text": "{expected_confirm_deny}", "emoji": false}}, ' \
                          f'"confirm": {{"type": "plain_text", "text": "{expected_confirm_confirm}", ' \
                          f'"emoji": false}}, "text": {{"type": "mrkdwn", "text": "{expected_confirm_text}", ' \
                          f'"verbatim": false}}, "title": {{"type": "plain_text", ' \
                          f'"text": "{expected_confirm_title}", "emoji": false}}}}, ' \
                          f'"style": "{expected_style}", "value": "{expected_value}", ' \
                          f'"url": "{expected_url}", "action_id": "{expected_action_id}", ' \
                          f'"text": {{"type": "plain_text", "text": "{expected_text}", ' \
                          f'"emoji": false}}}}'
        # WHEN
        instance_from_dict = Button.deserialize(serialized_dict)
        instance_from_json = Button.deserialize(serialized_json, from_json=True)

        # THEN
        assert isinstance(instance_from_dict, Button) and isinstance(instance_from_json, Button)

        for instance in (instance_from_dict, instance_from_json):
            _confirmation = getattr(instance, '_confirm')

            assert isinstance(getattr(instance, '_text'), PlainText)
            assert getattr(getattr(instance, '_text'), '_text') == expected_text
            assert getattr(instance, '_action_id') == expected_action_id
            assert getattr(instance, '_url') == expected_url
            assert getattr(instance, '_value') == expected_value
            assert getattr(instance, '_style') == expected_style
            assert getattr(instance, '_action_id') == expected_action_id

            assert isinstance(_confirmation, Confirmation)
            assert isinstance(getattr(_confirmation, '_title'), PlainText)
            assert isinstance(getattr(_confirmation, '_confirm'), PlainText)
            assert isinstance(getattr(_confirmation, '_deny'), PlainText)
            assert getattr(getattr(_confirmation, '_title'), '_text') == expected_confirm_title
            assert getattr(getattr(_confirmation, '_confirm'), '_text') == expected_confirm_confirm
            assert getattr(getattr(_confirmation, '_deny'), '_text') == expected_confirm_deny
            assert getattr(getattr(_confirmation, '_text'), '_text') == expected_confirm_text
            assert not hasattr(_confirmation, '_style')
