from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_read_root_must_return_ok_and_hello_word(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK


def test_creat_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'Douglas',
            'email': 'DouglasPaz@gmail.com',
            'password': '123456'
        }

    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'Douglas',
        'email': 'DouglasPaz@gmail.com',
        }


def test_read_user(client, create_fake_user, token):
    user_schema = UserPublic.model_validate(create_fake_user).model_dump()
    response = client.get(
        '/users/',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, create_fake_user, token):
    response = client.put(
        f'/users/{create_fake_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'Testeatualizado',
            'email': 'Testeatualizado@gmail.com',
            'password': '123456'
        }
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'Testeatualizado',
        'email': 'Testeatualizado@gmail.com',
        }


def test_delete_user(client, create_fake_user, token):

    response = client.delete(
        f'/users/{create_fake_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK


def test_update_user_with_wrong_user(client, create_fake_other_user, token):
    response = client.put(
        f'/users/{create_fake_other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        'detail':
        'Esse usuário não tem permissão para alterar outro'
        }
