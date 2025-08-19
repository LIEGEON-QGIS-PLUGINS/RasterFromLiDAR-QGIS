def classFactory(iface):
    from .RasterFromLiDAR import LiDARPlugin
    return LiDARPlugin(iface)
