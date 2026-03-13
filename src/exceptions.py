from fastapi import HTTPException


class DirectoryException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(DirectoryException):
    detail = "Объект не найден"


class OrganizationNotFoundException(ObjectNotFoundException):
    detail = "Организация не найдена"


class BuildingNotFoundException(ObjectNotFoundException):
    detail = "Здание не найдено"


class ActivityNotFoundException(ObjectNotFoundException):
    detail = "Вид деятельности не найден"


class NoOrganizationsInAreaException(DirectoryException):
    detail = "В указанном радиусе нет организаций"


class NoOrganizationsInBuildingException(DirectoryException):
    detail = "В здании нет организаций"


class NoOrganizationsByActivityException(DirectoryException):
    detail = "По указанному виду деятельности нет организаций"


class DirectoryHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self, *args, **kwargs):
        super().__init__(status_code=self.status_code, detail=self.detail)


class OrganizationNotFoundHTTPException(DirectoryHTTPException):
    status_code = 404
    detail = "Организация не найдена"


class BuildingNotFoundHTTPException(DirectoryHTTPException):
    status_code = 404
    detail = "Здание не найдено"


class ActivityNotFoundHTTPException(DirectoryHTTPException):
    status_code = 404
    detail = "Вид деятельности не найден"


class NoOrganizationsInAreaHTTPException(DirectoryHTTPException):
    status_code = 404
    detail = "В указанном радиусе нет организаций"


class NoOrganizationsInBuildingHTTPException(DirectoryHTTPException):
    status_code = 404
    detail = "В указанном здании нет организаций"


class NoOrganizationsByActivityHTTPException(DirectoryHTTPException):
    status_code = 404
    detail = "По указанному виду деятельности нет организаций"


class ApiKeyInvalidHTTPException(DirectoryHTTPException):
    status_code = 403
    detail = "Неверный API ключ"
