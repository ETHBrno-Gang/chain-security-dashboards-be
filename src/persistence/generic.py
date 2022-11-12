import logging
import sqlalchemy # noqa
import datetime
from typing import List, TypeVar, Generic, get_args, Optional
from . import db
from .utils import rollback_on_error


logger = logging.getLogger(__name__)


M = TypeVar("M", bound=db.Model)


class Repository(Generic[M]):
    ALL_DEFAULT_LIMIT = 100

    @classmethod
    def _get_model_type(cls):
        return get_args(cls.__orig_bases__[0])[0]  # noqa

    @classmethod
    def _get_model_type_name(cls):
        return cls._get_model_type().__name__

    @classmethod
    def _get_class_field(cls, field_name: str):
        if field_name not in cls._get_model_type().__dict__:
            return None
        return cls._get_model_type().__dict__[field_name]

    @classmethod
    def _get_filtered_query(cls, **kwargs) -> sqlalchemy.orm.query.Query:  # noqa
        for k in kwargs.keys():
            if k not in dir(cls._get_model_type()):
                logger.error(f'Tried to query "{cls._get_model_type_name()}" by "{k}", but it is not a member of the class')
        return cls._get_model_type().query.filter_by(**kwargs)

    # CREATE
    @classmethod
    @rollback_on_error
    def create(cls, entity: M) -> M:
        # TODO prevent creating twice
        # https://stackoverflow.com/questions/26655200/flask-sqlalchemy-check-whether-object-in-db-session-and-ready-for-commit
        # if already_exists(entity):
        #     logger.warning(f'Tried to create already existing entity. Will update instead')
        #     return cls.update(entity)
        db.session.add(entity)
        db.session.commit()
        logger.debug(f'Created {cls._get_model_type_name()} {entity}')
        return entity

    @classmethod
    @rollback_on_error
    def create_all(cls, entities_list: List[M]) -> List[M]:
        for e in entities_list:
            cls.create(e)
        logger.debug(f'Created {len(entities_list)} entities')
        return entities_list

    # READ
    @classmethod
    def read_by_primary_key(cls, pk: int) -> Optional[M]:
        logger.debug(f'Reading {cls._get_model_type_name()} with primary key {pk}')
        return cls._get_model_type().query.get(pk)

    @classmethod
    def read_by_unique(cls, **kwargs) -> Optional[M]:
        if len(kwargs) != 1:
            logger.warning(f'You should only query by a single unique identifier')
            return None
        field_name = list(kwargs.keys())[0]
        field = cls._get_class_field(field_name)
        if not field:
            logger.warning(f'No unique field found "{field_name}" in "{cls._get_model_type_name()}"')
            return None
        if not field.unique:
            logger.warning(f'You tried to perform a unique query on a non-unique field "{field_name}" of "{cls._get_model_type_name()}"')
            return None
        return cls._get_filtered_query(**kwargs).first()

    @classmethod
    def read_first(cls, **kwargs) -> Optional[M]:
        logger.debug(f'Reading first {cls._get_model_type_name()} with filters {kwargs}')
        return cls._get_filtered_query(**kwargs).first()

    @classmethod
    def read_last(cls, **kwargs) -> Optional[M]:
        logger.debug(f'Reading last {cls._get_model_type_name()} with filters {kwargs}')
        return cls._get_filtered_query(**kwargs).order_by(cls._get_model_type().id.desc()).first()

    @classmethod
    def read_all(cls, limit: int = None, use_limit: bool = True, **kwargs) -> List[M]:
        limit = limit or cls.ALL_DEFAULT_LIMIT
        limit_msg = f'limit {limit}' if use_limit else 'no limit'
        logger.debug(f'Reading all "{cls._get_model_type_name()}" with filters {kwargs} with {limit_msg}')
        if use_limit:
            return cls._get_filtered_query(**kwargs).limit(cls.ALL_DEFAULT_LIMIT).all()
        else:
            return cls._get_filtered_query(**kwargs).all()

    # UPDATE
    @classmethod
    @rollback_on_error
    def update(cls, entity: M) -> M:
        if hasattr(entity, 'updated_at'):
            entity.updated_at = datetime.datetime.now()
        db.session.add(entity)
        db.session.commit()
        logger.debug(f'Updated {cls._get_model_type_name()} {entity}')
        return entity

    # DELETE
    @classmethod
    @rollback_on_error
    def delete(cls, entity: M) -> M:
        db.session.delete(entity)
        db.session.commit()
        logger.debug(f'Deleted {cls._get_model_type_name()} {entity}')
        return entity
