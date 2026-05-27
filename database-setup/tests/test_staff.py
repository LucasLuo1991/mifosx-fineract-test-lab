import pytest
from api.api_client import FineractApiClient
from api.endpoints.staff import StaffEndpoint
from helpers.staff_helper import assert_staff_present, create_missing_staff, load_staff
from sqlalchemy.engine import Connection


@pytest.fixture(scope="module")
def staff_api(authenticated_api_client: FineractApiClient) -> StaffEndpoint:
    return authenticated_api_client.staff  # type: ignore


def test_staff_are_seeded(staff_api: StaffEndpoint, db_connection: Connection):
    staff = load_staff("staff.json")

    create_missing_staff(
        staff_api=staff_api,
        db_connection=db_connection,
        staff_members=staff,
    )

    assert_staff_present(
        db_connection=db_connection,
        staff=staff,
    )
