# Import all models here for Alembic
from app.db.session import Base  # noqa: F401
from app.models.alert import Alert  # noqa: F401
from app.models.content import ContentBrief, ContentDraft  # noqa: F401
from app.models.credential import Credential  # noqa: F401
from app.models.cwv_metric import CWVMetric  # noqa: F401
from app.models.gsc import GscSite  # noqa: F401
from app.models.integration import Integration  # noqa: F401
from app.models.internal_link import InternalLink  # noqa: F401
from app.models.links import LinkScore  # noqa: F401
from app.models.log import AuditLog  # noqa: F401
from app.models.page import Page  # noqa: F401
from app.models.page_metric import PageMetric  # noqa: F401
from app.models.project import Project  # noqa: F401
from app.models.query import Query  # noqa: F401
from app.models.site import Site  # noqa: F401
from app.models.suggestion import Suggestion  # noqa: F401
from app.models.user import User  # noqa: F401
