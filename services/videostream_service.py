
from services.database_service import dao


def add_video_data(label, location, timestamp, misc):
    return insert_video_data(label, location, timestamp, misc)
