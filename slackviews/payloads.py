"""
Module with logic to handle different types of payloads in Slack
"""
import abc
import logging

from slackviews import View
from werkzeug.datastructures import ImmutableDict


# -- helper
def get_obj_attr(object, item, missing_value=None, join_with=None, transform=None):
    """
    Returns the value of an object's attribute, checking if it exists. It can provide a predefined default value,
    in case it's an array can be joined with supplied char, and can be even transformed with supplied lambda function
    :param object: The object to look for the attribute
    :param item: The name of the field to retrieve
    :param missing_value: Default value in case it doesn't exists
    :param join_with: If the field value is an array, join the items with supplied char
    :param transform: Apply supplied transformation to the field, or to each member of the field if it's
    an array. The supplied function, must consider the type of data that the field value should contain, that is,
    we can not apply an upper() to an integer, for example.
    :return: The value of the field, or the default value if it doesn't exists and, optionally, transformed with
    supplied function or if it's an array, a single value with it's items joined
    """
    # traverse fields if several are provided joined by a dot
    fields = item.split('.')
    item = fields[-1]

    for _child in fields[:-1]:
        if hasattr(object, _child):
            object = getattr(object, _child)
        else:
            return missing_value

    if not hasattr(object, item):
        return missing_value

    value = getattr(object, item)

    if not isinstance(value, list):
        if transform:
            return transform(value)
        else:
            return value
    else:
        if transform and join_with:
            assert isinstance(join_with, str), f'{join_with} must be a string'
            return join_with.join([transform(x) for x in value])
        elif transform:
            return list(map(transform, value))
        elif join_with:
            return join_with.join(value)
        else:
            return value


# -- model classes to handle data easier

class Serializable:
    """
    Represents the interface that an object should implement to be serialized
    """
    def serialize(self, *skip_fields):
        """
        Serialize current object as json
        :param skip_fields: A list of fieldnames separated by colon to be skipped from serialized output
        :return: A valid serialized object as a dictionary
        """
        serialized_dict = dict()
        for k, v in self.__dict__.items():
            if k in skip_fields:
                continue
            if hasattr(v, 'serialize'):
                serialized_dict[k] = v.serialize(*skip_fields)
            else:
                serialized_dict[k] = v
        return serialized_dict


class DictionaryField(Serializable):
    """
    Encapsulates any object field with nested elements
    """
    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            if isinstance(value, dict):
                value = DictionaryField(**value)
            setattr(self, name, value)


class Command(ImmutableDict):

    __metaclass__ = abc.ABCMeta

    """
    Encapsulates the form content received when a slack command is invoked
    It's basically a wrapper over InmmutableDict to use it as a regular object
    with accessor methods
    """

    def __init__(self, _form, **kwargs):
        super().__init__(_form)

        # make sure command and arguments are ok
        self._verify_command()

    def token(self):
        """
        Provides the token
        :return: The token as a string
        """
        return self.get('token')

    def team_id(self):
        """
        Provides the team id
        :return: The team id as a string
        """
        return self.get('team_id')

    def team_domain(self):
        """
        Provides the team domain
        :return: The team domain as a string
        """
        return self.get('team_domain')

    def channel_id(self):
        """
        Provides id of the channel
        :return: The channel's id as a string
        """
        return self.get('channel_id')

    def channel_name(self):
        """
        Provides the name of the channel
        :return: The channel's name as a string
        """
        return self.get('channel_name')

    def user_id(self):
        """
        Provides user id
        :return: The user's id as a string
        """
        return self.get('user_id')

    def user_name(self):
        """
        Provides the user name
        :return: User's name as a string
        """
        return self.get('user_name')

    def command(self):
        """
        Provides invoked slack command
        :return: The name of the command as a string
        """
        return self.get('command')

    def text(self):
        """
        Provides arguments of invoked Slack commmand
        :return: The arguments of the slack command as a string
        """
        return self.get('text')

    def response_url(self):
        """
        Provides url to send the response of the command to
        :return: The response url for the command invoked
        """
        return self.get('response_url')

    def trigger_id(self):
        """
        Unique identifier of the action that started the interaction between
        user and the bot
        :return: The trigger id as a string
        """
        return self.get('trigger_id')

    def contains_command(self, command):
        """
        Checks if current form contains supplied command
        :param command: Name of the command to check
        :return: True if command in current form, False otherwise
        """
        return command in self.command()

    def contains_argument(self, arg):
        """
        Checks if current form contains supplied argument
        :param arg: name of the arg to check
        :return: True if arg in current form, False otherwise
        """
        return arg in self.text()

    def parse_args(self):
        """
        Returns an array with supplied arguments in form
        :return: An array with each argument in order
        """
        if not self.text():
            return []
        else:
            return self.text().split(' ')

    def num_args(self):
        """
        Provides the number of supplied arguments
        :return: The number of supplied arguments as an integer
        """
        return len(self.parse_args())

    @abc.abstractmethod
    def _verify_command(self):
        """
        Checks if command contains correct arguments for it's execution
        :return: True if arguments are correct. False otherwise
        """
        raise NotImplementedError()


