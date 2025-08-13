import json
import pandas as pd
import geopandas as gpd
import importlib.resources
from importlib.resources import files
import matplotlib.pyplot as plt

DEFAULT_GEO_FORMAT = {
    'figsize': (16, 10), 
    'cmap': 'Greens_r',
    'missing_kwds': {'color': 'grey', 'label': 'No Data'},
    'legend': True,
}

DEFAULT_PROVINCE_COLUMNS = {
    'geo_key': 'ten_tinh',
    'data_key': 'ProvinceName',
    'color_val': 'dtich_km2',
    'text_col': 'ten_tinh',
}

DEFAULT_TOWN_COLUMNS = {
    'geo_key': 'ten_xa',
    'data_key': 'TownName',
    'color_val': 'dtich_km2',
    'text_col': 'ten_xa',
}

def is_list_of_dicts(variable):
    if isinstance(variable, list):
        if all(isinstance(item, dict) for item in variable):
            return True
    return False

class GeoMap():
    def __init__(self, geo_type='Town', province='Đắk Lắk', data=None, **kwagrs):
        # Tải dữ liệu GEO
        geo_file = f"{(province if geo_type=='Town' else 'VN_Provinces')}.geojson"
        with importlib.resources.open_text("datavs.geo", geo_file, encoding="utf-8") as f:
            self._gdf = gpd.GeoDataFrame.from_features (json.load(f), crs="EPSG:4326")

        self._formats = DEFAULT_GEO_FORMAT
        self._columns = DEFAULT_TOWN_COLUMNS if geo_type=='Town' else  DEFAULT_PROVINCE_COLUMNS
        self._data = self.load_data(data, **kwagrs)
        
    def load_data(self, data=None, **kwagrs):
        for agr in kwagrs:
            if agr in self._columns:
                self._columns[agr] = kwagrs.get(agr)

        self._data = pd.json_normalize(data) if is_list_of_dicts(data) else \
                     data if isinstance(data, pd.DataFrame) else \
                     None        
                  
    # Vẽ bản đồ đường biên của các tỉnh kèm theo màu sắc theo giá trị cột color_col  
    def show(self, show_name=False, **kwagrs):
        ax = self._gdf.plot(column=self._columns['color_val'], **{**self._formats, **kwagrs}) if self._data is None else \
             self._gdf.merge(self._data, how='left', left_on=self._columns['geo_key'], right_on=self._columns['data_key'])\
                      .plot(column=self._columns['color_val'], **{**self._formats, **kwagrs})
        ax.set_axis_off()
    
        # Hiển thị tên tỉnh tại tọa độ trung tâm
        if (show_name):
            for idx, row in self._gdf.iterrows():
                x, y = row['geometry'].centroid.x, row['geometry'].centroid.y
                plt.text(x, y, row[self._columns['text_col']], fontsize=8, ha='center', va='center')

        return ax

    def explore(self, **kwagrs):
        ax = self._gdf.explore(column=self._columns['color_val'], **kwagrs) if self._data is None else \
             self._gdf.merge(self._data, how='left', left_on=self._columns['geo_key'], right_on=self._columns['data_key'])\
                      .explore(column=self._columns['color_val'], **kwagrs)
   
        return ax

