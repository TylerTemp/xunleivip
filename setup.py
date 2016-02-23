from setuptools import setup
import os
import sys

if sys.version_info[0] < 3:
    from codecs import open

with open(os.path.join(os.path.dirname(__file__), 'README.md'),
          'r', encoding='utf-8') as f:
    long_description = f.read()

    try:
        import pypandoc
        long_description = pypandoc.convert(
                long_description, 'rst', format='md')
    except BaseException as e:
        print(("DEBUG: README in Markdown format. It's OK if you're only "
               "installing this program. (%s)") % e)

setup(
    name='xunleivip',
    py_modules=['xunleivip'],
    package_data={
        '': [
            'README.md'
        ]
    },
    version='0.0.2',
    author='TylerTemp',
    author_email='tylertempdev@gmail.com',
    url='https://github.com/TylerTemp/xunleivip',
    download_url='http://github.com/TylerTemp/xunleivip/zipball/master/',
    license='GPLv3',
    description=('xunlei VIP account from 9sep.org'),
    keywords='xunlei VIP',
    long_description=long_description,
    install_requires=[
        'html5lib',
        'requests',
        'beautifulsoup4',
        'clipboard'
    ],
    entry_points={
        'console_scripts': [
        'xlvip = xunleivip:main'
        ]
    },
    platforms='linux',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Utilities',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
        ],
)
