from datetime import datetime, timedelta

from aiogoogle import Aiogoogle
from app.core.config import settings


FORMAT = '%Y/%m/%d %H:%M:%S'

SHEETS_API_NAME = 'sheets'
SHEETS_API_VERSION = 'v4'

DRIVE_API_NAME = 'drive'
DRIVE_API_VERSION = 'v3'

# Spreadsheet body
REPORT_TITLE = 'Отчёт от {datetime_now}'
LOCATE = 'ru_RU'
SHEET_TYPE = 'GRID'
SHEET_ID = 0
SHEET_TITLE = 'Лист1'
ROW_COUNT = 100
COLUMN_COUNT = 11

# Permissions
TYPE = 'user'
ROLE = 'writer'

# Spreadsheet update values
TABLE_INITIAL_VALUES = [
    ['Отчёт от', 'Текущее время'],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание'],
]
RANGE = 'A1:E30'
INPUT_OPTION = 'USER_ENTERED'
MAJOR_DIMENSION = 'ROWS'


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    service = await wrapper_services.discover(SHEETS_API_NAME,
                                              SHEETS_API_VERSION)
    spreadsheet_body = dict(
        properties=dict(
            title=REPORT_TITLE.format(
                datetime_now=datetime.now().strftime(FORMAT),
            ),
            locale=LOCATE,
        ),
        sheets=[
            dict(
                properties=dict(
                    sheetType=SHEET_TYPE,
                    sheetId=SHEET_ID,
                    title=SHEET_TITLE,
                    gridProperties=dict(
                        rowCount=ROW_COUNT,
                        columnCount=COLUMN_COUNT,
                    ),
                ),
            ),
        ]
    )
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle,
) -> None:
    permissions_body = dict(
        type=TYPE,
        role=ROLE,
        emailAddress=settings.email,
    )
    service = await wrapper_services.discover(DRIVE_API_NAME,
                                              DRIVE_API_VERSION)
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields='id'
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        projects: list,
        wrapper_services: Aiogoogle,
) -> None:
    service = await wrapper_services.discover(SHEETS_API_NAME,
                                              SHEETS_API_VERSION)
    TABLE_INITIAL_VALUES[0][1] = datetime.now().strftime(FORMAT)
    table_values = [
        *TABLE_INITIAL_VALUES,
        *[[project['name'],
           str(timedelta(seconds=project['duration'])),
           project['description']] for project in projects]
    ]
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=RANGE,
            valueInputOption=INPUT_OPTION,
            json=dict(
                majorDimension=MAJOR_DIMENSION,
                values=table_values,
            )
        )
    )
