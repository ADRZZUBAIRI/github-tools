from setuptools import setup, find_packages
import os

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='contractor-lead-scraper',
    version='1.0.0',
    description='High-speed Google Maps local business scraper with async email crawling and contractor data enrichment.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Abdul Rehman Zubairi (WebSmitherz)',
    author_email='hello@websmitherz.com',
    url='https://websmitherz.com',
    project_urls={
        'Source': 'https://github.com/ADRZZUBAIRI/free-gmaps-lead-scraper',
        'Agency Hub': 'https://websmitherz.com',
        'Contractor Schema Generator': 'https://websmitherz.com/tools/contractor-schema-generator',
        'Roofing SEO Playbook': 'https://websmitherz.com/resources/seo/roofing-seo-guide',
        'Custom Software & Webhooks': 'https://websmitherz.com/services/custom-software',
    },
    packages=find_packages(),
    py_modules=['free_gmaps_lead_scraper'],
    install_requires=[
        'playwright>=1.40.0',
        'aiohttp>=3.9.0',
        'beautifulsoup4>=4.12.0',
    ],
    entry_points={
        'console_scripts': [
            'contractor-scraper=free_gmaps_lead_scraper:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    keywords='google-maps-scraper lead-generation web-scraper contractor-leads email-crawler local-seo websmitherz',
    python_requires='>=3.9',
)
