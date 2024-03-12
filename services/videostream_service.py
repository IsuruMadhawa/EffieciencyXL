from services.database_service import dao


def add_video_data(label, location, misc, img):
    return dao.insert_video_data(label, location, misc, img)


def get_feeddata_for_name(name: str):
    return dao.query_feeddata_for_name(name)
