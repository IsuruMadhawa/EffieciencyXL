from services.database_service import dao


def get_all_clearance_requests():
    return dao.query_all_clearance_requests()


def get_all_lost_item_reports():
    return dao.query_all_lost_item_reports()
