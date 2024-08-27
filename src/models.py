import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False, unique=True)
    firstname = Column(String(250), nullable=False)
    lastname = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, unique=True)

    # Relationship to Post and Follower
    posts = relationship('Post', back_populates='user')
    followers = relationship('Follower', foreign_keys='Follower.user_from_id', back_populates='user_from')
    followed = relationship('Follower', foreign_keys='Follower.user_to_id', back_populates='user_to')
    comments = relationship('Comment', back_populates='author')

class Follower(Base):
    __tablename__ = 'follower'
    id = Column(Integer, primary_key=True)
    user_from_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user_to_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    # Relationships to the User
    user_from = relationship('User', foreign_keys=[user_from_id], back_populates='followers')
    user_to = relationship('User', foreign_keys=[user_to_id], back_populates='followed')

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    # Relationships to User, Media, and Comment
    user = relationship('User', back_populates='posts')
    media = relationship('Media', back_populates='post')
    comments = relationship('Comment', back_populates='post')

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    type = Column(String(250), nullable=False)
    url = Column(String(250), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)

    # Relationship to Post
    post = relationship('Post', back_populates='media')

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    comment_text = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)

    # Relationships to User and Post
    author = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')

# Crear el diagrama a partir del modelo de SQLAlchemy
try:
    result = render_er(Base, 'diagram.png')
    print("¡Éxito! En realizar mis tablas con sus relaciones")
except Exception as e:
    print("Hubo un problema generando el diagrama")
    raise e
