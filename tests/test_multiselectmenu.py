"""
Class with nosetests for MultiSelectMenu AbstractBlock in slack_view library
"""
from nose.tools import raises

from slackviews.view import PlainText, Option, MultiSelectMenu, Confirmation

__author__ = 'Agustin Escamez'
__email__ = 'aech22@gmail.com'


class TestMultiSelectMenu:

    def setup(self):

        self.expected_action_id = 'any action id'
        self.expected_placeholder = 'any placeholder'

        self.expected_option0_text = 'option 1 text'
        self.expected_option0_value = 'option 1 value'
        self.expected_option1_text = 'option 2 text'
        self.expected_option1_value = 'option 2 value'

        self.expected_confirmation_title = 'any title'
        self.expected_confirmation_confirm = 'any cofirm'
        self.expected_confirmation_deny = 'any deny'
        self.expected_confirmation_text = 'any text'

        self.expected_max_selected_items = 2

        self.expected_option0 = Option.Builder().text(self.expected_option0_text).value(self.expected_option0_value) \
            .build()
        self.expected_option1 = Option.Builder().text(self.expected_option1_text).value(self.expected_option1_value) \
            .build()

        _builder = MultiSelectMenu.Builder().action_id(self.expected_action_id).placeholder(self.expected_placeholder)
        self.multiselectmenu_instance_required = _builder.build()

        _builder = MultiSelectMenu.Builder().action_id(self.expected_action_id).placeholder(self.expected_placeholder)
        self.expected_option0 = Option.Builder().text(self.expected_option0_text).value(
            self.expected_option0_value).build()
        self.expected_option1 = Option.Builder().text(self.expected_option1_text).value(
            self.expected_option1_value).build()

        self.expected_options = [self.expected_option0, self.expected_option1]
        for opt_ in self.expected_options:
            _builder.Option__().text(getattr(getattr(opt_, '_text'), '_text')).value(getattr(opt_, '_value'))

        _builder.Confirm_() \
            .title(self.expected_confirmation_title) \
            .text(self.expected_confirmation_text) \
            .confirm(self.expected_confirmation_confirm) \
            .deny(self.expected_confirmation_deny)

        _builder.initial_option_(self.expected_option0_text)
        _builder.max_selected_items_(self.expected_max_selected_items)

        self.multiselectmenu_instance_all = _builder.build()

        self.expected_serialized_dict = {'type': 'multi_static_select',
                                         'confirm': {'deny': {'type': 'plain_text',
                                                              'text': self.expected_confirmation_deny, 'emoji': False},
                                                     'confirm': {'type': 'plain_text',
                                                                 'text': self.expected_confirmation_confirm,
                                                                 'emoji': False},
                                                     'text': {'type': 'mrkdwn', 'text': self.expected_confirmation_text,
                                                              'verbatim': False},
                                                     'title': {'type': 'plain_text',
                                                               'text': self.expected_confirmation_title,
                                                               'emoji': False}},
                                         'initial_option': {'value': self.expected_option0_value,
                                                            'text': {'type': 'plain_text',
                                                                     'text': self.expected_option0_text,
                                                                     'emoji': False}},
                                         'options': [{'value': self.expected_option0_value,
                                                      'text': {'type': 'plain_text',
                                                               'text': self.expected_option0_text,
                                                               'emoji': False}},
                                                     {'value': self.expected_option1_value,
                                                      'text': {'type': 'plain_text',
                                                               'text': self.expected_option1_text,
                                                               'emoji': False}}],
                                         'action_id': self.expected_action_id,
                                         'placeholder': {'type': 'plain_text', 'text': self.expected_placeholder,
                                                         'emoji': False},
                                         'max_selected_items': self.expected_max_selected_items}

        self.expected_serialized_json = f'{{"type": "multi_static_select", "confirm": {{"deny": ' \
                                        f'{{"type": "plain_text", "text": "{self.expected_confirmation_deny}", ' \
                                        f'"emoji": false}}, "confirm": {{"type": "plain_text", ' \
                                        f'"text": "{self.expected_confirmation_confirm}", "emoji": false}}, ' \
                                        f'"text": {{"type": "mrkdwn", "text": "{self.expected_confirmation_text}", ' \
                                        f'"verbatim": false}}, "title": {{"type": "plain_text", ' \
                                        f'"text": "{self.expected_confirmation_title}", "emoji": false}}}}, ' \
                                        f'"initial_option": {{"value": "{self.expected_option0_value}", ' \
                                        f'"text": {{"type": "plain_text", "text": "{self.expected_option0_text}", ' \
                                        f'"emoji": false}}}}, "options": [{{"value": "{self.expected_option0_value}", '\
                                        f'"text": {{"type": "plain_text", "text": "{self.expected_option0_text}", ' \
                                        f'"emoji": false}}}}, {{"value": "{self.expected_option1_value}", ' \
                                        f'"text": {{"type": "plain_text", "text": "{self.expected_option1_text}", '\
                                        f'"emoji": false}}}}], "action_id": "{self.expected_action_id}", ' \
                                        f'"placeholder": {{"type": "plain_text", ' \
                                        f'"text": "{self.expected_placeholder}", "emoji": false}}, '\
                                        f'"max_selected_items": {self.expected_max_selected_items}}}'

    def teardown(self):
        MultiSelectMenu.__all_slots__ = None

    def test_should_multiselectmenu_builder_provide_a_valid_instance_with_required_values(self):

        # GIVEN
        expected_slots = ['_max_selected_items']
        expected_all_slots = ['_placeholder', '_action_id', '_options', '_option_groups', '_initial_option', '_confirm']
        expected_all_slots.extend(expected_slots)

        # WHEN
        instance = self.multiselectmenu_instance_required

        # THEN
        assert isinstance(instance, MultiSelectMenu)
        assert hasattr(instance, '__all_slots__')
        assert hasattr(instance, '__slots__')
        for att in expected_slots:
            assert att in getattr(instance, '__slots__')
        for att in expected_all_slots:
            assert att in getattr(instance, '__all_slots__')

        assert isinstance(getattr(instance, '_placeholder'), PlainText)
        assert getattr(getattr(instance, '_placeholder'), '_text') == self.expected_placeholder
        assert getattr(instance, '_action_id') == self.expected_action_id

        assert not hasattr(instance, '_options')
        assert not hasattr(instance, '_option_groups')
        assert not hasattr(instance, '_initial_option')
        assert not hasattr(instance, '_confirm')
        assert not hasattr(instance, '_max_selected_items')

    @raises(AssertionError)
    def test_should_multiselectmenu_serialize_raise_assert_error_when_both_mutually_exclusive_options_are_given(self):
        # GIVEN
        multiselectmenu = self.multiselectmenu_instance_required
        setattr(multiselectmenu, '_options', 'any options')
        setattr(multiselectmenu, '_option_groups', 'an option group when options exists')

        # WHEN
        multiselectmenu.serialize()

    def test_should_multiselectmenu_builder_provide_a_valid_instance_with_any_values(self):

        # GIVEN
        instance = self.multiselectmenu_instance_all

        # THEN
        assert isinstance(getattr(instance, '_confirm'), Confirmation)
        assert isinstance(getattr(instance, '_options'), list)
        assert isinstance(getattr(instance, '_initial_option'), Option)

        _confirmation = getattr(instance, '_confirm')
        assert getattr(getattr(_confirmation, '_title'), '_text') == self.expected_confirmation_title
        assert getattr(getattr(_confirmation, '_text'), '_text') == self.expected_confirmation_text
        assert getattr(getattr(_confirmation, '_confirm'), '_text') == self.expected_confirmation_confirm
        assert getattr(getattr(_confirmation, '_deny'), '_text') == self.expected_confirmation_deny
        assert getattr(instance, '_initial_option').__eq__(self.expected_option0)

        _options = getattr(instance, '_options')
        assert _options[0].__eq__(self.expected_option0)
        assert _options[1].__eq__(self.expected_option1)

        assert getattr(instance, '_max_selected_items') == self.expected_max_selected_items

    @raises(AttributeError)
    def test_should_multiselectmenu_serialize_raise_attributeerror_if_serialize_with_only_actionid(self):

        # WHEN
        MultiSelectMenu.Builder().action_id('any').build().serialize()

    @raises(AttributeError)
    def test_should_multiselectmenu_serialize_raise_attributeerror_if_serialize_with_only_placeholder(self):

        # WHEN
        MultiSelectMenu.Builder().placeholder('any').build().serialize()

    def test_should_multiselectmenu_serialize_provide_correct_dict_and_json_data(self):

        # GIVEN
        instance = self.multiselectmenu_instance_all

        # WHEN
        serialized_dict = instance.serialize()
        serialized_json = instance.serialize(as_json=True)

        # THEN
        assert serialized_dict == self.expected_serialized_dict
        assert serialized_json == self.expected_serialized_json

    def test_should_multiselectmenu_deserialize_provide_correct_instances_from_dict_and_json(self):

        # GIVEN
        serialized_dict = self.expected_serialized_dict
        serialized_json = self.expected_serialized_json

        # WHEN
        instance_from_dict = MultiSelectMenu.deserialize(serialized_dict)
        instance_from_json = MultiSelectMenu.deserialize(serialized_json, from_json=True)

        # THEN
        assert isinstance(instance_from_dict, MultiSelectMenu)
        assert isinstance(instance_from_json, MultiSelectMenu)
        for instance in (instance_from_dict, instance_from_json):
            assert isinstance(getattr(instance, '_placeholder'), PlainText)
            assert getattr(getattr(instance, '_placeholder'), '_text') == self.expected_placeholder
            assert getattr(instance, '_action_id') == self.expected_action_id

            assert isinstance(getattr(instance, '_confirm'), Confirmation)
            assert isinstance(getattr(instance, '_options'), list)
            assert isinstance(getattr(instance, '_initial_option'), Option)

            _confirmation = getattr(instance, '_confirm')
            assert getattr(getattr(_confirmation, '_title'), '_text') == self.expected_confirmation_title
            assert getattr(getattr(_confirmation, '_text'), '_text') == self.expected_confirmation_text
            assert getattr(getattr(_confirmation, '_confirm'), '_text') == self.expected_confirmation_confirm
            assert getattr(getattr(_confirmation, '_deny'), '_text') == self.expected_confirmation_deny
            assert getattr(instance, '_initial_option').__eq__(self.expected_option0)

            _options = getattr(instance, '_options')
            assert _options[0].__eq__(self.expected_option0)
            assert _options[1].__eq__(self.expected_option1)

            assert getattr(instance, '_max_selected_items') == self.expected_max_selected_items

    def test_should_builder_create_instance_if_option_groups_are_used_instead_of_options(self):

        # WHEN
        instance = MultiSelectMenu.Builder().placeholder('any placeholder').action_id('any actionid') \
            .OptionGroup__().label('any label').Option().text('any text').value('any value').up().up().build()

        # THEN
        assert isinstance(instance, MultiSelectMenu)
        assert hasattr(instance, '_option_groups')
        assert not hasattr(instance, '_option')
        assert isinstance(getattr(instance, '_option_groups'), list)
        assert len(getattr(instance, '_option_groups')) == 1

    def test_should_serialize_instance_work_correctly_if_option_groups_are_used_instead_of_options(self):

        # GIVEN
        expected_serialized_dict = {'type': 'multi_static_select',
                                    'option_groups': [{'options': [{'value': 'any value',
                                                                    'text': {'type': 'plain_text', 'text': 'any text',
                                                                             'emoji': False}}],
                                                       'label': {'type': 'plain_text', 'text': 'any label',
                                                                 'emoji': False}}],
                                    'action_id': 'any actionid',
                                    'placeholder': {'type': 'plain_text', 'text': 'any placeholder', 'emoji': False}}

        expected_serialized_json = '{"type": "multi_static_select", "option_groups": [{"options": [{"value": "any value", ' \
                                   '"text": {"type": "plain_text", "text": "any text", "emoji": false}}], ' \
                                   '"label": {"type": "plain_text", "text": "any label", "emoji": false}}], ' \
                                   '"action_id": "any actionid", "placeholder": {"type": "plain_text", ' \
                                   '"text": "any placeholder", "emoji": false}}'


        instance = MultiSelectMenu.Builder().placeholder('any placeholder').action_id('any actionid') \
            .OptionGroup__().label('any label').Option().text('any text').value('any value').up().up().build()

        # WHEN
        serialized_dict = instance.serialize()
        serialized_json = instance.serialize(as_json=True)

        # THEN
        assert serialized_dict == expected_serialized_dict
        assert serialized_json == expected_serialized_json

    def test_should_get_default_provide_correct_initial_option_if_options_defined(self):

        # GIVEN
        instance = self.multiselectmenu_instance_all

        # WHEN
        initial_option = instance.get_default()

        # THEN
        assert initial_option.__eq__(self.expected_option0)

    def test_should_get_default_provide_correct_initial_option_if_optiongroups_defined(self):

        # GIVEN
        expected_text = 'any option text'
        expected_value = 'any option value'
        default_by_text = MultiSelectMenu.Builder().action_id('any actionid').placeholder('any placeholder') \
            .OptionGroup__().label('any label').Option().text(expected_text).value(expected_value).up() \
            .up().initial_option_(expected_text).build()
        default_by_value = MultiSelectMenu.Builder().action_id('any actionid').placeholder('any placeholder') \
            .OptionGroup__().label('any label').Option().text(expected_text).value(expected_value).up() \
            .up().initial_option_(expected_value).build()

        # WHEN
        initial_option_by_text = default_by_text.get_default()
        initial_option_by_value = default_by_value.get_default()

        # THEN
        for instance in (initial_option_by_text, initial_option_by_value):
            assert isinstance(instance, Option)
            assert getattr(getattr(initial_option_by_text, '_text'), '_text') == expected_text
            assert getattr(initial_option_by_text, '_value') == expected_value
            assert getattr(getattr(initial_option_by_value, '_text'), '_text') == expected_text
            assert getattr(initial_option_by_value, '_value') == expected_value

    def test_should_get_default_provide_none_if_no_initial_option_is_defined(self):

        # GIVEN
        instance = self.multiselectmenu_instance_required

        # WHEN
        initial_option = instance.get_default()

        # THEN
        assert not initial_option

    def test_should_has_option_provide_correct_answer_if_initial_option_is_defined(self):

        # GIVEN
        instance_without_options = self.multiselectmenu_instance_required
        instance_with_options = self.multiselectmenu_instance_all

        # WHEN
        with_options = instance_with_options.has_option(self.expected_option0_text)
        without_options = instance_without_options.has_option(self.expected_option0_text)

        # THEN
        assert with_options and not without_options

    @raises(AttributeError)
    def test_should_set_default_raise_attributeerror_if_supplied_option_does_not_exists(self):

        # GIVEN
        instance = self.multiselectmenu_instance_all

        # WHEN
        instance.set_default('non existing text or value')

    @raises(AttributeError)
    def test_should_initial_option_raise_attributeerror_if_no_option_or_optiongroups_exists(self):

        # GIVEN
        _builder = MultiSelectMenu.Builder().placeholder('any placeholder').action_id('any action_id')

        # WHEN
        _builder.initial_option_('any value when no options or option_groups exist')

