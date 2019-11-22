"""
Сlass with the basic methods of interacting with the database
"""
from sqlalchemy.orm import Query
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import NotFound
from .core import db
from typing import Union
import uuid


class BaseDBService:
    model = None

    def get_by_id(self, id_: int) -> db.Model:
        """
        Get instance by id
        :param id_:
        :return: instance or NotFound
        :raise NotFound: if instance not found
        """
        try:
            return db.session.query(self.model).filter_by(id=id_).one()
        except NoResultFound as e:
            raise NotFound()

    def get_by_id_or_none(self, id_: int) -> Union[db.Model, None]:
        """
        Get instance by id
        :param id_:
        :return: instance or none
        """
        return db.session.query(self.model).filter_by(id=id_).first()

    def get_by_uuid(self, uuid_: str) -> db.Model:
        """
        Get instance by uuid
        :param uuid_:
        :return: instance or NotFound
        :raise  NotFound: if instance not found
        """
        try:
            return db.session.query(self.model).filter_by(uuid=uuid_).one()
        except NoResultFound as e:
            raise NotFound()

    def get_by_uuid_or_none(self, uuid_: str) -> Union[db.Model, None]:
        """
        Get instance by uuid
        :param uuid_:
        :return: instance or none
        """
        return db.session.query(self.model).filter_by(uuid=uuid_).first()

    def get_uuid_by_id(self, id_: int) -> uuid:
        """
        Get uuid by id
        :param id_:
        :return: uuid for instance
        """
        return db.session.query(self.model.uuid).filter_by(id=id_).first().uuid

    def filter(self, **kwargs):
        """
        Filter
        :param kwargs:
        :return:
        """
        return db.session.query(self.model).filter_by(**kwargs)

    def apply_pagination(self, query: Query, start: int, page_size: int) -> Query:
        """
        Apply pagination for page
        :param query:
        :param start:
        :param page_size:
        :return:
        """
        return query.paginate(start, page_size, True)

    def new(self, **kwargs) -> db.Model:
        """
        Create instance
        :param kwargs:
        :return:
        """
        instance = self.model(**kwargs)

        db.session.add(instance)

        return instance

    def commit(self):
        """
        Make Commit
        :return:
        """
        db.session.commit()


