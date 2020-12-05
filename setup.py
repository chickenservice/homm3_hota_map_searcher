from setuptools import setup, find_packages

setup(
    name='h3map',
    version='0.0.1',
    description='A sample Python project',
    author='Alessio Eberl',
    author_email='alessio.eberl@gmx.at',
    classifiers=[
        'Development Status :: 3 - Alpha',
    ],
    keywords='heroes iii, hota, maps',
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=['click'],
    entry_points={
        'console_scripts': [
            'h3map=h3map.main:h3map',
        ],
    },
)