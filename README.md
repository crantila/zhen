Zhen
====

汉英词典 Chinese-English Dictionary

https://zhen-crantila.rhcloud.com/


What?
-----

It's a Chinese-English translating dictionary that I'm writing for the
["10k Apart" competition](https://a-k-apart.com/). I don't expect to win---my visual design skills
aren't that good---but the goal is to learn how to build a web app without any front-end frameworks
while also building something that I want to use.


Setup for Development
---------------------

1. Run the "bootstrap.sh" script from the repository root directory. (That is, the same directory
   as this `README.md` file).
1. Make a virtualenv and activate it.
1. Update pip and setuptools (`pip install -U pip setuptools`).
1. Install *Zhen* to the virtualenv (`pip install -e .` in this directory).

And run it with `python -m zhen`.


Deploy to OpenShift
-------------------

*Zhen* can run on the [Red Hat OpenShift](https://openshift.redhat.com/) cloud service. When you
create your gear, give this repository's URL as the starting URL. You should not have to modify
anything for *Zhen* to work!


Deploy to Azure
---------------

I'll have to deploy on Microsoft Azure for the "10k Apart" contest. Instructions to follow...


Attribution
-----------

This dictionary web app uses the contents of the MDBG dictionary, available under a Creative Commons
license from http://www.mdbg.net/chindict/chindict.php?page=cc-cedict .
