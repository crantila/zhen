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


Design Decisions
----------------

Why load a webfont? Some users or devices may not have a font that can display Chinese characters,
so I thought it would be important to include one. Obviously it would be too big to load by default,
so it's "lazy loaded" only if the user has JavaScript enabled.

I split the CSS into two "zones." The CSS required to make the site bearable is all included in a
`<style>` element on every page. The "extra.css" file includes more styling to make the site...
well... even more bearable.

The results table on mobile screens is, uh, different. On screens wider than 500px, it's a regular
table. On smaller screens, the regular table is still usable but when the "extra.css" is loaded,
each column is vertically aligned, with each row separated by a visible divider. Therefore the same
semantically correct `<table>` HTML structure is used in both cases.

I didn't want to re-style the radio buttons from scratch. I tried pretty hard to avoid it. In the
end, I don't mind the radio button appearance, but all my browsers gave a :focus indicator that
ranged from poor to awful... so the default styling was not very accessible! Thankfully, one of
the world's great web design heroes suffered on our behalf:
https://www.sitepoint.com/replacing-radio-buttons-without-replacing-radio-buttons/
As it goes for this 10k contest, this is a pretty heavy solution. And I don't think I've really
produced something visually appealing. Damn.
