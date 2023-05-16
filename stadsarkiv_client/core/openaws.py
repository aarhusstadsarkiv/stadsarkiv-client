from openaws_client.client import Client, AuthenticatedClient

# JWT Login
from openaws_client.models.body_auth_db_bearer_login_v1_auth_jwt_login_post import (
    BodyAuthDbBearerLoginV1AuthJwtLoginPost as AuthJwtLoginPost,
)
from openaws_client.models.bearer_response import BearerResponse
from openaws_client.api.auth import auth_db_bearer_login_v1_auth_jwt_login_post as auth_jwt_login_post

# Users module
from openaws_client.api.users import users_current_user_v1_users_me_get as users_me_get
from openaws_client.models.user_read import UserRead

# Register module
from openaws_client.api.auth import register_register_v1_auth_register_post as auth_register_post
from openaws_client.models.user_create import UserCreate
from openaws_client.models.user_permissions import UserPermissions
from openaws_client.models.user_flag import UserFlag

# Verify
from openaws_client.api.auth import verify_verify_v1_auth_verify_post as auth_verify_post
from openaws_client.models.body_verify_verify_v1_auth_verify_post import BodyVerifyVerifyV1AuthVerifyPost as VerifyPost


# Forgotten password
from openaws_client.models.body_reset_forgot_password_v1_auth_forgot_password_post import (
    BodyResetForgotPasswordV1AuthForgotPasswordPost as ForgotPasswordPost,
)
from openaws_client.api.auth import (
    reset_forgot_password_v1_auth_forgot_password_post as auth_forgot_password_post,
)

# Schema
from openaws_client.models.schema_create import SchemaCreate
from openaws_client.models.schema_read import SchemaRead
from openaws_client.models.schema_create_data import SchemaCreateData

from openaws_client.api.schemas import (
    entity_get_schema_v1_schemas_name_get as schemas_name_get,
    entity_create_schema_v1_schemas_post as schemas_post,
    entity_get_available_schemas_v1_schemas_get as schemas_get,
)

# Entity models
from openaws_client.models.entity_create import EntityCreate
from openaws_client.models.entity_read import EntityRead
from openaws_client.models.entity_update import EntityUpdate

# Entity modules
from openaws_client.api.entities import (
    entity_create_entity_v1_entities_post as entities_post,
    entity_get_entities_v1_entities_get as entities_get,
    entity_update_entity_v1_entities_uuid_patch as entities_uuid_patch,
    entity_get_entity_v1_entities_uuid_get as entities_uuid_get,
)

# Records models
from openaws_client.models.records_get_record_v1_records_record_id_get_response_records_get_record_v1_records_record_id_get import (
    RecordsGetRecordV1RecordsRecordIdGetResponseRecordsGetRecordV1RecordsRecordIdGet as RecordsIdGet,
)
from openaws_client.models.records_search_records_v1_records_search_get_response_records_search_records_v1_records_search_get import (
    RecordsSearchRecordsV1RecordsSearchGetResponseRecordsSearchRecordsV1RecordsSearchGet as RecordsSearchGet,
)

from openaws_client.api.proxies import (
    records_get_record_v1_records_record_id_get as record_id_get,
    records_search_records_v1_records_search_get as records_search_get,
)

# Error / Validation
from openaws_client.models.http_validation_error import HTTPValidationError
from openaws_client.models.error_model import ErrorModel

__ALL__ = [
    # auth
    AuthJwtLoginPost,
    auth_jwt_login_post,
    BearerResponse,
    # verify
    auth_verify_post,
    VerifyPost,
    # me
    UserRead,
    UserPermissions,
    users_me_get,
    # errors
    HTTPValidationError,
    ErrorModel,
    # Register. Forgot password
    ForgotPasswordPost,
    UserCreate,
    UserFlag,
    auth_register_post,
    auth_forgot_password_post,
    # schema
    SchemaCreate,
    SchemaRead,
    SchemaCreateData,
    schemas_name_get,
    schemas_post,
    schemas_get,
    # entity
    EntityRead,
    EntityCreate,
    EntityUpdate,
    entities_uuid_patch,
    entities_get,
    entities_post,
    entities_uuid_get,
    # records
    RecordsIdGet,
    RecordsSearchGet,
    record_id_get,
    records_search_get,
    # client related
    AuthenticatedClient,
    Client,
]
