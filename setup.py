from setuptools import find_packages, setup

package_name = 'ntu_dorm_lighting'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'paho-mqtt'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='your.email@domain.com',
    description='Automated scheduled lighting controller for NTU dorms using ROS 2 and MQTT.',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'lighting_controller = ntu_dorm_lighting.lighting_controller:main'
        ],
    },
)
