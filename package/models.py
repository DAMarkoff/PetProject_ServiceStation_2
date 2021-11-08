# coding: utf-8
from sqlalchemy import BigInteger, Boolean, Column, Date, DateTime, ForeignKey, Integer, String, Table, Time, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from package import db

Base = declarative_base()
metadata = Base.metadata


t_managers = Table(
    'managers', metadata,
    Column('manager_id', Integer, unique=True),
    Column('first_name', String(20)),
    Column('last_name', String(50)),
    Column('position_id', Integer),
    Column('email', String(100)),
    Column('phone', String(30)),
    Column('hour_cost', Integer),
    Column('active', Boolean)
)


class Position(Base):
    __tablename__ = 'positions'

    position_id = Column(Integer, primary_key=True)
    position_name = Column(String(20), nullable=False)
    salary = Column(Integer, nullable=False)
    delta_minutes = Column(Integer, nullable=False)


# class Size(Base):
#     __tablename__ = 'sizes'
#
#     size_id = Column(Integer, primary_key=True)
#     size_name = Column(Integer)


# class Size(db.Model):
#     __tablename__ = 'sizes'
#
#     size_id = db.Column('size_id', Integer, primary_key=True)
#     size_name = db.Column('size_name', Integer)


class Task(Base):
    __tablename__ = 'tasks'

    task_id = Column(Integer, primary_key=True)
    task_name = Column(String(30), nullable=False)
    task_cost = Column(Integer, nullable=False)
    task_duration = Column(Time, nullable=False)


class TireServiceOrderType(Base):
    __tablename__ = 'tire_service_order_type'

    service_type_id = Column(Integer, primary_key=True, server_default=text("nextval('tire_service_order_type_service_type_id_seq'::regclass)"))
    service_type_name = Column(String, nullable=False)


# class UsersGroup(Base):
#     __tablename__ = 'users_groups'
#
#     group_id = Column(Integer, primary_key=True, server_default=text("nextval('users_groups_group_id_seq'::regclass)"))
#     group_name = Column(String, nullable=False)


class Vehicle(Base):
    __tablename__ = 'vehicle'

    vehicle_id = Column(Integer, primary_key=True)
    vehicle_name = Column(String(20), nullable=False)


class Staff(Base):
    __tablename__ = 'staff'

    worker_id = Column(Integer, primary_key=True)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(50), nullable=False)
    position_id = Column(ForeignKey('positions.position_id'), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(30), nullable=False)
    hour_cost = Column(Integer, nullable=False)
    active = Column(Boolean, nullable=False, server_default=text("true"))

    position = relationship('Position')


# class User(db.Model, UserMixin):
# class User(Base):
#     __tablename__ = 'users'
#
#     user_id = Column(BigInteger, primary_key=True, server_default=text("nextval('users_user_id_seq'::regclass)"))
#     first_name = Column(String(50), nullable=False)
#     last_name = Column(String(50), nullable=False)
#     email = Column(String(100), nullable=False)
#     phone = Column(String(30), nullable=False)
#     _pass = Column('pass', String(32))
#     active = Column(Boolean, nullable=False, server_default=text("true"))
#     password = Column(String, nullable=False)
#     salt = Column(String, nullable=False)
#     created = Column(DateTime)
#     group_id = Column(ForeignKey('users_groups.group_id'), nullable=False)
#
#     group = relationship('UsersGroup')


class Warehouse(Base):
    __tablename__ = 'warehouse'

    shelf_id = Column(Integer, primary_key=True)
    active = Column(Boolean, nullable=False)
    size_id = Column(ForeignKey('sizes.size_id'), nullable=False)

    size = relationship('Size')


class StorageOrder(Base):
    __tablename__ = 'storage_orders'

    storage_order_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    start_date = Column(Date, nullable=False)
    stop_date = Column(Date, nullable=False)
    storage_order_cost = Column(Integer, nullable=False)
    shelf_id = Column(ForeignKey('warehouse.shelf_id'), nullable=False)
    created = Column(DateTime)

    shelf = relationship('Warehouse')
    user = relationship('User')


class UserVehicle(Base):
    __tablename__ = 'user_vehicle'

    user_vehicle_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    vehicle_id = Column(ForeignKey('vehicle.vehicle_id'), nullable=False)
    size_id = Column(ForeignKey('sizes.size_id'), nullable=False)
    created = Column(DateTime)

    size = relationship('Size')
    user = relationship('User')
    vehicle = relationship('Vehicle')


class TireServiceOrder(Base):
    __tablename__ = 'tire_service_order'

    service_order_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    start_datetime = Column(DateTime, nullable=False)
    user_vehicle_id = Column(ForeignKey('user_vehicle.user_vehicle_id'), nullable=False)
    manager_id = Column(Integer, nullable=False)
    stop_datetime = Column(DateTime, nullable=False)
    service_type_id = Column(ForeignKey('tire_service_order_type.service_type_id'), nullable=False)
    created = Column(DateTime, nullable=False)
    service_order_cost = Column(Integer)

    service_type = relationship('TireServiceOrderType')
    user = relationship('User')
    user_vehicle = relationship('UserVehicle')


class ListOfWork(Base):
    __tablename__ = 'list_of_works'

    work_id = Column(Integer, primary_key=True)
    service_order_id = Column(ForeignKey('tire_service_order.service_order_id', ondelete='CASCADE'), nullable=False)
    task_id = Column(ForeignKey('tasks.task_id'), nullable=False, server_default=text("0"))
    worker_id = Column(ForeignKey('staff.worker_id'), nullable=False, server_default=text("0"))

    service_order = relationship('TireServiceOrder')
    task = relationship('Task')
    worker = relationship('Staff')
