from typing import List

from google_data_manager._google_conf import spreadsheets_service


def clear_sheet(spreadsheet_id: str, sheet_name: str) -> None:
    (spreadsheets_service.spreadsheets()
                         .values()
                         .batchClear(spreadsheetId=spreadsheet_id,
                                     body={'ranges': [f'{sheet_name}!A2:C']}).execute())


def rewrite_data_to_sheet(spreadsheet_id: str, data: List[List[str]], sheet_name: str) -> None:
    clear_sheet(spreadsheet_id, sheet_name)
    result = spreadsheets_service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [{'range': f'{sheet_name}!A2:C', 'majorDimension': 'ROWS', 'values': data}]
        }
    ).execute()
    print('{0} cells updated.'.format(result.get('totalUpdatedCells')))
