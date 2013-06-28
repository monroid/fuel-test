Структура директорий

Набор тестов для Fuel и инфраструктура.

Тесты сводятся к созданию виртуального окружения и развертывания в нем OpenStack при помощи Fuel. Также это используется для подготовки окружения для прогона  набора тестов Tempest.

fuel_test  ( в том же репозитории, что и Fuel: https://github.com/Mirantis/fuel.git     )

    ci    классы реализующие окружения для CI-тестов

    cobbler    тесты для разных вариантов развертывания OpenStack

    config    конфигурационные файлы для tempest* test suite


остальное --- хелперы, базовые классы и прочий вспомогательный код

"остальное" -- тоже имеет важное значение, не совсем хорошо, ограничиваться только этим описанием. Например -- base_test_case.py, config.py, helpers.py, prepare*.py, settings.py!!!, test_config.py, test_manifest.py + важно обозначить использование devops более подробно

Tempest --- это набор интеграционных тестов для Openstack
  (  https://github.com/openstack/tempest )



Библиотека devops

Библиотека позволяет создавать виртульные окружения через libvirt для тестирования

devops ( в отдельном репозитории https://github.com/Mirantis/devops.git  )

    bin    dos.py --- оболочка для управления виртуальными окружениями

    devops    файлы библиотеки Devops

    docs    заготовки для документации (пустые), getstart.rst (как начать работу)

    samples    примеры как создавать виртуальные окружения при помощи devops




Файлы

fuel_test:

README.rst    краткая инструкция по настройке и применению fuel-test

astute.py    формирует конфигурационный Yaml для Astute

base_test_case.py    абстрактный базовый класс для тестов

config.py    класс реализующий конфиг. файлы для astute, openstack

helpers.py    кt

iso_master.py    кt

manifest.py    кt

node_roles.py    краткая инструкция по настройке и применению fuel-test

pip-requires    краткая инструкция по настройке и применению fuel-test

prepare.py    кt

prepare_tempest_ci.py    кt

prepare_tempest.py    краткая инструкция по настройке и применению fuel-test

root.py    краткая инструкция по настройке и применению fuel-test

settings.py    краткая инструкция по настройке и применению fuel-test

test_config.py    кt

test_manifest.py    кt


fuel_test/ci:

README.rst    краткая инструкция по настройке и применению fuel-test

README.rst    краткая инструкция по настройке и применению fuel-test

README.rst    краткая инструкция по настройке и применению fuel-test

README.rst    краткая инструкция по настройке и применению fuel-test

fuel_test/cobbler:

README.rst    краткая инструкция по настройке и применению fuel-test

README.rst    краткая инструкция по настройке и применению fuel-test

README.rst    краткая инструкция по настройке и применению fuel-test
fuel_test/config:

README.rst    краткая инструкция по настройке и применению fuel-test

README.rst    краткая инструкция по настройке и применению fuel-test

README.rst    краткая инструкция по настройке и применению fuel-test






Классы и методы
Классы для создания виртуальных окружений





CiBase - базовый класс для подготовки тестового окружения (группа VM) для интеграционного тестирования (CI)

CiVM -  класс для развертывания тестового окружения на виртуальных машинах (VM)

CiBM -  класс для развертывания тестового окружения на физических машинах
  (BM=Bare Metal)

Эти классы используются в нижеописанных FullTestCase, CompactTestCase, SimpleTestCase,   SingleTestCase и прочих для тестов по развертыванию OpenStack в соответствующих вариантах ( deployment mode ).





Классы для запуска тестовых сценариев

FullTestCase - класс для развертывания тестового окружения для интеграционного тестирования (CI). Данный класс реализует метод-тест test_full который предполагается запускать через nosetests ( https://nose.readthedocs.org ). Метод выполняет развертывание OpenStack в варианте “Multi node HA Standalone” посредством Fuel. Фактически тут один тест, который ничего кроме деплоймета OpenStack не выполняет. Также реализованы и все остальные классы CompactTestCase, MinimalTestCase, SimpleTestCase,  SingleTestCase для других вариантов развертывания.

CompactTestCase - ???

MinimalTestCase - ???


SimpleTestCase - ???

NoopTestCase - ???

NovaSubClassesTestCase - ???



SwiftCase ( test_swift.py ) - класс для тестирования SWIFT.   НЕ ИСПОЛЬЗУЕТСЯ!

class CobblerClient(xmlrpclib.Server)   cobbler_client.py

class NoopTestCase(CobblerTestCase)   test_apply_noop.py

class CompactTestCase(CobblerTestCase)   test_compact.py

class FullTestCase(CobblerTestCase)   test_full.py

class MinimalTestCase(CobblerTestCase)   test_minimal.py

class NovaSubClassesTestCase(CobblerTestCase)   test_nova_subclasses.py

class SimpleTestCase(CobblerTestCase)   test_simple.py

class SingleTestCase(CobblerTestCase)   test_single.py

class SwiftCase(CobblerTestCase)   test_swift.py

class MyTestCase(CobblerTestCase)   tmp.py

class CobblerTestCase(BaseTestCase)   vm_test_case.py





CobblerTestCase ( test_cobbler.py ) - базовый класс на основе которого реализуются классы для тест-кейсов по развертыванию в разных вариантах ( “Single node”, “Multi node HA Standalone”,  “Multi node HA Compact SWIFT”, и т.д. )

BaseTestCase  - базовый родительский класс производный от TestCase из модуля TestCase на основе которого построены все остальные.

Вспомогательные классы и методы

Классы:

Config - ???

SelfTest - ???

Template - ???

Manifest - ???

NodeRoles -???

Nodes - ???

Prepare - ???

PrepareTempest - ???

PrepareTempestCI - ???

TestConfig - ???

TestManifest - ???


