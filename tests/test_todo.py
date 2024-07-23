from http import HTTPStatus

from fast_zero.models import ToDoState
from tests.conftest import ToDoFactory


def test_create_todo(client, header_authorization):
    response = client.post(
        '/todo/',
        headers=header_authorization,
        json={
            'title': 'Test Todo',
            'description': 'Test Description',
            'state': 'draft',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'title': 'Test Todo',
        'description': 'Test Description',
        'state': 'draft',
    }


def test_list_to_dos_should_return_5(session, client, user, header_authorization):
    expected_to_dos = 5
    session.bulk_save_objects(ToDoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/todo/',
        headers=header_authorization,
    )

    assert len(response.json()['result']) == expected_to_dos


def test_list_to_dos_should_return_2(session, client, user, header_authorization):
    expected_to_dos = 2
    session.bulk_save_objects(ToDoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/todo/?offset=1&limit=2',
        headers=header_authorization,
    )

    assert len(response.json()['result']) == expected_to_dos


def test_list_to_dos_filter_title_should_return_5(
    session, client, user, header_authorization
):
    expected_to_dos = 5
    session.bulk_save_objects(
        ToDoFactory.create_batch(5, user_id=user.id, title='Test title')
    )
    session.commit()

    response = client.get(
        '/todo/?title=test',
        headers=header_authorization,
    )

    assert len(response.json()['result']) == expected_to_dos


def test_list_to_dos_filter_description_should_return_5(
    session, client, user, header_authorization
):
    expected_to_dos = 5
    session.bulk_save_objects(
        ToDoFactory.create_batch(5, user_id=user.id, description='Test Description')
    )
    session.commit()

    response = client.get(
        '/todo/?description=test',
        headers=header_authorization,
    )

    assert len(response.json()['result']) == expected_to_dos


def test_list_to_dos_filter_state_should_return_5(
    session, client, user, header_authorization
):
    expected_to_dos = 5
    session.bulk_save_objects(
        ToDoFactory.create_batch(5, user_id=user.id, state=ToDoState.draft)
    )
    session.commit()

    response = client.get(
        '/todo/?state=draft',
        headers=header_authorization,
    )

    assert len(response.json()['result']) == expected_to_dos


def test_list_todos_filter_combined_should_return_5(
    session, client, user, header_authorization
):
    expected_to_dos = 5
    session.bulk_save_objects(
        ToDoFactory.create_batch(
            5,
            user_id=user.id,
            title='Test title',
            description='Test Description',
            state=ToDoState.done,
        )
    )

    session.bulk_save_objects(
        ToDoFactory.create_batch(
            3,
            user_id=user.id,
            title='Other title',
            description='Other Description',
            state=ToDoState.doing,
        )
    )

    session.commit()

    response = client.get(
        '/todo/?title=test&description=test&state=done',
        headers=header_authorization,
    )

    assert len(response.json()['result']) == expected_to_dos


def test_list_todos_filter_combined_should_return_3(
    session, client, user, header_authorization
):
    expected_to_dos = 3
    session.bulk_save_objects(
        ToDoFactory.create_batch(
            5,
            user_id=user.id,
            title='Test title',
            description='Test Description',
            state=ToDoState.done,
        )
    )

    session.bulk_save_objects(
        ToDoFactory.create_batch(
            3,
            user_id=user.id,
            title='Other title',
            description='Other Description',
            state=ToDoState.doing,
        )
    )

    session.commit()

    response = client.get(
        '/todo/?title=test&description=test&state=done&offset=2&limit=3',
        headers=header_authorization,
    )

    assert len(response.json()['result']) == expected_to_dos
