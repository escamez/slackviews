"""
Class with nosetests for Confirmation AbstractBlock in slack_view library
"""

from nose.tools import raises

from slackviews.view import Confirmation, PlainText, MarkDown

__author__ = 'Agustin Escamez'
__email__ = 'aech22@gmail.com'


class TestConfirmation:

    def teardown(self):
        Confirmation.__all_slots__ = None

    def test_should_confirmation_builder_provide_a_valid_instance_with_required_values(self):

        # GIVEN
        expected_slots = ['_title', '_text', '_confirm', '_deny']
        expected_all_slots = ['_style']
        expected_all_slots.extend(expected_slots)
        expected_text = 'any text'
        expected_title = 'any title'
        expected_confirm = 'any confirm'
        expected_deny = 'any deny'

        # WHEN
        instance = Confirmation.Builder().text(expected_text).title(expected_title) \
            .confirm(expected_confirm).deny(expected_deny).build()

        # THEN
        assert hasattr(instance, '__all_slots__')
        assert hasattr(instance, '__slots__')
        for att in expected_slots:
            assert att in getattr(instance, '__slots__')
        for att in expected_all_slots:
            assert att in getattr(instance, '__all_slots__')

        assert isinstance(getattr(instance, '_title'), PlainText)
        assert isinstance(getattr(instance, '_confirm'), PlainText)
        assert isinstance(getattr(instance, '_deny'), PlainText)
        assert isinstance(getattr(instance, '_text'), MarkDown)

        assert getattr(getattr(instance, '_title'), '_text') == expected_title
        assert getattr(getattr(instance, '_confirm'), '_text') == expected_confirm
        assert getattr(getattr(instance, '_deny'), '_text') == expected_deny
        assert getattr(getattr(instance, '_text'), '_text') == expected_text

        assert not hasattr(instance, '_style')

    def test_should_confirmation_builder_provide_a_valid_instance_with_any_values(self):

        # GIVEN
        expected_style = 'any style'

        # WHEN
        instance = Confirmation.Builder().text('any text').title('any title') \
            .confirm('any confirm').deny('any deny').style_(expected_style).build()

        assert hasattr(instance, '_style')
        assert getattr(instance, '_style') == expected_style

    @raises(AttributeError)
    def test_should_confirmation_serialize_raise_attributeerror_if_trying_to_serialize_without_all_required_slots(self):

        # WHEN
        Confirmation.Builder().build().serialize()

    def test_should_confirmation_serialize_provide_correct_dict_and_json_data(self):

        # GIVEN
        expected_text = 'any text'
        expected_title = 'any title'
        expected_confirm = 'any confirm'
        expected_deny = 'any deny'

        expected_serialized_dict = {'deny': {'type': 'plain_text', 'text': expected_deny, 'emoji': False},
                                    'confirm': {'type': 'plain_text', 'text': expected_confirm, 'emoji': False},
                                    'text': {'type': 'mrkdwn', 'text': expected_text, 'verbatim': False},
                                    'title': {'type': 'plain_text', 'text': expected_title, 'emoji': False}}

        expected_serialized_json = f'{{"deny": {{"type": "plain_text", "text": "{expected_deny}", "emoji": false}}, ' \
                                   f'"confirm": {{"type": "plain_text", "text": "{expected_confirm}", "emoji": false}}, ' \
                                   f'"text": {{"type": "mrkdwn", "text": "{expected_text}", "verbatim": false}}, ' \
                                   f'"title": {{"type": "plain_text", "text": "{expected_title}", "emoji": false}}}}'

        instance = Confirmation.Builder().text(expected_text).title(expected_title).confirm(expected_confirm) \
            .deny(expected_deny).build()

        # WHEN
        serialized_dict = instance.serialize()
        serialized_json = instance.serialize(as_json=True)

        # THEN
        assert serialized_dict == expected_serialized_dict
        assert serialized_json == expected_serialized_json

    def test_should_confirmation_deserialize_provide_correct_instances_from_dict_and_json(self):

        # GIVEN
        expected_text = 'any text'
        expected_title = 'any title'
        expected_confirm = 'any confirm'
        expected_deny = 'any deny'

        serialized_dict = {'deny': {'type': 'plain_text', 'text': expected_deny, 'emoji': False},
                           'confirm': {'type': 'plain_text', 'text': expected_confirm, 'emoji': False},
                           'text': {'type': 'mrkdwn', 'text': expected_text, 'verbatim': False},
                           'title': {'type': 'plain_text', 'text': expected_title, 'emoji': False}}

        serialized_json = f'{{"deny": {{"type": "plain_text", "text": "{expected_deny}", "emoji": false}}, ' \
                          f'"confirm": {{"type": "plain_text", "text": "{expected_confirm}", "emoji": false}}, ' \
                          f'"text": {{"type": "mrkdwn", "text": "{expected_text}", "verbatim": false}}, ' \
                          f'"title": {{"type": "plain_text", "text": "{expected_title}", "emoji": false}}}}'

        # WHEN
        instance_from_dict = Confirmation.deserialize(serialized_dict)
        instance_from_json = Confirmation.deserialize(serialized_json, from_json=True)

        # THEN
        assert isinstance(instance_from_dict, Confirmation) and isinstance(instance_from_json, Confirmation)

        for instance in (instance_from_dict, instance_from_json):
            assert isinstance(getattr(instance, '_title'), PlainText)
            assert isinstance(getattr(instance, '_confirm'), PlainText)
            assert isinstance(getattr(instance, '_deny'), PlainText)
            assert getattr(getattr(instance, '_title'), '_text') == expected_title
            assert getattr(getattr(instance, '_confirm'), '_text') == expected_confirm
            assert getattr(getattr(instance, '_deny'), '_text') == expected_deny
            assert getattr(getattr(instance, '_text'), '_text') == expected_text
            assert not hasattr(instance, '_style')
