from services.database_service import dao


def get_all_clearance_requests():
    return dao.query_all_clearance_requests()


def get_all_lost_item_reports():
    return dao.query_all_lost_item_reports()


def get_single_clearance_request(r_id):
    return dao.query_single_clearance_request(r_id)


def update_clearance_report(r_id, o_id, details):
