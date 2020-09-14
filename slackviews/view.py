"""
Module with most of Slack types of Blocks and layouts, that can be used to build Views using the builder pattern,
if needed.

# Introduction

    instance = <AbstractBlock>.Builder().any_method(value).AnyOtherBlockElement().method_of_new_block().up() \
                                        .other_method_of_initial_block()...

The methods of each builder, has a syntax to distinguish between required, optional or mutually exclusive options where
only one of two attributes is required


Syntax

There is a convention to distinguish between *required*, *optional* and *mutually exclusive* attributes:

 - required attributes*: Required attributes are represented for those builder's methods that **do not** have
   underscores at all.

 - optional attributes: Optional attributes are represented for those builder's methods that **do** have **one**
   underscore at the end, for example: `text()`, `element()`, ...

 - mutually exclusive attributes: In those cases where only one out of two attributes can be set, are represented
 for those builder's methods that **do** have a **double underscored** at the end, for example: `field__()`,
 `text__()`, ...

NOTE:

    Only mrkdwn available in those elements where plain_text or mrkdwn are allowed
"""

__author__ = 'Agustin Escamez'
__email__ = 'aech22@gmail.com'

import abc
import importlib
import json


# ################# #
# -- block elements #
# ################# #


class AbstractBlock:
    """
    Main class that represents an instance of a Block element in Slack. Any instance that represents
    a block will inherit from it
    """
    __metaclass__ = abc.ABCMeta

    # strict tuple of block fields
    __slots__ = ()

    # all slots from inheritance chain. Helps during deserialization
    __all_slots__ = None

    # the kind of block being built
    __type__ = None

    # Slots that are required to define for each type of block
    __required_slots__ = ()

    # A tuple with slots that are mutually exclusive.
    # For some type of blocks, it's required to provide one of these slots, but not both of them, that's why they
    # are not included in required_slots
    __mutually_exclusive_slots__ = ()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '__type__'):
            raise AttributeError('Missing required class attribute __type__')

        # initialize __all_slots__
        if not getattr(cls, '__all_slots__'):
            slots_ = list()
            for c in [c for c in cls.__mro__ if c.__name__ != 'object']:
                slots_.extend(c.__slots__)
            setattr(cls, '__all_slots__', tuple(reversed(slots_)))
        return super().__new__(cls)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

        # check block spec
        self._validation()

    def __eq__(self, other):
        """
        Two instances are equal if their serialization dict matches
        :param other: Another instance of current type
        :return: True if equal, False otherwise
        """
        assert isinstance(other, self.__class__)
        return self.serialize() == other.serialize()

    def serialize(self, as_json=False):
        """
        Builds a dictionary with current block elements. It's a recursive function that serializes
        all elements in block
        :param as_json: If True, provides a json representation of the dictionary with the block elements.
        :return: A dictionary with block elements
        """
        for slot in getattr(self.__class__, '__required_slots__'):
            if not hasattr(self, slot):
                raise AttributeError(f'Missing required slot [{slot}]')

        # mutually exclusive are defined, at least one should exists
        _slot_tuple = getattr(self.__class__, '__mutually_exclusive_slots__')
        if _slot_tuple:
            assert (hasattr(self, _slot_tuple[0]) and not hasattr(self, _slot_tuple[1])) or \
                   (hasattr(self, _slot_tuple[1]) and not hasattr(self, _slot_tuple[0])), \
                f'At least one of this slots must be defined: {_slot_tuple}, but not both'

        # check block spec
        self._validation()

        _dict = dict()

        # check if __type__ exists and add it first
        _type = getattr(self.__class__, '__type__')
        if _type:
            _dict['type'] = _type

        # walk all slots in hierarchy, not only the ones of current class
        for slot in getattr(self, '__all_slots__'):
            if not hasattr(self, slot):
                continue

            slot_value = getattr(self, slot)

            # if it's another block, serialize it and add it to dict
            if isinstance(slot_value, AbstractBlock) or hasattr(slot_value, 'serialize'):
                _dict[slot.lstrip('_')] = slot_value.serialize()
            # if it's a list, we must serialize each element of the list, and then add the list to the dict
            elif isinstance(slot_value, list):
                list_dict = []
                for elem in slot_value:
                    # if a list element is an AbstractBlock, serialize it
                    if isinstance(elem, AbstractBlock):
                        list_dict.append(elem.serialize())
                    else:
                        list_dict.append(elem)
                _dict[slot.lstrip('_')] = list_dict
            # simple values are added directly
            else:
                _dict[slot.lstrip('_')] = getattr(self, slot)

        # dump the serialized dict as json if True
        if as_json:
            return json.dumps(_dict)
        else:
            return _dict

    @classmethod
    def deserialize(cls, _dict, from_json=False):
        """
        Deserializes a slack block, building the instance that represents it. The function
        invokes BlocksFactory.of method recursively when needed
        :param _dict: The block instance as a dictionary
        :param from_json: If True, it loads dictionary first from supplied json string
        :return: An instance of a Slack block
        """
        if from_json:
            assert isinstance(_dict, str), '_dict should be a json representation as a string'
            return cls.deserialize(json.loads(_dict))

        # make sure all required slots are supplied in dictionary
        for slot in getattr(cls, '__required_slots__'):
            assert slot.lstrip('_') in _dict.keys(), f'Missing require field: {slot}'

        # now, check mutually exclusive slots, since they one of them is required too
        slot_tuple = getattr(cls, '__mutually_exclusive_slots__')
        dict_keys = _dict.keys()
        if slot_tuple:
            assert slot_tuple[0].lstrip('_') in dict_keys or slot_tuple[1].lstrip('_') in dict_keys, \
                f'A least one of these two fields is required {slot_tuple}'

        instance = cls()

        # check all slots in inheritance chain (defined by __all_slots__)
        for field, value in _dict.items():
            slot = f'_{field}'

            # skip type
            if slot == '_type':
                continue
            assert slot in getattr(cls, '__all_slots__'), f'unknown supplied slot {slot}'

            # in case it's a dictionary, check if it's a known AbstractBlock classname and build the block using
            # the factory
            if isinstance(value, dict) and BlocksFactory.get_block_class(value):
                setattr(instance, slot, BlocksFactory.of(value))
            # in case it's a list, make the same former check for each list's element
            elif isinstance(value, list):
                list_block = []
                for elem in value:
                    if isinstance(elem, dict) and BlocksFactory.get_block_class(elem):
                        list_block.append(BlocksFactory.of(elem))
                    else:
                        list_block.append(elem)
                setattr(instance, slot, list_block)
            else:
                # any regular value is added directly
                setattr(instance, slot, value)
        return instance

    @abc.abstractmethod
    def _validation(self):
        """
        This method checks if supplied arguments meets required block specification
        :return: An AttributeError is thrown if something is wrong
        """
        raise NotImplementedError()


class AbstractBuilder:
    """
    Abstract class that represents a builder of am AbstractBlock. Any builder in an AbstractBlock must
    inherit from it. It allows the "chain-navigation" of the Block using the builder pattern, allowing
    to step back to uppper builder when all settings in current builder are donde.
    """
    __metaclass__ = abc.ABCMeta

    # Type of object that this builder will instantiate
    __obj__ = None

    def __new__(cls, *args, **kwargs):
        if not getattr(cls, '__obj__'):
            raise AttributeError('Missing required class attribute __obj__')
        elif isinstance(cls.__obj__, str):
            # the first time we load the class, then next times we only need to instantiate it
            cls.__obj__ = getattr(importlib.import_module(cls.__module__), getattr(cls, '__obj__'))
        return super().__new__(cls)

    def __init__(self, _parent=None):
        # helper to return current builder or the supplied one. Needed to navigate through builders
        self._parent = _parent or self
        self._obj = self.__obj__()

    def up(self):
        """
        Provides the builder being used in attribute _parent, which by default is self
        :return: The builder represented by attribute _parent
        """
        return self._parent

    def build(self):
        """
        Returns the instance of the object in any moment
        :return: The instance created by the builder, which type is defined by __obj__
        """
        return self._obj


