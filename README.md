Bộ thư viện trực quan hóa dữ liệu:
   Thư viện hiển thị biểu đồ địa lý các tỉnh/thành, phường/xã theo màu từ dữ liệu
   Thư viện hiển thị các biểu đò trực quan nâng cao

Cài đặt:
   # Cài đặt thư viện từ github
   !pip install git+https://github.com/phnampy/datavs

Cách dùng:
   # Sử dụng thư viện - hiển thị bản đồ tỉnh thành
   import datavs.map as gm
   provinces = gm.GeoMap(geo_type='Provinces')
   provinces.show()

   # Sử dụng thư viện - hiển thị bản đồ xã phường (Mặc định Đắk Lắk)
   towns = gm.GeoMap()
   towns.show()

   # Hiển thị mật độ dân số - xã phường
   towns.load_data(color_val='dan_so') #dan_so matdo_km2 dtich_km2
   towns.show(show_name=True, figsize = (20, 16), cmap='Blues');


