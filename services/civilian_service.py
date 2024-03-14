from services.database_service import dao


def complaint(name, division, district, complaint):
    """
    Add a complaint to the database
    Args:
        name: name of the civilian
        division: police division
        district: district
        complaint: the complaint

    Returns:
        "Complaint is sent" if the complaint was inserted successfully
        An error message if the complaint was not inserted successfully
    """
    return dao.insert_complaint(name, division, district, complaint)


def clearance_request(name, division, district, description):
    """
    Add a clearance request to the database
    Args:
        name: name of the civilian
        division: police division
        district: district
        description: description of the request

    Returns:
        "Request for clearance is sent" if the request was inserted successfully
        An error message if the request was not inserted successfully
    """
    return dao.insert_clearance_request(name, division, district, description)


def add_lost_item_report(name, division, district, item, description):
    """
    Add a lost item report to the database
    Args:
        name: name of the civilian
        division: police division
        district: district
        item: the lost item
        description: description of the lost item

    Returns:
        "Lost item report is sent" if the report was inserted successfully
        An error message if the report was not inserted successfully
    """
    return dao.insert_lost_item_report(name, division, district, item, description)
