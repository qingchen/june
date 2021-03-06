# coding: utf-8

from flask import Blueprint, request
from flask import render_template, abort
from ..helpers import force_int
from ..models import Account, Topic, fill_with_nodes


__all__ = ['bp']

bp = Blueprint('user', __name__)


@bp.route('/')
def users():
    """
    The user list page.
    """
    page = force_int(request.args.get('page', 1), 0)
    if not page:
        return abort(404)
    paginator = Account.query.order_by(Account.id.desc()).paginate(page)
    staffs = Account.query.filter(Account.role.in_(('staff', 'admin'))).all()
    return render_template(
        'user/users.html',
        paginator=paginator,
        staffs=staffs
    )


@bp.route('/<username>')
def view(username):
    """
    View a user with the given username.

    :param username: the username of a user.
    """
    page = force_int(request.args.get('page', 1), 0)
    if not page:
        return abort(404)
    user = Account.query.filter_by(username=username).first_or_404()
    topics = Topic.query.filter_by(account_id=user.id)\
            .order_by(Topic.id.desc()).limit(16)
    topics = fill_with_nodes(topics)
    return render_template('user/view.html', user=user, topics=topics)
