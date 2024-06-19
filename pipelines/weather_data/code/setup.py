from setuptools import setup, find_packages
setup(
    name = 'weather_data',
    version = '1.0',
    packages = find_packages(include = ('weather_data*', )) + ['prophecy_config_instances'],
    package_dir = {'prophecy_config_instances' : 'configs/resources/config'},
    package_data = {'prophecy_config_instances' : ['*.json', '*.py', '*.conf']},
    description = 'workflow',
    install_requires = [
'databricks-mosaic', 'prophecy_spark_ai', 'google-cloud-storage', 'oauth2-client', 'prophecy-libs==1.8.19'],
    entry_points = {
'console_scripts' : [
'main = weather_data.pipeline:main'], },
    data_files = [(".prophecy", [".prophecy/workflow.latest.json"])],
    extras_require = {
'test' : ['pytest', 'pytest-html'], }
)
