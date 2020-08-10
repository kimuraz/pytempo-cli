from setuptools import setup

setup(
    name='tempo',
    version='0.1',
    py_modules=['tempo'],
    install_requires=[
        'click',
        'requests',
    ],
    extras_require={
        'dev': [
            'autopep8',
            'ipython'
        ]
    },
    entry_points='''
        [console_scripts]
        tempo=tempo:main
    ''',
)