class AbstractText(AbstractBlock):
    """
    Represents any Text block in Slack, and contains common functionality to both
    implementations, plain:text and mrkdwn
    """
    __slots__ = ('_text',)
    __metaclass__ = abc.ABCMeta

    __required_slots__ = ('_text',)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _validation(self):
        return

    class Builder(AbstractBuilder):
        """
        Common Builder for text fields
        """

        def text(self, text):
            """
            Set's the value of the text block
            :param text: The value that contains current Text element
            :return: The current builder
            """
            setattr(self._obj, '_text', text)
            return self


class PlainText(AbstractText):
    """
    Class that represents a slack's plain_text block
    """
    # Indicates whether emojis in a text field should be escaped into the colon emoji format.
    # -- only useful with plain_text
    __slots__ = ('_emoji',)

    __type__ = 'plain_text'

    def __init__(self, **kwargs):
        kwargs['_emoji'] = kwargs.get('_emoji', False)
        super().__init__(**kwargs)

    class Builder(AbstractText.Builder):
        """
        Builder for PlainText object. Extends AbstractText builder with new methods
        """
        __obj__ = 'PlainText'

        def emoji_(self, boolean):
            """
            Indicates whether emojis in a text field should be escaped into the colon emoji format.
            :param boolean: boolean value to be set
            :return: Current PlainText builder
            """
            setattr(self._obj, '_emoji', boolean)
            return self


class MarkDown(AbstractText):
    """
    Class that represents a slack's mrkdwn block
    """

    # When set to false (as is default) URLs will be auto-converted into links, conversation names will be
    # link-ified, and certain mentions will be automatically parsed.
    # Using a value of true will skip any preprocessing of this nature, although you can still include manual
    # parsing strings.
    # only useful for Markdown
    __slots__ = ('_verbatim',)

    __type__ = 'mrkdwn'

    def __init__(self, **kwargs):
        kwargs['_verbatim'] = kwargs.get('_verbatim', False)
        super().__init__(**kwargs)

    class Builder(AbstractText.Builder):
        """
        Builder for MarkDown object. Extends AbstractText builder with new methods
        """
        __obj__ = 'MarkDown'

        def verbatim_(self, boolean):
            """
            When set to false (as is default) URLs will be auto-converted into links, conversation names
            will be link-ified, and certain mentions will be automatically parsed. Using a value of true will
             skip any preprocessing of this nature, although you can still include manual parsing strings.
            :param boolean:  boolean value to be set
            :return: Current MarkDown builder
            """
            setattr(self._obj, '_verbatim', boolean)
            return self


class Header(AbstractBlock):
    """
    Class that represents a header block in Slack
    """
    __slots__ = ('_text', '_block_id')

    __type__ = 'header'
    __required_slots__ = ('_text',)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _validation(self):
        if hasattr(self, '_text'):
            assert len(getattr(getattr(self, '_text'), '_text')) <= 3000, 'Max number of chars is 3000 for header text'

        if hasattr(self, '_block_id'):
            assert len(getattr(self, '_block_id')) <= 255, 'Max number of chars is 255 for header block_id'

    class Builder(AbstractBuilder):

        __obj__ = 'Header'

        def text(self, txt):
            builder = PlainText.Builder().text(txt)
            setattr(self._obj, '_text', builder.build())
            return self

        def block_id_(self, block_id):
            setattr(self._obj, '_block_id', block_id)
            return self


class Image(AbstractBlock):
    """
    An element to insert an image as part of a larger block of content.
    """
    __slots__ = ('_image_url', '_alt_text')

    __type__ = 'image'
    __required_slots__ = ('_image_url', '_alt_text')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _validation(self):
        return

    class Builder(AbstractBuilder):
        __obj__ = 'Image'

        def image_url(self, image_url):
            """
            The URL of the image to be displayed.
            :param image_url: An url as a string
            :return: Image's builder
            """
            setattr(self._obj, '_image_url', image_url)
            return self

        def alt_text(self, alt_text):
            """
            The text to be used as a a plain-text summary of the image. This should not contain any markup.
            :param alt_text: The string to use as an alternative description
            :return: Image's builder
            """
            setattr(self._obj, '_alt_text', alt_text)
            return self


# -- composed objects


class Confirmation(AbstractBlock):
    """
    An object that defines a dialog that provides a confirmation step to any interactive element. This dialog
    will ask the user to confirm their action by offering a confirm and deny buttons.
    """
    __slots__ = ('_title', '_text', '_confirm', '_deny', '_style')

    __required_slots__ = ('_title', '_text', '_confirm', '_deny')

    STYLE_PRIMARY = 'primary'
    STYLE_DANGER = 'danger'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _validation(self):
        for att in ('_title', '_confirm', '_deny'):
            if hasattr(self, att):
                assert isinstance(getattr(self, att), PlainText), f'{att} must be an instance of PlainText'

        if hasattr(self, '_text'):
            assert isinstance(getattr(self, '_text'), MarkDown), 'text must be an instance of MarkDown'

    class Builder(AbstractBuilder):

        __obj__ = 'Confirmation'

        def title(self, title):
            """
            Confirmation dialog title. Maximum length for this field is 100 characters.
            :param title:  Text to use in  plain_text-only object
            :return: Confirmation's builder
            """
            builder = PlainText.Builder().text(title)
            setattr(self._obj, '_title', builder.build())
            return self

        def confirm(self, confirm):
            """
            The content of the plain_text-only text object that defines the text of the button
            that confirms the action. Maximum length for the text in this field is 30 characters.
            :param confirm: The text to use in plain_text object
            :return: Confirmation's builder
            """
            builder = PlainText.Builder().text(confirm)
            setattr(self._obj, '_confirm', builder.build())
            return self

        def deny(self, deny):
            """
            The text for the plain_text-only text object that defines the text of the button that cancels the action.
            Maximum length for the text in this field is 30 characters.
            :param deny: The text for the plain_text object
            :return: Confirmation's builder
            """
            builder = PlainText.Builder().text(deny)
            setattr(self._obj, '_deny', builder.build())
            return self

        def text(self, text, verbatim=False):
            """
            A text object that defines the explanatory text that appears in the confirm dialog. 
            Maximum length for the text in this field is 300 characters.
            :param: Text that will be used to create a MarkDown object
            :return: Confirmation's builder
            """
            builder = MarkDown.Builder().verbatim_(verbatim).text(text)
            setattr(self._obj, '_text', builder.build())
            return self

        def style_(self, style):
            """
            Defines the color scheme applied to the confirm button. A value of "danger" will display the button with
            a red background on desktop, or red text on mobile. A value of "primary" will display the button with a
            green background on desktop, or blue text on mobile. If this field is not provided, the default value
            will be primary.
            :param style: One of "primary" or "danger"
            :return: Confirmation's builder
            """
            setattr(self._obj, '_style', style)
            return self


