import base64
import os
from datetime import datetime, timedelta
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)

        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }

        return data


class User(PaginatedAPIMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(64))
    token = db.Column(db.String(32), unique=True)
    token_expiration = db.Column(db.DateTime)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def to_dict(self):
        data = {
            'id':    self.id,
            'email': self.email,
            'name':  self.name
        }

        return data


    def from_dict(self, data, new_user=False):
        for field in ['id', 'email', 'name']:
            if field in data:
                setattr(self, field, data[field])

        if new_user and 'password_hash' in data:
            self.set_password(data['password_hash'])


    def get_token(self, expires_in=3600):
        now = datetime.now()

        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token

        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)

        db.session.add(self)

        return self.token


    def revoke_token(self):
        self.token_expiration = datetime.now() - timedelta(seconds=1)


    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()

        if user is None or user.token_expiration < datetime.now():
            return None
            
        return user