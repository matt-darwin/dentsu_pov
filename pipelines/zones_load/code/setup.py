from setuptools import setup, find_packages
setup(
    name = 'zones_load',
    version = '1.0',
    packages = find_packages(include = ('zones_load*', )) + ['prophecy_config_instances'],
    package_dir = {'prophecy_config_instances' : 'configs/resources/config'},
    package_data = {'prophecy_config_instances' : ['*.json', '*.py', '*.conf']},
    description = 'workflow',
    install_requires = [
'databricks-mosaic', 'prophecy_spark_ai', 'google-cloud-storage', 'oauth2-client', 'prophecy-libs==1.9.5'],
    entry_points = {
'console_scripts' : [
'main = zones_load.pipeline:main'], },
    data_files = [(".prophecy", [".prophecy/workflow.latest.json"])],
    extras_require = {
'test' : ['pytest', 'pytest-html'], }
)