class Button(AbstractBlock):
    """
    Represent's the interactive component, Button.
    """
    __slots__ = ('_text', '_action_id', '_url', '_value', '_style', '_confirm')

    __type__ = 'button'
    __required_slots__ = ('_text', '_action_id')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _validation(self):
        if hasattr(self, '_text'):
            assert isinstance(getattr(self, '_text'), PlainText), 'text must be an instance of PlainText'
        return

    class Builder(AbstractBuilder):
        __obj__ = 'Button'

        def action_id(self, action_id):
            """
            An identifier for this action. You can use this when you receive an interaction payload to identify
            the source of the action. It MUST BE unique among all other action_ids used elsewhere in the slackviews.
            Maximum length for this field is 255 characters.
            :param action_id: A valid string
            :return: Button's builder
            """
            setattr(self._obj, '_action_id', action_id)
            return self

        def text(self, text):
            """
            A string for the plain_text object that defines the button's text.
            Maximum length for the text in this field is 75 characters.
            :param text: A valid string
            :return: Button's builder
            """
            builder = PlainText.Builder().text(text)
            setattr(self._obj, '_text', builder.build())
            return self

        def url_(self, url):
            """
            A URL to load in the user's browser when the button is clicked.
            Maximum length for this field is 3000 characters. If you're using url, you'll still receive an
            interaction payload and will need to send an acknowledgement response.
            :param url: A valid url as a string
            :return: Button's builder
            """
            setattr(self._obj, '_url', url)
            return self

        def value_(self, value):
            """
            The value to send along with the interaction payload.
            Maximum length for this field is 2000 characters.
            :param value: Any value needed to be sent with interaction payload
            :return: Button's builder
            """
            setattr(self._obj, '_value', value)
            return self

        def style_(self, style):
            """
            Decorates buttons with alternative visual color schemes. Use this option with restraint.

            Options:

            "primary" gives buttons a green outline and text, primary should only be used for one button within a set.
            "danger" gives buttons a red outline and text, and should be used when the action is destructive.

            If not specified, default is used, with means default font color

            :param style: One of "primary" or "danger"
            :return: Button's builder
            """
            setattr(self._obj, '_style', style)
            return self

        def Confirm_(self):
            """
            Provides a Confirmation builder object to help creating an optional confirmation dialog after
            the button is clicked.
            :return: Confirmation's builder
            """
            builder = Confirmation.Builder(_parent=self)
            setattr(self._obj, '_confirm', builder.build())
            return builder


class Option(AbstractBlock):
    """
    An object that represents a single selectable item in a select menu, multi-select menu, checkbox group,
    radio button group, or overflow menu.
    """
    __slots__ = ('_text', '_value', '_description', '_url')

    __required_slots__ = ('_text', '_value')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _validation(self):
        if hasattr(self, '_text'):
            assert isinstance(getattr(self, '_text'), PlainText), 'text must be an instance of PlainText'

        if hasattr(self, '_value'):
            assert isinstance(getattr(self, '_value'), str), 'value must be a string'

        if hasattr(self, '_description'):
            assert isinstance(getattr(self, '_description'), PlainText), 'description must be an instance of PlainText'

    class Builder(AbstractBuilder):

        __obj__ = 'Option'

        def text(self, text):
            """
            A text object that defines the text shown in the option on the menu. Overflow, select, and multi-select
            menus can only use plain_text objects, while radio buttons and checkboxes can use mrkdwn text objects.
            Maximum length for the text in this field is 75 characters.

            In this release, no radio buttons or checkboxes are supplied, so only plain_text will be used
            :param text:  The text to show in an plain_text object
            :return: Option's builder
            """
            builder = PlainText.Builder().text(text)
            setattr(self._obj, '_text', builder.build())
            return self

        def value(self, value):
            """
            The string value that will be passed to your slackviews when this option is chosen. Maximum length for
            this field is 75 characters.
            :param value: A valid string. It MUST be a string, no integers, etc
            :return: Option's builder
            """
            setattr(self._obj, '_value', value)
            return self

        def description_(self, description):
            """
            The text for the plain_text only text object that defines a line of descriptive text shown below the
            text field beside the radio button. Maximum length for the text object within this field is 75 characters.
            :param description: A valid string
            :return: Option's builder
            """
            builder = PlainText.Builder().text(description)
            setattr(self._obj, '_description', builder.build())
            return self

        def url_(self, url):
            """
            A URL to load in the user's browser when the option is clicked. The url attribute is only available
            in overflow menus. Maximum length for this field is 3000 characters.
            If you're using url, you'll still receive an interaction payload and will need to send an acknowledgement
            response.
            :param url: A valid url as a string
            :return: Option's builder
            """
            setattr(self._obj, '_url', url)
            return self


class OptionGroup(AbstractBlock):
    """
    Provides a way to group options in a select menu or multi-select menu.
    """
    __slots__ = ('_label', '_options')

    __required_slots__ = __slots__

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _validation(self):
        if hasattr(self, '_label'):
            assert isinstance(getattr(self, '_label'), PlainText), 'label must be an instance of PlainText'

        if hasattr(self, '_options'):
            options = getattr(self, '_options')
            assert isinstance(options, list), 'options must be an array'
            for opt in options:
                assert isinstance(opt, Option), 'options must be an array of Option instances'

    class Builder(AbstractBuilder):

        __obj__ = 'OptionGroup'

        def label(self, label):
            """
            The text for the plain_text only text object that defines the label shown above this group of options.
            Maximum length for the text in this field is 75 characters.
            :param label: A valid string
            :return: OptionGroup's builder
            """
            builder = PlainText.Builder().text(label)
            setattr(self._obj, '_label', builder.build())
            return self

        def Option(self):
            """
            An array of option objects that belong to this specific group.
            Maximum of 100 items.
            :return: Option's builder
            """
            if not hasattr(self._obj, '_options'):
                setattr(self._obj, '_options', [])

            opts = getattr(self._obj, '_options')
            builder = Option.Builder(_parent=self)
            opts.append(builder.build())
            return builder


