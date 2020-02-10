import setuptools

description_file = open('README.md', 'r', encoding='utf-8')

setuptools.setup(
    name='Zhihu QRCode Login',
    version='0.0.1',
    description='One line to login Zhihu by QRCode.',
    long_description=description_file.read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Crawler995/ZhihuQRCodeLogin',
    author='crawler995',
    author_email='zhang_995@foxmail.com',
    keywords=['Zhihu', 'login'],
    packages=setuptools.find_packages(),
    license='MIT',
    install_requires=[
        'requests'
    ],
    package_dir={'zhihu_qrcode_login': 'zhihu_qrcode_login'}
)