"""initial schema

Revision ID: 001
Revises: 
Create Date: 2026-11-13

-- requirement: FR-001, FR-002, FR-004, FR-023, FR-024, NFR-015
"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # requirement: FR-001, FR-002, FR-004
    op.create_table(
        'cases',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('case_reference', sa.String(length=64), nullable=False),
        sa.Column('workflow_type', sa.String(length=32), nullable=False),
        sa.Column('submission_channel', sa.String(length=32), nullable=False),
        sa.Column('applicant_reference', sa.String(length=128), nullable=False),
        sa.Column('applicant_name', sa.String(length=256), nullable=False),
        sa.Column('goods_description', sa.String(), nullable=True),
        sa.Column('origin_country_code', sa.String(length=8), nullable=True),
        sa.Column('agreement_reference', sa.String(length=64), nullable=True),
        sa.Column('case_state', sa.String(length=32), nullable=False),
        sa.Column('current_step_id', sa.String(length=16), nullable=False),
        sa.Column('accountable_role', sa.String(length=64), nullable=False),
        sa.Column('registration_sync_status', sa.String(length=16), nullable=False),
        sa.Column('reason_codes_json', sa.JSON().with_variant(postgresql.JSONB(), 'postgresql'), nullable=False, server_default=sa.text("'[]'")),
        sa.Column('submitted_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('case_reference')
    )
    op.create_index(op.f('ix_cases_case_reference'), 'cases', ['case_reference'], unique=True)
    op.create_index(op.f('ix_cases_workflow_type'), 'cases', ['workflow_type'], unique=False)
    op.create_index(op.f('ix_cases_case_state'), 'cases', ['case_state'], unique=False)
    op.create_index(op.f('ix_cases_accountable_role'), 'cases', ['accountable_role'], unique=False)

    # requirement: FR-001
    op.create_table(
        'case_attachments',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('case_id', sa.Uuid(), nullable=False),
        sa.Column('file_name', sa.String(length=256), nullable=False),
        sa.Column('media_type', sa.String(length=128), nullable=False),
        sa.Column('storage_key', sa.String(length=512), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['case_id'], ['cases.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_case_attachments_case_id'), 'case_attachments', ['case_id'], unique=False)

    # requirement: FR-023, FR-024
    op.create_table(
        'case_events',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('case_id', sa.Uuid(), nullable=False),
        sa.Column('event_type', sa.String(length=64), nullable=False),
        sa.Column('step_id', sa.String(length=16), nullable=False),
        sa.Column('decision_source', sa.String(length=32), nullable=False),
        sa.Column('actor_type', sa.String(length=32), nullable=False),
        sa.Column('actor_id', sa.String(length=128), nullable=False),
        sa.Column('visible_to_external', sa.Boolean(), nullable=False),
        sa.Column('reason_code', sa.String(length=128), nullable=True),
        sa.Column('rationale_summary', sa.String(), nullable=True),
        sa.Column('evidence_ref', sa.String(length=256), nullable=True),
        sa.Column('correlation_id', sa.String(length=128), nullable=False),
        sa.Column('payload_json', sa.JSON().with_variant(postgresql.JSONB(), 'postgresql'), nullable=False),
        sa.Column('occurred_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['case_id'], ['cases.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_case_events_case_id'), 'case_events', ['case_id'], unique=False)
    op.create_index(op.f('ix_case_events_correlation_id'), 'case_events', ['correlation_id'], unique=False)
    op.create_index(op.f('ix_case_events_occurred_at'), 'case_events', ['occurred_at'], unique=False)

    # requirement: FR-023, FR-024
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('case_id', sa.Uuid(), nullable=True),
        sa.Column('event_category', sa.String(length=64), nullable=False),
        sa.Column('severity', sa.String(length=16), nullable=False),
        sa.Column('actor_id', sa.String(length=128), nullable=False),
        sa.Column('action', sa.String(length=128), nullable=False),
        sa.Column('correlation_id', sa.String(length=128), nullable=False),
        sa.Column('entity_type', sa.String(length=64), nullable=False),
        sa.Column('entity_id', sa.String(length=128), nullable=False),
        sa.Column('details_json', sa.JSON().with_variant(postgresql.JSONB(), 'postgresql'), nullable=False),
        sa.Column('occurred_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['case_id'], ['cases.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_audit_logs_case_id'), 'audit_logs', ['case_id'], unique=False)
    op.create_index(op.f('ix_audit_logs_correlation_id'), 'audit_logs', ['correlation_id'], unique=False)
    op.create_index(op.f('ix_audit_logs_occurred_at'), 'audit_logs', ['occurred_at'], unique=False)

    # requirement: NFR-015
    op.create_table(
        'auth_sessions',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('case_id', sa.Uuid(), nullable=True),
        sa.Column('user_id', sa.String(length=128), nullable=False),
        sa.Column('token_hash', sa.String(length=128), nullable=False),
        sa.Column('issued_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('last_activity_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('revoked_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['case_id'], ['cases.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('token_hash')
    )
    op.create_index(op.f('ix_auth_sessions_user_id'), 'auth_sessions', ['user_id'], unique=False)
    op.create_index(op.f('ix_auth_sessions_expires_at'), 'auth_sessions', ['expires_at'], unique=False)

    # Users table for authentication
    op.create_table(
        'users',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('email', sa.String(length=256), nullable=False),
        sa.Column('hashed_password', sa.String(length=128), nullable=False),
        sa.Column('role', sa.String(length=64), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_auth_sessions_expires_at'), table_name='auth_sessions')
    op.drop_index(op.f('ix_auth_sessions_user_id'), table_name='auth_sessions')
    op.drop_table('auth_sessions')
    op.drop_index(op.f('ix_audit_logs_occurred_at'), table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_correlation_id'), table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_case_id'), table_name='audit_logs')
    op.drop_table('audit_logs')
    op.drop_index(op.f('ix_case_events_occurred_at'), table_name='case_events')
    op.drop_index(op.f('ix_case_events_correlation_id'), table_name='case_events')
    op.drop_index(op.f('ix_case_events_case_id'), table_name='case_events')
    op.drop_table('case_events')
    op.drop_index(op.f('ix_case_attachments_case_id'), table_name='case_attachments')
    op.drop_table('case_attachments')
    op.drop_index(op.f('ix_cases_accountable_role'), table_name='cases')
    op.drop_index(op.f('ix_cases_case_state'), table_name='cases')
    op.drop_index(op.f('ix_cases_workflow_type'), table_name='cases')
    op.drop_index(op.f('ix_cases_case_reference'), table_name='cases')
    op.drop_table('cases')