class SelectMenu(AbstractBlock):
    """
    A select menu, just as with a standard HTML <select> tag, creates a drop down menu with a list of options for 
    a user to choose. The select menu also includes type-ahead functionality, where a user can type a part or all 
    of an option string to filter the list.
    """
    __slots__ = ('_placeholder', '_action_id', '_options', '_option_groups', '_initial_option', '_confirm')

    __type__ = 'static_select'
    __required_slots__ = ('_placeholder', '_action_id')
    __mutually_exclusive_slots__ = ('_options', '_option_groups')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _validation(self):
        assert not (hasattr(self, '_options') and hasattr(self, '_option_groups')), 'options and option_groups are ' \
                                                                                    'mutually exclusive'
        if hasattr(self, '_placeholder'):
            assert isinstance(getattr(self, '_placeholder'), PlainText), 'placeholder must be an instance of PlainText'

        if hasattr(self, '_options'):
            options = getattr(self, '_options')
            assert isinstance(options, list), 'options must be an array'
            for opt in options:
                assert isinstance(opt, Option), 'options must be an array of Option instances'
        elif hasattr(self, '_option_groups'):
            option_groups = getattr(self, '_option_groups')
            assert isinstance(option_groups, list), 'option_groups must be an array'
            for group in option_groups:
                assert isinstance(group, OptionGroup), 'option_groups must be an array of OptionGroup instances'

        if hasattr(self, '_initial_option'):
            assert isinstance(getattr(self, '_initial_option'), Option), 'initial_option must be an instance of Option'

        if hasattr(self, '_confirm'):
            assert isinstance(getattr(self, '_confirm'), Confirmation), 'confirm must be an instance of Confirmation'

    def set_default(self, text_option):
        """
        Sets default value in the menu. It's possible to supply, or the text that represents the underlying value
        in the menu, or the  value itself
        :param text_option: The value of the default option, or the text representing such value in the menu
        """
        assert hasattr(self, '_options') or hasattr(self, '_option_groups'), \
            'Can not set a default option without options or options_groups first'
        assert isinstance(text_option, str), 'supplied value must be the text of desired initial option'
        _opt = self.__get_option(text_option)
        if _opt:
            setattr(self, '_initial_option', _opt)
        else:
            raise AttributeError(f'Option [{text_option}] does not exists')

    def get_default(self):
        """
        Provides the default option, if any, as a tuple
        :return:  The default option if any, as a tuple (text, value)
        """
        if hasattr(self, '_initial_option'):
            return getattr(self, '_initial_option')
        else:
            return None

    def has_option(self, text_option):
        """
        Checks if the text supplied is already included in the array of options
        :param text_option: The option text to check if exists in array
        :return: True if exists, False otherwise
        """
        return bool(self.__get_option(text_option))

    def __get_option(self, text_option):
        """
        Provides the option that matches supplied text in the current array of options, either in
        text_ or value_ fields.
        :param text_option: The option text to check if exists in array
        :return: The option with supplied text, None if it does not exists
        """
        assert text_option, 'Supplied text_option can not be empty'

        # look for option in _options, if exists
        if hasattr(self, '_options'):
            for _opt in getattr(self, '_options'):
                if getattr(getattr(_opt, '_text'), '_text') == text_option or \
                        getattr(_opt, '_value') == text_option:
                    return _opt

        # now, look for default option in option_groups
        if hasattr(self, '_option_groups'):
            for _opt_group in getattr(self, '_option_groups'):
                for _opt in getattr(_opt_group, '_options'):
                    if getattr(getattr(_opt, '_text'), '_text') == text_option or \
                            getattr(_opt, '_value') == text_option:
                        return _opt
        return None

    class Builder(AbstractBuilder):

        __obj__ = 'SelectMenu'

        def action_id(self, action_id):
            """
            An identifier for the action triggered when a menu option is selected. You can use this when you receive
            an interaction payload to identify the source of the action. Should be unique among all other action_ids
            used elsewhere by your slackviews. Maximum length for this field is 255 characters.
            :param action_id: A string to used as action id
            :return: SelectMenu's builder
            """
            setattr(self._obj, '_action_id', action_id)
            return self

        def placeholder(self, placeholder):
            """
            A text for the plain_text object that defines the placeholder text shown on the menu.
            Maximum length for the text in this field is 150 characters.
            :param placeholder: The text to use as placeholder in the menu. i.e. Choose one:, Select: etc...
            :return: SelectMenu's builder
            """
            builder = PlainText.Builder().text(placeholder)
            setattr(self._obj, '_placeholder', builder.build())
            return self

        def Option__(self):
            """
            In case this method is invoked, a new Option element is created an added to the "options" attribute
            in the selectmenu. Maximum number of options is 100. If option_groups is specified,
             this field should not be, that's why it's included in mutually exclusive tuple
            :return: Option's builder
            """
            if not hasattr(self._obj, '_options'):
                setattr(self._obj, '_options', [])

            opts = getattr(self._obj, '_options')
            builder = Option.Builder(_parent=self)
            opts.append(builder.build())
            return builder

        def OptionGroup__(self):
            """
            In case this method is invoked, a new OptionGroup element is created an added to the "option_groups"
            attribute in the selectmenu. Maximum number of option groups is 100. If options is specified,
            this field should not be, that's why it's included in mutually exclusive tuple
            :return: OptionGroup's builder
            """
            if not hasattr(self._obj, '_option_groups'):
                setattr(self._obj, '_option_groups', [])

            opts = getattr(self._obj, '_option_groups')
            builder = OptionGroup.Builder(_parent=self)
            opts.append(builder.build())
            return builder

        def initial_option_(self, text_option):
            """
            A single option that exactly matches one of the options within options or option_groups.
            This option will be selected when the menu initially loads.
            :param text_option: A value, or the text representing such value, of one of the existing options
            in options or option_groups
            :return: SelectMenu's builder
            """
            # initial option must be an exact value of current options, so it should be contained
            if not hasattr(self._obj, '_options') and not hasattr(self._obj, '_option_groups'):
                raise AttributeError('Can not set initial option, without options or option_groups')
            self._obj.set_default(text_option)
            return self

        def Confirm_(self):
            """
            A confirm object that defines an optional confirmation dialog that appears after a menu item is selected.
            :return: Confirmation's builder
            """
            builder = Confirmation.Builder(_parent=self)
            setattr(self._obj, '_confirm', builder.build())
            return builder


class MultiSelectMenu(SelectMenu):
    """
    A multi-select menu allows a user to select multiple items from a list of options. Just like regular select menus,
    multi-select menus also include type-ahead functionality, where a user can type a part or all of an option string
    to filter the list
    """
    __slots__ = ('_max_selected_items',)

    # it's needed to initialize all slots again correctly
    __all_slots__ = None

    __type__ = 'multi_static_select'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _validation(self):
        super()._validation()
        if hasattr(self, '_max_selected_items'):
            assert isinstance(getattr(self, '_max_selected_items'), int), 'max_selected_items must be an integer'

    class Builder(SelectMenu.Builder):
        __obj__ = 'MultiSelectMenu'

        def max_selected_items_(self, max_selected_items):
            """
            Specifies the maximum number of items that can be selected in the menu.
            Minimum number is 1.
            :param max_selected_items: Number of items that can be selected
            :return: MultiSelectMenu's builder
            """
            setattr(self._obj, '_max_selected_items', max_selected_items)
            return self


class Overflow(AbstractBlock):
    """
    This is like a cross between a button and a select menu - when a user clicks on this overflow button, they will
    be presented with a list of options to choose from. Unlike the select menu, there is no typeahead field, and
    the button always appears with an ellipsis ("...") rather than customisable text.
    As such, it is usually used if you want a more compact layout than a select menu, or to supply a list of
    less visually important actions after a row of buttons.

    You can also specify simple URL links as overflow menu options, instead of actions.
    """
    __slots__ = ('_action_id', '_options', '_confirm')

    __type__ = 'overflow'
    __required_slots__ = ('_action_id', '_options')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _validation(self):
        if hasattr(self, '_options'):
            options = getattr(self, '_options')
            assert isinstance(options, list), 'options must be an array'
            assert 2 <= len(options) <= 5, 'No more than 5 options can be used in an overflow, and the minimum is 2'

            for opt in options:
                assert isinstance(opt, Option), 'options must be an array of Option instances'

        if hasattr(self, '_confirm'):
            assert isinstance(getattr(self, '_confirm'), Confirmation), 'confirm must be an instance of Confirmation'

    class Builder(AbstractBuilder):

        __obj__ = 'Overflow'

        def action_id(self, action_id):
            """
            An identifier for the action triggered when a menu option is selected. You can use this when you
            receive an interaction payload to identify the source of the action. Should be unique among all
            other action_ids used elsewhere by your slackviews. Maximum length for this field is 255 characters.
            :param action_id: A string to be used as axtion id
            :return: Overflow's builder
            """
            setattr(self._obj, '_action_id', action_id)
            return self

        def Option(self):
            """
            In case this method is invoked, a new Option element is created an added to the "options" attribute
            in the overflow. Maximum number of options is 5, minimum is 2
            :return: Option's builder
            """
            if not hasattr(self._obj, '_options'):
                setattr(self._obj, '_options', [])

            opts = getattr(self._obj, '_options')
            builder = Option.Builder(_parent=self)
            opts.append(builder.build())
            return builder

        def Confirm_(self):
            """
            A confirm object that defines an optional confirmation dialog that appears after an item is selected.
            :return: Confirmation's builder
            """
            builder = Confirmation.Builder(_parent=self)
            setattr(self._obj, '_confirm', builder.build())
            return builder


