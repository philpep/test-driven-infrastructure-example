##################################
Test driven infrastructure example
##################################

This is a sample project that achieve Test driven infrastructure.

Requirements:

- Easy to install
- Easy to use
- Speed testing
- Usable on normal developer hardware
- Usable on a CI server
- Should test both full and upgrade deployment


The stack
=========

This is a brief description of the tools used in this project, but each has
alternatives that you could use on your stack.


- Docker_ provide a fast system that is pretty close to production one and it
  is easy to install on a modern Linux distro. Alternatives: Qemu_, Xen_,
  VMWare_, Libvirt_...
- Vagrant_ can run multiples machines and provision them. Alternatives:
  Test-Kitchen_, Beaker_, shell script.
- Ansible_. Alternatives: Puppet_, Chef_, Salt_...
- Testinfra_ to run tests. Alternatives: Serverspec_, shell script.
- Tox_ to setup the virtualenv and run vagrant and testinfra. Alternatives:
  Make, shell script.
- Travis_ as CI server to run tests on pull requests. Alternatives: Jenkins_


Installation
============

You will need a recent (>= 1.7) vagrant that's supports docker:
https://www.vagrantup.com/downloads

To install docker see https://docs.docker.com/installation/

Then install tox and requirements to build the virtualenv::

    $ sudo apt-get install python-tox python-dev


To run the full test suite just run `tox`.


Infrastructure code
===================

`The playbook
<https://github.com/philpep/test-driven-infrastructure-example/blob/master/playbook.yml>`_
is a simple Nginx_ installation that setup an website with a "Hello world"
page.


Target images
=============

Two docker images (based on ubuntu:trusty) are configured in the `vagrant
config
<https://github.com/philpep/test-driven-infrastructure-example/blob/master/Vagrantfile>`_,
A default image that is not provisioned and a production image that is
provisioned at the same state than your production servers (eg: master branch).

The default image is build using `this Dockerfile
<https://github.com/philpep/test-driven-infrastructure-example/blob/master/Dockerfile>`_::

    $ docker build -t philpep/test-driven-infrastructure-example:default .


The production image is the default image that is provisioned::

    $ vagrant up --no-provision --provider=docker default
    $ vagrant provision default
    ==> default: Running provisioner: ansible...

    PLAY [all] ********************************************************************

    [... ansible stuff ...]
    PLAY RECAP ********************************************************************
    default                    : ok=6    changed=6    unreachable=0    failed=0


    $ docker ps
    CONTAINER ID        IMAGE                                              [...]
    89ab9d4c3e52        philpep/test-driven-infrastructure-example:default [...]

    $ docker commit 89ab9d4c3e52 philpep/test-driven-infrastructure-example:production
    $ docker push philpep/test-driven-infrastructure-example:production


The tests
=========

The tests are written using Testinfra_.

- `test_nginx.py
  <https://github.com/philpep/test-driven-infrastructure-example/blob/master/test_nginx.py>`_
  simple test that validate nginx is working.
- `test_same_state.py
  <https://github.com/philpep/test-driven-infrastructure-example/blob/master/test_same_state.py>`_
  a test that check the website root directory is the same after full (default) or half (production)
  provisioning.


Let's break the tests
=====================

There are `three pull requests
<https://github.com/philpep/test-driven-infrastructure-example/pulls>`_ in this repository.

At a first look, all the patch seems corrects, but in fact they are not.

- `#2 <https://github.com/philpep/test-driven-infrastructure-example/pull/2>`_
  will break if you deploy a new server, but works on an already provisioned
  one.
- `#4 <https://github.com/philpep/test-driven-infrastructure-example/pull/4>`_
  will break an already provisioned server but works on a new one.
- `#3 <https://github.com/philpep/test-driven-infrastructure-example/pull/3>`_
  will result to a different state between your old and new servers.


Now think about your experience with infrastructure code, this is some of the
common error patterns that you have or will encounter.


.. _Docker: https://www.docker.com/
.. _Salt: http://saltstack.com/
.. _Ansible: http://www.ansible.com/
.. _Puppet: https://puppetlabs.com/
.. _Chef: https://www.chef.io/
.. _Serverspec: http://serverspec.org/
.. _Pytest: http://pytest.org
.. _Qemu: http://wiki.qemu.org/Main_Page
.. _Xen: http://www.xenproject.org/
.. _VMWare: https://www.vmware.com
.. _Libvirt: https://libvirt.org/
.. _Test-Kitchen: http://kitchen.ci/
.. _Beaker: https://github.com/puppetlabs/beaker
.. _Vagrant: https://www.vagrantup.com/
.. _Testinfra: https://testinfra.readthedocs.org
.. _Tox: https://tox.readthedocs.org
.. _Nginx: http://nginx.org/
.. _CI: https://en.wikipedia.org/wiki/Continuous_integration
.. _Jenkins: https://jenkins-ci.org/
.. _Travis: https://travis-ci.org/
