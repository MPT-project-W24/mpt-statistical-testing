from setuptools import setup, find_packages

setup(
   name='TrackONauts',
   version='1.0',
   description='A useful module',
   author='Man Foo',
   author_email='foomail@foo.example',
   packages=find_packages(), #['TrackONautsStats', 'video_quality_map', 'data_separation', 'TrackONautsVis', 'user_input_filepath'],  #same as name
   install_requires=['pandas', 'numpy'=1.22, 'scipy', 'matplotlib', 'seaborn'], #external packages as dependencies
)
