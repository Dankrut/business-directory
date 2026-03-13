from .building import BuildingWithOrganizations
from .activity import ActivityWithChildren
from .organization import Organization

# перестраиваем все схемы с циклическими ссылками
BuildingWithOrganizations.model_rebuild()
Organization.model_rebuild()
ActivityWithChildren.model_rebuild()
