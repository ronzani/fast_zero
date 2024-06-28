from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    new_user = User(
        username='Alice', password='secret', email='teste@test.com'
    )
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'Alice'))

    assert user.username == 'Alice'
    assert user.email == 'teste@test.com'
