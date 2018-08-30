from setuptools import setup


setup(name='simulation',
      version='0.1',
      description='Simulating the performance of VMs and FaaS',
      author='Timon Back',
      license='MIT',
      install_requires=[
          'matplotlib',
          'falcon',
          # 'gunicorn', #Linux
          'waitress',  # Windows
          'httpie',  # Nice http client

          # Development
          'coverage'
      ],
      test_suite='tests.all_tests.suite',
      zip_safe=False)
