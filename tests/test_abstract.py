"""
Class with nosetests for AbstractBlock and AbstractBuilder in slack_view library
"""

from mock import patch, Mock
from nose.tools import raises

from slackviews.view import AbstractBlock, AbstractBuilder

__author__ = 'Agustin Escamez'
__email__ = 'aech22@gmail.com'


class TestAbstract:

    @raises(NotImplementedError)
    @patch.object(AbstractBlock, '__type__')
    def test_should_abstractblock_validation_raise_notimplementederror_if_not_in_instance_class(self, mock_type):
        # GIVEN
        mock_type.return_value = 'any_type'

        # WHEN
        AbstractBlock()

        # THEN
        assert mock_type.called

    @raises(AttributeError)
    def test_should_abstractbuilder_raise_attributeerror_if_obj_not_defined(self):
        # WHEN
        AbstractBuilder()

    @patch.object(AbstractBuilder, '__obj__')
    def test_should_abstractblock_end_provide_correct_parent_reference(self, mock_obj):
        # GIVEN
        mock_obj.return_value = str
        mock_parent = Mock()
        builder = AbstractBuilder(_parent=mock_parent)

        # WHEN
        parent_ref = builder.up()

        # THEN
        assert mock_obj.called
        assert parent_ref == mock_parent

    @patch.object(AbstractBuilder, '__obj__')
    def test_should_abstractblock_build_provide_correct_object_instance(self, mock_obj):
        # GIVEN
        mock_obj.return_value = 'AnyClass'
        builder = AbstractBuilder()

        # WHEN
        build_ref = builder.build()

        # THEN
        assert mock_obj.called
        assert isinstance(build_ref, str)
        assert build_ref == 'AnyClass'
