#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
#******************************************************************************
#********************* Carbyne Solutions, Incorporated ************************
#------------------------------------------------------------------------------
#
# [2014] - [2014] Carbyne Solutions, Incorporated
# All Rights Reserved
#
# Notice: All information contained herein is, and remains the property of
# Carbyne Solutions, Incorporated and its suppliers, if any. The intellectual
# and technical concepts contained herein are proprietary to Carbyne Solutions
# Incorporated and its suppliers, if any, and may be covered by U.S and Foreign
# Patents, patents in process, and are protected by trade secret or copyright
# law. Dissemination of this information or reproduction of this material is
# strictly forbidden unless prior written permission is obtained from Carbyne
# Solutions, Incorporated.
#
#******************************************************************************

from sqlalchemy import Column, create_engine, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, sessionmaker


class Adapter(object):
    """General Database Adapter that allows dynamic store operations on data."""

    def __init__(self, engine):
        """Initialize the Adapter with an engine string.

        http://docs.sqlalchemy.org/en/latest/core/engines.html
        """
        self.engine = create_engine(engine)
        self.base = declarative_base()
        self.tables = dict()  # key = tablename
        self.__table_definitions = dict()  # key = tablename
        self.types = dict()  # key typename

    @property
    def definitions(self):
        """Provide table definitions."""
        return self.__table_definitions

    def declare(self, tablename, pk, mapping):
        """Declare a table dynamically using the mapping.

        :param tablename: str. the name of the table to be defined
        :param pk: str. the primary key column defined in mapping
        :param mapping: dict. descriptive dictionary with table schema definitions
        :raises: AttributeError. if the pk was not found in the mapping

        For an example, take a look at the below code block
        .. code-block:: python

            {
                'id': Column(Integer, primary_key=True), 
                'name': Column(String), 
                'fullname': Column(String), 
                'password': Column(String)
            }
        """
        self.__table_definitions[tablename] = dict()
        if pk not in mapping.iterkeys():
            raise AttributeError('Invalid primary key defined')

        for column_name, column_declaration in mapping.iteritems():
            if column_name not in self.types:
                # Cache column types for all declaration imports
                _import = __import__('sqlalchemy', fromlist=[str(column_declaration)])
                self.types[column_name] = getattr(_import, column_declaration)

            self.__table_definitions[tablename][column_name] = Column(column_name, self.types[column_name])
            if pk == column_name:
                self.__table_definitions[tablename][column_name].primary_key=True

        metadata = MetaData(bind=self.engine)
        self.tables[tablename] = \
            Table(tablename, metadata, *self.__table_definitions[tablename].itervalues(), extend_existing=True)
        metadata.create_all()

    def query(self, tablename, column_name):
        """Helper fn to query a specific table for column."""
        class Table(object):
            pass

        Session = sessionmaker(bind=self.engine)
        session = Session()
        mapper(Table, self.tables[tablename])
        results = session.query(getattr(Table, column_name))

        return results