import mongo_module


def create(vod_id):
    data = {
        'vod_id': vod_id,
        'channel_id': 1,
        'game': 'PUPG',
        'comment': 'test'

    }
    return mongo_module.insert_vod(data)

def index(highlight_id):
    return mongo_module.index(highlight_id)
