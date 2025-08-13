# setup.py

from setuptools import setup, find_packages

setup(
    name='datavs',
    version='1.0',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=["pandas", "geopandas", "matplotlib", "seaborn"],
    author='Hồ Phương Nam',
    description='Thư viện trực quan hóa dữ liệu nâng cao',
    include_package_data=True,
    package_data={'datavs': ['geo/*.geojson']},  # dữ liệu địa lý GEO
)