from sqlalchemy import select

from fast_zero.models import ToDo, User


def test_create_user(session):
    new_user = User(username='Alice', password='secret', email='teste@test.com')
    session.add(new_user)
    session.commit()

    user_bd = session.scalar(select(User).where(User.username == 'Alice'))

    assert user_bd.username == 'Alice'
    assert user_bd.email == 'teste@test.com'


def test_create_todo(session, user: User):
    to_do_db = ToDo(
        title='Test Todo',
        description='Test Desc',
        state='draft',
        user_id=user.id,
    )

    session.add(to_do_db)
    session.commit()
    session.refresh(to_do_db)

    user = session.scalar(select(User).where(User.id == user.id))

    assert to_do_db.title == 'Test Todo'
    assert to_do_db.description == 'Test Desc'
    assert to_do_db.state == 'draft'
    assert to_do_db in user.todos