class PlainTextInput(AbstractBlock):
    """
    A plain-text input, it creates a field where a user can enter freeform data.
    It can appear as a single-line field or a larger textarea using the multiline flag.
    PlainTextInput elements are currently only available in modals.
    """
    __slots__ = ('_action_id', '_placeholder', '_initial_value', '_multiline', '_min_length', '_max_length')

    __type__ = 'plain_text_input'
    __required_slots__ = ('_action_id',)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _validation(self):
        if hasattr(self, '_placeholder'):
            assert isinstance(getattr(self, '_placeholder'), PlainText), 'placeholder must be an instance of PlainText'

        if hasattr(self, '_multiline'):
            assert isinstance(getattr(self, '_multiline'), bool), '_multiline must be a boolean'

        for att in ('_min_length', '_max_length'):
            if hasattr(self, att):
                assert isinstance(getattr(self, att), int), f'{att} must be an integer'

    class Builder(AbstractBuilder):
        __obj__ = 'PlainTextInput'

        def action_id(self, action_id):
            """
            An identifier for the input value when the parent modal is submitted. You can use this when you receiv
            a view_submission payload to identify the value of the input element. Should be unique among all other
            action_ids used elsewhere by your slackviews. Maximum length for this field is 255 characters.
            :param action_id: A string to be used as action id
            :return: PlainTextInput's builder
            """
            setattr(self._obj, '_action_id', action_id)
            return self

        def initial_value_(self, initial_value):
            """
            The initial value in the plain-text input when it is loaded.
            :param initial_value: A string
            :return: PlainTextInput's builder
            """
            setattr(self._obj, '_initial_value', initial_value)
            return self

        def min_length_(self, min_length):
            """
            The minimum length of input that the user must provide. If the user provides less, they will receive
            an error. Maximum value is 3000
            :param min_length: An integer representing min input length
            :return: PlainTextInput's builder
            """
            setattr(self._obj, '_min_length', min_length)
            return self

        def max_length_(self, max_length):
            """
            The maximum length of input that the user can provide. If the user provides more, they will receive
            an error.
            :param max_length: An integer representing max input length
            :return: PlainTextInput's builder
            """
            setattr(self._obj, '_max_length', max_length)
            return self

        def multiline_(self, boolean):
            """
            Indicates whether the input will be a single line (false) or a larger textarea (true).
            Defaults to false.
            :param boolean: A boolean to use multi-line in input text.
            :return: PlainTextInput's builder
            """
            setattr(self._obj, '_multiline', boolean)
            return self

        def placeholder_(self, placeholder):
            """
            A text to user in plain_text object that defines the placeholder text shown in the plain-text input.
            Maximum length for the text in this field is 150 characters.
            :param placeholder: A string for the placeholder
            :return: PlainTextInput's builder
            """
            builder = PlainText.Builder().text(placeholder)
            setattr(self._obj, '_placeholder', builder.build())
            return self


# ################# #
# -- block layouts  #
# ################# #

class Section(AbstractBlock):
    """
    A section can be used as a simple text block, in combination with text fields, or side-by-side with any of
    the available block elements.
    """
    __slots__ = ('_text', '_block_id', '_fields', '_accessory')

    __type__ = 'section'
    __mutually_exclusive_slots__ = '_text', '_fields'

    _ALLOWED_ACCESSORIES = [Button, Image, Overflow, PlainTextInput, SelectMenu, MultiSelectMenu]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _validation(self):

        if hasattr(self, '_text'):
            assert isinstance(getattr(self, '_text'), MarkDown), 'text must be an instance of MarkDown'

        if hasattr(self, '_fields'):
            fields = getattr(self, '_fields')
            assert isinstance(fields, list) and len(fields) < 11, 'fields must be an array of max length 10'
            for field in fields:
                assert isinstance(field, MarkDown), 'All elements of fields must be an instance of MarkDown'

        if hasattr(self, '_accessory'):
            assert type(getattr(self, '_accessory')) in Section._ALLOWED_ACCESSORIES, \
                f'accessory must be one of {Section._ALLOWED_ACCESSORIES}'

    class Builder(AbstractBuilder):

        __obj__ = 'Section'

        def text__(self, text, verbatim=False):
            """
            The text for the block, in the form of a text object. Maximum length for the text in this field is
            3000 characters. This field is not required if a valid array of fields objects is provided instead.
            :param text: the content of the text object
            :param verbatim: Use verbatim mode in text object
            :return: Section's builder
            """
            builder = MarkDown.Builder().verbatim_(verbatim).text(text)
            setattr(self._obj, '_text', builder.build())
            return self

        def block_id_(self, block_id):
            """
            A string acting as a unique identifier for a block. If not specified, one will be generated.
            You can use this block_id when you receive an interaction payload to identify the source of the action.
            Maximum length for this field is 255 characters. Block_id should be unique for each message and each
            iteration of a message. If a message is updated, use a new block_id.
            :param block_id: A string to use as block_id
            :return: Section's builder
            """
            setattr(self._obj, '_block_id', block_id)
            return self

        def field__(self, text, verbatim=False):
            """
            Creates an a new Text instance, and add it to the array of text objects. Any text objects included
            with fields will be rendered in a compact format that allows for 2 columns of side-by-side text.
             Maximum number of items is 10. Maximum length for the ext in each item is 2000 characters.
            :param text: The text for the Text instance
            :param verbatim: Enable verbatim in MarkDown text
            :return: Section's buildr
            """
            if not hasattr(self._obj, '_fields'):
                setattr(self._obj, '_fields', [])
            fields = getattr(self._obj, '_fields')

            # max is 10 elements
            if len(fields) == 10:
                raise AttributeError('max number of fields elements is 10, can not add another one')

            builder = MarkDown.Builder().verbatim_(verbatim).text(text)
            fields.append(builder.build())
            return self

        def accessory_(self):
            """
            Provides an inner class instance with a builder instance of each one of the available element objects.
            Namely: Button, Image, MultiSelectMenu,Overflow, PlainTextInput, SelectMenu

            :return:  A class with each builder of available element objects
            """

            class Accessory:
                def __init__(self, _parent):
                    self._parent = _parent

                def Button(self):
                    """
                    An instance of Button builder
                    :return: Button's builder
                    """
                    _builder = Button.Builder(_parent=self._parent)
                    setattr(getattr(self._parent, '_obj'), '_accessory', _builder.build())
                    return _builder

                def Image(self):
                    """
                    An instance of Image builder
                    :return: Image's builder
                    """
                    _builder = Image.Builder(_parent=self._parent)
                    setattr(getattr(self._parent, '_obj'), '_accessory', _builder.build())
                    return _builder

                def MultiSelectMenu(self):
                    """
                    An instance of MultiSelectMenu builder
                    :return: MultiSelectMenu's builder
                    """
                    _builder = MultiSelectMenu.Builder(_parent=self._parent)
                    setattr(getattr(self._parent, '_obj'), '_accessory', _builder.build())
                    return _builder

                def Overflow(self):
                    """
                    An instance of Overflow builder
                    :return: Overflow's builder
                    """
                    _builder = Overflow.Builder(_parent=self._parent)
                    setattr(getattr(self._parent, '_obj'), '_accessory', _builder.build())
                    return _builder

                def PlainTextInput(self):
                    """
                    An instance of PlainTextInput builder
                    :return: PlainTextInput's builder
                    """
                    _builder = PlainTextInput.Builder(_parent=self._parent)
                    setattr(getattr(self._parent, '_obj'), '_accessory', _builder.build())
                    return _builder

                def SelectMenu(self):
                    """
                    An instance of SelectMenu builder
                    :return: SelectMenu's builder
                    """
                    _builder = SelectMenu.Builder(_parent=self._parent)
                    setattr(getattr(self._parent, '_obj'), '_accessory', _builder.build())
                    return _builder

            return Accessory(_parent=self)


