"""Initial schema"""

from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(), nullable=False, unique=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("role", sa.Enum("owner", "admin", "editor", "writer", "viewer", name="userrole"), nullable=False, server_default="admin"),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("owner_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("goals", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "sites",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("project_id", sa.Integer(), sa.ForeignKey("projects.id"), nullable=False),
        sa.Column("domain", sa.String(), nullable=False),
        sa.Column("wp_base_url", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "integrations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("project_id", sa.Integer(), sa.ForeignKey("projects.id"), nullable=False),
        sa.Column("type", sa.Enum("gsc", "psi", "wordpress", "indexnow", "gemini", name="integrationtype"), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "credentials",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("integration_id", sa.Integer(), sa.ForeignKey("integrations.id"), nullable=False),
        sa.Column("key_name", sa.String(), nullable=False),
        sa.Column("value_encrypted", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "gsc_sites",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("site_id", sa.Integer(), sa.ForeignKey("sites.id"), nullable=False),
        sa.Column("property_uri", sa.String(), nullable=False),
    )

    op.create_table(
        "pages",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("site_id", sa.Integer(), sa.ForeignKey("sites.id"), nullable=False),
        sa.Column("url", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column("last_crawled_at", sa.DateTime(), nullable=True),
    )

    op.create_table(
        "queries",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("site_id", sa.Integer(), sa.ForeignKey("sites.id"), nullable=False),
        sa.Column("query_text", sa.String(), nullable=False),
    )

    op.create_table(
        "page_metrics",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("page_id", sa.Integer(), sa.ForeignKey("pages.id"), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("clicks", sa.Float(), default=0),
        sa.Column("impressions", sa.Float(), default=0),
        sa.Column("ctr", sa.Float(), default=0),
        sa.Column("position", sa.Float(), default=0),
    )

    op.create_table(
        "cwv_metrics",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("page_id", sa.Integer(), sa.ForeignKey("pages.id"), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("lcp", sa.Float(), nullable=True),
        sa.Column("inp", sa.Float(), nullable=True),
        sa.Column("cls", sa.Float(), nullable=True),
        sa.Column("lab_json", sa.JSON(), nullable=True),
        sa.Column("field_json", sa.JSON(), nullable=True),
    )

    op.create_table(
        "internal_links",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("from_page_id", sa.Integer(), sa.ForeignKey("pages.id"), nullable=False),
        sa.Column("to_page_id", sa.Integer(), sa.ForeignKey("pages.id"), nullable=False),
        sa.Column("anchor_text", sa.String(), nullable=False),
        sa.Column("score", sa.Float(), nullable=False, server_default="0"),
    )

    op.create_table(
        "linkscore",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("page_id", sa.Integer(), sa.ForeignKey("pages.id"), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("score", sa.Float(), nullable=False, server_default="0"),
    )

    op.create_table(
        "suggestions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("site_id", sa.Integer(), sa.ForeignKey("sites.id"), nullable=False),
        sa.Column("type", sa.Enum("onpage", "internal", "tech", name="suggestiontype"), nullable=False),
        sa.Column("payload_json", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "content_briefs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("site_id", sa.Integer(), sa.ForeignKey("sites.id"), nullable=False),
        sa.Column("topic", sa.String(), nullable=False),
        sa.Column("intent", sa.String(), nullable=True),
        sa.Column("stage", sa.String(), nullable=True),
        sa.Column("outline_json", sa.JSON(), nullable=True),
        sa.Column("checklist_json", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "content_drafts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("site_id", sa.Integer(), sa.ForeignKey("sites.id"), nullable=False),
        sa.Column("wp_post_id", sa.Integer(), nullable=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("slug", sa.String(), nullable=True),
        sa.Column("html", sa.Text(), nullable=True),
        sa.Column("schema_json", sa.JSON(), nullable=True),
        sa.Column("score_onpage", sa.Float(), nullable=True),
        sa.Column("status", sa.String(), nullable=False, server_default="draft"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "alerts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("project_id", sa.Integer(), sa.ForeignKey("projects.id"), nullable=False),
        sa.Column("severity", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("detail", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("project_id", sa.Integer(), sa.ForeignKey("projects.id"), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("action", sa.String(), nullable=False),
        sa.Column("payload_json", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("logs")
    op.drop_table("alerts")
    op.drop_table("content_drafts")
    op.drop_table("content_briefs")
    op.drop_table("suggestions")
    op.drop_table("linkscore")
    op.drop_table("internal_links")
    op.drop_table("cwv_metrics")
    op.drop_table("page_metrics")
    op.drop_table("queries")
    op.drop_table("pages")
    op.drop_table("gsc_sites")
    op.drop_table("credentials")
    op.drop_table("integrations")
    op.drop_table("sites")
    op.drop_table("projects")
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS userrole")
    op.execute("DROP TYPE IF EXISTS integrationtype")
    op.execute("DROP TYPE IF EXISTS suggestiontype")