# -- interactions
class HasBlocks:
    """
    Represents a interface that provides a method to get the blocks of an interaction
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def blocks(self):
        """
        Provides the blocks of last interaction
        :return: An array with blocks or an empty array
        """
        raise NotImplementedError()


class HasInputAction:
    """
    Represents a interface that provides a method to obtain a given input action in 'values' or 'actions' fields
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_input_action(self, block_id, action_id):
        """
        Checks if given block_id has an action_id is in submitted 'values' or 'actions'
        :param block_id: The block id of the input being searched
        :param action_id: The action_id being searched
        :return: True if exists, False otherwise
        """
        raise NotImplementedError()


class HasPrivateMetadata:
    """
    Interface that provides access to privatemetadata
    """
    __metaclass__ = abc.ABCMeta

    def private_metadata(self):
        """
        Provides the private metadata of interaction view, if any. In our
        model, if any content exists, it'll be given as a dictionary, since
        the format of private_metadata is field1=value1&field2=value2...

        A dictionary is built with supplied data

        :return: The private metadata content as dictionary
        """
        raise NotImplementedError()


class HasView(HasPrivateMetadata):
    """
    Represents an interface with methods to access interaction's view data
    """

    __metaclass__ = abc.ABCMeta

    def is_home(self):
        """
        Returns whether or not, current view is a "Home"
        :return: True if view is home, False otherwise
        """
        raise NotImplementedError()


class Interaction(DictionaryField, HasBlocks, HasInputAction):
    """
    Encapsulates the payload occurred in a message interaction (button, combo, date etc...)
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = logging.getLogger(self.__class__.__name__)

    def is_block_actions(self):
        return getattr(self, 'type') == 'block_actions'

    def is_view_submission(self):
        return getattr(self, 'type') == 'view_submission'

    def is_view_closed(self):
        return getattr(self, 'type') == 'view_closed'

    def search_block(self, block_id):
        """
        Searches for a given block_id in view's blocks
        :param block_id: The id of the block to look for
        :return: The block with given block_id, if anyone exists
        """
        _found = list(filter(lambda b: (b.get('block_id') == block_id) or (block_id in b.get('block_id')),
                             self.blocks()))
        if _found:
            return _found[0]
        else:
            return None

    def user_slack_id(self):
        """
        Provides the slack_id of the user who performed the interaction
        :return: The slack id as a string
        """
        return get_obj_attr(self, 'user.id', None)

    def get_selectmenu_value(self, block_id, action_id):
        """
        Provides the text, and the value of the select element in a SelectMenu
        :param block_id: The block id of the input being searched
        :param action_id: The action_id being searched
        :return: The text and value of the selected element in the SelectMenu
        """
        element = self.get_input_action(block_id, action_id)

        assert element.type == 'static_select', f'Wrong element type, it should be a static_select'
        value = get_obj_attr(element, 'selected_option.value')
        text = get_obj_attr(element, 'selected_option.text.text')

        self.logger.debug(f'\t text, value -> {text}, {value}')
        return text, value

    def get_textinput_value(self, block_id, action_id):
        """
        Provides the value, of a PlainTextInput element, if found
        :param block_id: The block id of the input being searched
        :param action_id: The action_id being searched
        :return: The value of the PlainTextInput element
        """
        element = self.get_input_action(block_id, action_id)

        assert element.type == 'plain_text_input', f'Wrong element type, it should be a plain_text_input'
        value = get_obj_attr(element, 'value')
        self.logger.debug(f'\f value -> {value}')
        return value


class ViewInteraction(Interaction, HasView):
    """
    Represent any interaction that contains view data
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._private_metadata = None

    @staticmethod
    def private_metadata_string(dictionary):
        """
        Creates a string that can be used as private_metadata from supplied dictionary
        :param dictionary: The dictionary with key=value pairs to create a string representation separated by &
        :return: A string representing private metadata from supplied dictionary
        """
        return '&'.join([f'{key}={value}' for key, value in dictionary.items()])

    @staticmethod
    def private_metadata_dictionary(string):
        """
        Creates a dictionary from supplied string with private metadata
        :param string: A private metadata string repsentation
        :return: A dictionary  representing private metadata from supplied string
        """
        dict_ = dict()
        for f in string.split('&'):
            f = f.split('=')
            dict_[f[0]] = f[1]
        return dict_

    def is_home(self):
        return get_obj_attr(self, 'view.type') == 'home'

    def private_metadata(self):
        """
        Provides the private metadata of interaction view, if any. In our
        model, if any content exists, it'll be given as a dictionary, since
        the format of private_metadata is field1=value1&field2=value2...

        A dictionary is built with supplied data

        :return: The private metadata content as dictionary
        """
        # depending on interaction, it could be a message, and not a view
        if not hasattr(self, 'view') or not getattr(getattr(self, 'view'), 'private_metadata'):
            return None
        if not self._private_metadata:
            _metadata = getattr(getattr(self, 'view'), 'private_metadata')
            self.logger.debug(f'converting {_metadata} to a dictionary....')
            dict_ = ViewInteraction.private_metadata_dictionary(_metadata)
            self.logger.debug(f'\t -> OK {dict_}')
            self._private_metadata = dict_
        return self._private_metadata

    def blocks(self):
        if not hasattr(self, 'view'):
            return []
        elif isinstance(getattr(self, 'view'), View):
            return getattr(getattr(self, 'view'), '_blocks')
        else:
            return getattr(getattr(self, 'view'), 'blocks')


