from setuptools import setup, Extension
import platform
import sys

def get_extension_kwargs():
    extra_compile_args = []
    extra_link_args = []
    
    if sys.platform.startswith('linux'):
        extra_compile_args.extend(['-std=c99', '-fPIC', '-O3'])
    elif sys.platform == 'darwin':
        extra_compile_args.extend(['-std=c99', '-fPIC', '-O3', '-mmacosx-version-min=10.9'])
        extra_link_args.append('-mmacosx-version-min=10.9')
    elif sys.platform == 'win32':
        extra_compile_args = ['/O2']  # Optimize for speed on Windows
    
    # Add architecture-specific optimizations
    if platform.machine().lower() in ('x86_64', 'amd64', 'i386', 'i686'):
        if sys.platform != 'win32':
            extra_compile_args.append('-msse2')
        else:
            extra_compile_args.append('/arch:SSE2')
    elif 'arm' in platform.machine().lower():
        if 'linux' in sys.platform:
            extra_compile_args.append('-mfpu=neon')
    elif 'ppc' in platform.machine().lower() or 'powerpc' in platform.machine().lower():
        if 'linux' in sys.platform:
            extra_compile_args.extend(['-mvsx', '-mcpu=power8'])

    return {
        'sources': ['src/base64perf/base64perf.c'],
        'include_dirs': ['src/base64perf'],
        'extra_compile_args': extra_compile_args,
        'extra_link_args': extra_link_args,
    }

base64perf_module = Extension('base64perf.base64perf', **get_extension_kwargs())

setup(
    name='base64perf',
    version='0.0.10',
    description='Fast Base64 encoding/decoding with SSE2 and VSX optimizations',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Oscar Bahamonde',
    author_email="oscar.bahamonde@pucp.pe",
    url='https://github.com/bahamondex/base64perf',
    ext_modules=[base64perf_module],
    packages=['base64perf'],
    package_dir={'base64perf': 'src/base64perf'},    
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: C',
        'Operating System :: POSIX :: Linux',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    python_requires='>=3.8',
    extras_require={
        'dev': ['pytest', 'pyright', 'isort', 'black'],
    }
)