class Divider(AbstractBlock):
    """
    A block divider. Basically adds a horizontal line that can be use to separate blocks
    """
    __slots__ = '_block_id',

    __type__ = 'divider'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _validation(self):
        return

    class Builder(AbstractBuilder):
        __obj__ = 'Divider'

        def block_id_(self, block_id):
            setattr(self._obj, '_block_id', block_id)
            return self


class Actions(AbstractBlock):
    """
    A block that is used to hold interactive elements.
    """

    __slots__ = ('_elements', '_block_id')

    __type__ = 'actions'
    __required_slots__ = ('_elements',)

    _ALLOWED_ELEMENTS = Button, SelectMenu, Overflow

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _validation(self):
        if hasattr(self, '_elements'):
            elements = getattr(self, '_elements')
            assert isinstance(elements, list), 'elements must be an array'
            assert len(elements) < 6, 'maximum of 5 elements allowed'
            for element in elements:
                assert type(element) in Actions._ALLOWED_ELEMENTS, f'all elements must be an instace of' \
                                                                   f' {Actions._ALLOWED_ELEMENTS}'

    class Builder(AbstractBuilder):

        __obj__ = 'Actions'

        def block_id_(self, block_id):
            """
            A string acting as a unique identifier for this block. If not specified, a block_id will be generated.
            You can use this block_id when you receive an interaction payload to identify the source of the action.
            Maximum length for this field is 255 characters. block_id should be unique for each message and each iteration of a message. If a message is updated, use a new block_id.
            :param block_id: A valid string representing the block id
            :return: Action's builder
            """
            setattr(self._obj, '_block_id', block_id)
            return self

        def element(self):
            """
            If no "elements" array is found, a new one is created, and an instance of an internal class with all
            builders from allowed elements is shown. The attribute "elements" holds an array of interactive
            element objects - buttons, select menus, overflow menus, or date pickers (not implement right now)
            There is a maximum of 5 elements in each action block.
            :return: An instance of a class with all builders of allowed elements (Button, Overflow and SelectMenu)
            """

            if not hasattr(self._obj, '_elements'):
                setattr(self._obj, '_elements', [])

            if len(getattr(self._obj, '_elements')) == 5:
                raise AttributeError('elements already has max number of allowed elements, [5]')

            class Element:
                def __init__(self, _parent):
                    self._parent = _parent
                    self._elements = getattr(getattr(_parent, '_obj'), '_elements')

                def Button(self):
                    """
                    Provides an instance of Button builder
                    :return: Button's builder
                    """
                    _builder = Button.Builder(_parent=self._parent)
                    self._elements.append(_builder.build())
                    return _builder

                def Overflow(self):
                    """
                    Provides an instance of Overflow builder
                    :return: Overflow's builder
                    """
                    _builder = Overflow.Builder(_parent=self._parent)
                    self._elements.append(_builder.build())
                    return _builder

                def SelectMenu(self):
                    """
                    Provides an instance of SelectMenu builder
                    :return: SelectMenu's builder
                    """
                    _builder = SelectMenu.Builder(_parent=self._parent)
                    self._elements.append(_builder.build())
                    return _builder

            return Element(_parent=self)


class Context(AbstractBlock):
    """
    Displays message context, which can include both images and text.
    The size (images, fonts etc) of this block is smaller than other Blocks
    """
    __slots__ = ('_elements', '_block_id')

    __type__ = 'context'
    __required_slots__ = ('_elements',)

    _ALLOWED_ELEMENTS = Image, MarkDown

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _validation(self):
        if hasattr(self, '_elements'):
            elements = getattr(self, '_elements')
            assert isinstance(elements, list), 'elements must be an array'
            assert len(elements) < 6, 'maximum of 5 elements allowed'
            for element in elements:
                assert type(element) in Context._ALLOWED_ELEMENTS, f'all elements must be an instace of' \
                                                                   f' {Context._ALLOWED_ELEMENTS}'

    class Builder(AbstractBuilder):

        __obj__ = 'Context'

        def block_id_(self, block_id):
            """
            A string acting as a unique identifier for this block. If not specified, one will be generated.
            Maximum length for this field is 255 characters. block_id should be unique for each message
            and each iteration of a message. If a message is updated, use a new block_id.
            :param block_id: A string representing the block id
            :return: Context's builder
            """
            setattr(self._obj, '_block_id', block_id)
            return self

        def element(self):
            if not hasattr(self._obj, '_elements'):
                setattr(self._obj, '_elements', [])

            if len(getattr(self._obj, '_elements')) == 5:
                raise AttributeError('elements already has max number of allowed elements, [5]')

            class Element:
                def __init__(self, _parent):
                    self._parent = _parent
                    self._elements = getattr(getattr(_parent, '_obj'), '_elements')

                def Image(self):
                    """
                    Provides an instance of Image's builder
                    :return: Image's builder
                    """
                    _builder = Image.Builder(_parent=self._parent)
                    self._elements.append(_builder.build())
                    return _builder

                def Text(self):
                    """
                    Provides an instance of Markdown's builder (it could be Plain-Text or Markdown, but currently
                    decided to use MarkDown only.
                    :return: Markdown's builder
                    """
                    _builder = MarkDown.Builder(_parent=self._parent)
                    self._elements.append(_builder.build())
                    return _builder

            return Element(_parent=self)