class ViewSubmission(ViewInteraction):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_input_action(self, block_id, action_id):
        self.logger.debug(f'searching for __{action_id}__ in input block __{block_id}__')
        element = get_obj_attr(self, f'view.state.values.{block_id}.{action_id}')
        self.logger.debug(f'\t -> FOUND -> __{element}__')
        return element


class NoActionIdException(Exception):
    """
    Exception returned when no action_id is found in interaction message
    """


class BlockActions(Interaction):

    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def action_id(self):
        """
        Provides action_id name, if exists, else an empty string
        :return: Current action id name, or ''
        """
        if hasattr(self, 'actions'):
            return self.actions[0]['action_id']
        else:
            return NoActionIdException('No actions field in payload')

    def action_value(self):
        """
        Provides action_id value, if exists
        :return: Current action value as a string
        """
        if hasattr(self, 'actions'):
            return self.actions[0]['value']
        else:
            return NoActionIdException('No actions field in payload')

    def action_element_type(self):
        """
        Provides the type of element that started the  interaction, i.e. "button", ....
        :return: The type of element as a string
        """
        if hasattr(self, 'actions'):
            return self.actions[0]['type']
        else:
            return NoActionIdException('No actions field in payload')

    def get_input_action(self, block_id, action_id):
        self.logger.debug(f'searching for __{action_id}__ in input block __{block_id}__')
        element = None
        actions = [DictionaryField(**a) for a in get_obj_attr(self, 'actions', missing_value=[])]
        try:
            element = [act_ for act_ in actions if getattr(act_, 'block_id') == block_id and
                       getattr(act_, 'action_id') == action_id][0]
        except IndexError:
            pass

        self.logger.debug(f'\t -> FOUND -> __{element}__')
        return element


class ViewBlocksInteraction(BlockActions, ViewInteraction):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def blocks(self):
        if not hasattr(self, 'view'):
            return []
        elif isinstance(getattr(self, 'view'), View):
            return getattr(getattr(self, 'view'), '_blocks')
        else:
            return getattr(getattr(self, 'view'), 'blocks')


class MessageBlocksInteraction(BlockActions):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def message_ts(self):
        """
        Provides the message timestamp of this interaction
        :return: The message timestamp as a string
        """
        assert hasattr(self, 'container'), 'Wrong interaction type'
        return get_obj_attr(self, 'container.message_ts')

    def channel_id(self):
        """
        Provides the channel id where this interaction started
        :return: The id of the channel as a string
        """
        assert hasattr(self, 'channel'), 'Wrong interaction type'
        return get_obj_attr(self, 'channel.id')

    def channel_name(self):
        """
        Provides the channel name where this interaction started
        :return: The name of the channel as a string
        """
        assert hasattr(self, 'channel'), 'Wrong interaction type'
        return get_obj_attr(self, 'channel.name')

    def blocks(self):
        """
        Provides the interaction message's blocks array
        :return: The message blocks as an array
        """
        assert hasattr(self, 'message'), 'Wrong interaction type'
        return get_obj_attr(self, 'message.blocks')
