from services.database_service import dao


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