class Input(AbstractBlock):
    """
    A block that collects information from users - it can hold a plain-text input element, a select menu element,
    a multi-select menu element, or a datepicker (later one currently not implemented)
    """
    __slots__ = ('_label', '_element', '_block_id', '_hint', '_optional')

    __type__ = 'input'
    __required_slots__ = ('_label', '_element')

    _ALLOWED_ELEMENTS = PlainTextInput, SelectMenu, MultiSelectMenu

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _validation(self):
        for att in ('_label', '_hint'):
            if hasattr(self, att):
                assert isinstance(getattr(self, att), PlainText), f'{att} must be of type PlainText'

        if hasattr(self, '_optional'):
            assert isinstance(getattr(self, '_optional'), bool), f'_optional must be a boolean'

        if hasattr(self, '_element'):
            assert type(getattr(self, '_element')) in Input._ALLOWED_ELEMENTS, f'element must be an instance of' \
                                                                               f' {Input._ALLOWED_ELEMENTS}'

    class Builder(AbstractBuilder):

        __obj__ = 'Input'

        def label(self, label):
            """
            A label that appears above an input element in the form of a text object as plain_text.
            Maximum length for the text in this field is 2000 characters.
            :param label: A valid string
            :return: Input's builder
            """
            _builder = PlainText.Builder().text(label)
            setattr(self._obj, '_label', _builder.build())
            return self

        def element(self):
            """
            Provides an instance of a class with all builders of allowed elements in an input block
            :return: An instance with all allowed element builders
            """

            class Element:
                def __init__(self, _parent):
                    self._parent = _parent

                def PlainTextInput(self):
                    """
                    An instance of PlainTextInput builder
                    :return: PlainTextInput's builder
                    """
                    _builder = PlainTextInput.Builder(_parent=self._parent)
                    setattr(getattr(self._parent, '_obj'), '_element', _builder.build())
                    return _builder

                def SelectMenu(self):
                    """
                    An instance of SelectMenu builder
                    :return: SelectMenu's builder
                    """
                    _builder = SelectMenu.Builder(_parent=self._parent)
                    setattr(getattr(self._parent, '_obj'), '_element', _builder.build())
                    return _builder

                def MultiSelectMenu(self):
                    """
                    An instance of MultiSelectMenu builder
                    :return: MultiSelectMenu's builder
                    """
                    _builder = MultiSelectMenu.Builder(_parent=self._parent)
                    setattr(getattr(self._parent, '_obj'), '_element', _builder.build())
                    return _builder

            return Element(_parent=self)

        def block_id_(self, block_id):
            """
            A string acting as a unique identifier for a block. If not specified, one will be generated.
            Maximum length for this field is 255 characters. block_id should be unique for each message
            and each iteration of a message. If a message is updated, use a new block_id
            :param block_id: A string representing the block id
            :return: Input's builder
            """
            setattr(self._obj, '_block_id', block_id)
            return self

        def hint_(self, hint):
            """
            An optional hint that appears below an input element in a lighter grey. It's the text of a plain_text
            object. Maximum length for the text in this field is 2000 characters.
            :param hint: A valid string
            :return: Input's builder
            """
            _builder = PlainText.Builder().text(hint)
            setattr(self._obj, '_hint', _builder.build())
            return self

        def optional_(self, boolean):
            """
            A boolean that indicates whether the input element may be empty when a user submits the modal.
            Defaults to false.
            :param boolean: A boolean
            :return: Input's builder
            """
            setattr(self._obj, '_optional', boolean)
            return self


# -- View
class View(AbstractBlock):
    """
    Abstract class that represents a View. There're two types of  views, namely Modals and Hometabs.
    """

    __metaclass__ = abc.ABCMeta
    __slots__ = ('_blocks', '_callback_id', '_clear_on_close', '_close', '_external_id', '_notify_on_close',
                 '_private_metadata', '_submit', '_title')

    # __type__ not declared, so an instance of this class can not be done. It should be declare in child class

    __required_slots__ = ('_title', '_blocks')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _validation(self):
        for att in ('_title', '_close', '_submit'):
            if hasattr(self, att):
                _obj = getattr(self, att)
                assert (isinstance(_obj, PlainText) and len(getattr(_obj, '_text')) <= 24), \
                    f'{att} must be of type PlainText and max lentgh is 24 char'

        if hasattr(self, '_blocks'):
            blocks = getattr(self, '_blocks')
            if isinstance(blocks, BlocksArray):
                num_of_blocks = blocks.num_of_blocks()
                has_input = blocks.has_input_block()
            else:
                assert isinstance(blocks, list), 'blocks field must be, an instance of BlocksArray, ' \
                                                 'or an array of Blocks'
                has_input = False
                for _b in blocks:
                    assert isinstance(_b, AbstractBlock), 'blocks array elements must be instances of AbstractBlock'
                    if isinstance(_b, Input):
                        has_input = True
                num_of_blocks = len(blocks)

            assert num_of_blocks <= 100, 'Max number of blocks in a View is 100'

            if has_input:
                assert getattr(self, '_submit'), 'submit is required when an input block is within supplied blocks'

            if hasattr(self, '_private_metadata'):
                assert len(getattr(self, '_private_metadata')) <= 3000, 'Max length for private_metadata is 3.000 chars'

            if hasattr(self, '_callback_id'):
                assert len(getattr(self, '_callback_id')) <= 255, 'Max length for private_metadata is 255 chars'

    class Builder(AbstractBuilder):

        __obj__ = 'View'

        def title(self, txt):
            """
            The title that appears in the top-left of the modal
            :param txt: The content of the plain-text object
            :return: View's builder
            """
            _builder = PlainText.Builder().text(txt)
            setattr(self._obj, '_title', _builder.build())
            return self

        def Blocks(self):
            """
            Use this to build the array of blocks of the view
            :return: An instance of BlockArray's builder
            """
            _builder = BlocksArray.Builder(_parent=self)
            setattr(self._obj, '_blocks', _builder.build())
            return _builder

        def close_(self, close_txt):
            """
            Text to create a plain_text element that
            defines the text displayed in the close button at
            the bottom-right of the view.
            :param close_txt: The content of the plain-text object
            :return: View's builder
            """
            _builder = PlainText.Builder().text(close_txt)
            setattr(self._obj, '_close', _builder.build())
            return self

        def submit_(self, submit_txt):
            """
            Text to create an optional plain_text element that defines
            the text displayed in the submit button at
            the bottom-right of the view.
            :param submit_txt: The content of the plain-text object
            :return: View's builder
            """
            _builder = PlainText.Builder().text(submit_txt)
            setattr(self._obj, '_submit', _builder.build())
            return self

        def private_metadata_(self, private_metadata):
            """
            An optional string that will be sent to your slackviews in
            view_submission and block_actions events.
            Max length of 3000 characters.
            :param private_metadata: The string representing private metadata
            :return: View's builder
            """
            setattr(self._obj, '_private_metadata', private_metadata)
            return self

        def callback_id_(self, callback_id):
            """
            An identifier to recognize interactions and submissions of
            this particular view. Don't use this to store sensitive
            information (use private_metadata instead). Max length is 255
            :param callback_id: The callback_id as a string
            :return: View's builder
            """
            setattr(self._obj, '_callback_id', callback_id)
            return self

        def clear_on_close_(self, clear_on_close):
            """
            When set to true, clicking on the close button will clear all
            views in a modal and close it. Defaults to false.
            :param clear_on_close: A boolean
            :return: View's builder
            """
            setattr(self._obj, '_clear_on_close', clear_on_close)
            return self

        def notify_on_close_(self, notify_on_close):
            """
            Indicates whether Slack will send your request URL a view_closed
            event when a user clicks the close button. Defaults to false.
            :param notify_on_close: A boolean
            :return: View's builder
            """
            setattr(self._obj, '_notify_on_close', notify_on_close)
            return self

        def external_id_(self, external_id):
            """
             A custom identifier that must be unique for all views on a per-team basis.
            :param external_id: A string representing external id
            :return: View's builder
            """
            setattr(self._obj, '_external_id', external_id)
            return self


class Modal(View):
    """
    Modals provide focused spaces ideal for requesting and collecting data from users, or temporarily
    displaying dynamic and interactive information.
    """
    __slots__ = ('_id', '_team_id', '_state', '_hash', '_previous_view_id', '_root_view_id', '_app_id',
                 '_app_installed_team_id', '_bot_id')

    __type__ = 'modal'

    class Builder(View.Builder):
        __obj__ = 'Modal'


class Home(View):
    """
    The Home tab is a persistent, yet dynamic interface for apps.
    Present each of your users with a unique Home tab just for them, always found in the exact same place.
    """
    __type__ = 'home'

    class Builder(View.Builder):
        __obj__ = 'Home'


# -- Global Block builder and factory

