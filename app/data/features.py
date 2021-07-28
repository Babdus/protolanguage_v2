from app.data.pickles import features_info
from app.models.feature import Feature

features_cache = {k: Feature(v[1], k, v[2], v[0]) for k, v in features_info.items()}
fts = features_cache
empty_feature = features_cache['X']