class BlocksArray:
    """
    This class represents the array of blocks being sent to Slack message. It doesn't extend AbstractBlocks because
    actually it's not a block, but a group of blocks in an array. So just acts as a wrapper of an array with a
    dictionary of blocks
    """
    __slots__ = ('_blocks',)

    def __init__(self, **kwargs):
        setattr(self, '_blocks', kwargs.get('_blocks', []))

    def serialize(self, as_json=False):
        """
        Returns the array of blocks's dictionary. It's an array,  not a dictionary with key "blocks". The array is ready
        to be serialized in Slack
        :return: An array of  dicts with current content blocks
        """
        array_ = [blk.serialize() for blk in getattr(self, '_blocks')]
        if as_json:
            return json.dumps(array_)
        else:
            return array_

    def _from(self, _array_of_blocks):
        """
        Sets the array of blocks of current instance not from dictionary directly but from supplied array of
        AbstractBlock instances. It's an internal method, the static method <of> should be used to create an instance
        from an array of already serialized blocks, that is, an array of dictionaries
        """
        assert len(list(filter(lambda x: not x, [isinstance(elem, AbstractBlock)
                                                 for elem in _array_of_blocks]))) == 0, \
            'All elements in array must be an instance of AbstractBlock'
        setattr(self, '_blocks', _array_of_blocks)

    def has_input_block(self):
        """
        Check if current blocks contain an Input block type. Useful to validate submit field in Views
        :return: True if contains an Input Block, False otherwise
        """
        for blk in getattr(self, '_blocks'):
            if isinstance(blk, Input):
                return True
        return False

    def num_of_blocks(self):
        """
        Provides the current number of block elements created
        :return: The length of internal array _blocks
        """
        return len(getattr(self, '_blocks'))

    @staticmethod
    def of(_array_of_dicts, from_json=False):
        """
        Provides an instance of BlocksArray initialized with supplied array of serialized blocks. Supplied argument
        must be an array of Block's dictionaries, or a json dumps of such array
        :param _array_of_dicts: An array of Block dictionaries
        :param from_json: Supplied dictionary is in json representation
        :return: An instance of BlockArray with an array of instances of AbstractBlocks in field _blocks
        """
        if from_json:
            assert isinstance(_array_of_dicts, str), 'Supplied array of dictionaries should be a json representation' \
                                                     'as a string, if from_json param is True'
            _array_of_dicts = json.loads(_array_of_dicts)

        assert isinstance(_array_of_dicts, list), '_array_of_dicts must be an array'
        instance = BlocksArray()
        instance._from([BlocksFactory.of(d) for d in _array_of_dicts])
        return instance

    class Builder(AbstractBuilder):

        __obj__ = 'BlocksArray'

        def Actions(self):
            """
            Appends an instance of Actions to current array of blocks, and returns the Builder the instance
            :return: The builder of the Actions just added to the array of blocks
            """
            _builder = Actions.Builder(_parent=self)
            _blocks = getattr(getattr(self, '_obj'), '_blocks')
            _blocks.append(_builder.build())
            return _builder

        def Context(self):
            """
            Appends an instance of Context to current array of blocks, and returns the Builder the instance
            :return: The builder of the Context just added to the array of blocks
            """
            _builder = Context.Builder(_parent=self)
            _blocks = getattr(getattr(self, '_obj'), '_blocks')
            _blocks.append(_builder.build())
            return _builder

        def Divider(self):
            """
            Appends an instance of Divider to current array of blocks, and returns the Builder the instance
            :return: The builder of the Divider just added to the array of blocks
            """
            _builder = Divider.Builder(_parent=self)
            _blocks = getattr(getattr(self, '_obj'), '_blocks')
            _blocks.append(_builder.build())
            return _builder

        def Header(self):
            _builder = Header.Builder(_parent=self)
            _blocks = getattr(getattr(self, '_obj'), '_blocks')
            _blocks.append(_builder.build())
            return _builder

        def Input(self):
            """
            Appends an instance of Input to current array of blocks, and returns the Builder the instance
            :return: The builder of the Input just added to the array of blocks
            """
            _builder = Input.Builder(_parent=self)
            _blocks = getattr(getattr(self, '_obj'), '_blocks')
            _blocks.append(_builder.build())
            return _builder

        def Section(self):
            """
            Appends an instance of Section to current array of blocks, and returns the Builder the instance
            :return: The builder of the Section just added to the array of blocks
            """
            _builder = Section.Builder(_parent=self)
            _blocks = getattr(getattr(self, '_obj'), '_blocks')
            _blocks.append(_builder.build())
            return _builder


class BlocksFactory:
    """
    Factory class to deserialize blocks back to objects. Very useful to manipulate messages and update content
    of objects that extend AbstractBlock
    """
    _BLOCK_BY_TYPE = {Actions.__type__: Actions,
                      Button.__type__: Button,
                      Context.__type__: Context,
                      Divider.__type__: Divider,
                      Header.__type__: Header,
                      Image.__type__: Image,
                      Input.__type__: Input,
                      MarkDown.__type__: MarkDown,
                      MultiSelectMenu.__type__: MultiSelectMenu,
                      Overflow.__type__: Overflow,
                      PlainText.__type__: PlainText,
                      PlainTextInput.__type__: PlainTextInput,
                      Section.__type__: Section,
                      SelectMenu.__type__: SelectMenu,
                      Modal.__type__: Modal}

    _BLOCK_BY_REQUIRED_FIELDS = {Confirmation.__required_slots__: Confirmation,
                                 Option.__required_slots__: Option,
                                 OptionGroup.__required_slots__: OptionGroup}

    @classmethod
    def __class_of_type(cls, type_):
        """
        Creates an empty Block object based on type
        :param type_: The type of the block object
        :return: The class of the block
        """
        return cls._BLOCK_BY_TYPE.get(type_)

    @classmethod
    def __class_of_fields(cls, _fields):
        """
        Creates an empty Block object based on the supplied fields, comparing with required fields of other instances
        :param _fields: The list of fields of the block object
        :return: The class of the block which required fields are included in the _fields set
        """
        for _req_fields, classname in cls._BLOCK_BY_REQUIRED_FIELDS.items():
            if set(_req_fields).issubset(set(_fields)):
                return classname
        raise AttributeError('supplied fields do not match any block structure')

    @classmethod
    def get_block_class(cls, dict_):
        """
        It checks if type_ exists in given dictionary, and then loads the class of that type. If no "type" field is
        in the dictionary, then it checks the field names to see if they match a set of required fields by some blocks,
        in such case, an instance of that class is loaded. If no match is found, then None is returned
        :param dict_: A dictionary with blocks fields to try to find a Block name
        :return: The name of the class that matches supplied dictionary fields, or None if no match is found
        """
        # find the kind of block
        type_ = dict_.get('type')
        if type_:
            class_of = cls.__class_of_type(type_)
        else:
            try:
                class_of = cls.__class_of_fields([f'_{k}' for k in dict_.keys()])
            except AttributeError:
                return None
        return class_of

    @staticmethod
    def of(dictionary, from_json=False):
        """
        Builds an instance of a class that inherits from AbstractBlock from supplied dictionary
        :param dictionary:  The previously serialized dictionary
        :param from_json: Supplied dictionary is a json representation of a dictionary
        :return: An instance of some class that extends AbstractBlock
        """
        if from_json:
            assert isinstance(dictionary, str), 'Supplied dictionary must be a string representation of a dictionary if' \
                                                'from_json param is True'
            dictionary = json.loads(dictionary)

        assert isinstance(dictionary, dict), 'Only dictionaries are supported in this method, If you are trying to ' \
                                             'deserialize an array of blocks, use <BlocksArray.of> method  instead'

        class_of = BlocksFactory.get_block_class(dictionary)
        assert issubclass(class_of, AbstractBlock), 'Unknown dict type. Only AbstractBlock classes can be deserialized'

        return class_of.deserialize(dictionary)
