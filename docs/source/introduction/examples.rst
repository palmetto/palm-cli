========
Examples
========

Onboarding
==========

Setting up a new full-time employee for success is the most straightforward example
of how palm can immediately impact productivity. 

Let’s say today is your first day as an Analytics Engineer for a shop that uses dbt. 
Let’s also say this shop also uses palm, with the palm-dbt plugin. 

Day one goes something like this:

1. You install Docker, git, your text editor and palm
2. You get all your secrets assigned and SSH set up with github
3. You clone the working dbt repo and run `palm` from root. You see something like this: 

.. code:: bash

   $ palm
   Commands: 
   run          executes dbt run in the namespaced schema for your branch
   cycle        executes dbt run, test, run, test 
   cleanup      cleans the local and removes all remote artifacts from testing in the data warehouse
  
   # compile, test etc.
  

4. Using the gitflow naming pattern of ``<branch-type>/<ticket-key>/<description>`` you check out your first work ticket: 

.. code:: bash

   $ git checkout -b feature/DATA-204/fix-sales-column-name

5. You run ``palm cycle`` as a baseline: 

.. code:: bash

   $ palm cycle
   running command `dbt seed && dbt run --vars '{"exclude_ods_keys":"yes", "first_transfer": 20210901}'`
   against schema `TEST.feature_data_204_fix_sales_column_name`
   ## ... dbt run details here
   success. dbt completed with 96 models and 144 tests, run 2x each in 120 seconds.
   cleaning up the remote target... 
   clean. 

Your development work executes in a sophisticated environment with automated namespacing, 
automated cleanup, and idempotency testing. 

There was near-zero learning curve for you, no tribal knowledge transfer needed, and you were able to start adding value hours into your first day on the team.


Cross Platform
==============
Palm is written in Python, giving you the interoperability of a higher level programming language, 
and relies heavily on the ``docker`` and ``docker-compose`` APIs to create OS-agnostic 
development environments. Leveraging palm's native `run_in_docker` commands, you can run the same code
on any system and get the same results. 


Context Switching
=================

Possibly the most powerful long-term impact of palm is the way it removes internal barriers between software workflows. 
Let’s say you are a developer at a modern e-commerce platform. The ecom site is powered by Ruby on Rails. The highly-trafficked content site uses WordPress. Your virtual dressing room software is built on Rocket, and the whole of the infrastructure is managed by Terraform. 
A new feature is rolling out that uses the virtual dressing room. First, you update the Rocket application to enable the feature. You start by reviewing your options (it’s been a minute since you have worked in this repo): 

.. code:: bash 

   $ cd ~/Repos/virtual_dressing_room && palm 
   Commands:
   launch     launches the vdr as a request server (daemon)
   request    starts an interactive request terminal to to the local server
   test          runs all the non-destructive tests locally
   launch-test    runs tests that will destroy the UAT environment, should only be run before a deployment

Once the Rocket code is updated and merged, you launch the feature on the ecom site. 

.. code:: bash 

   $ cd ~/Repos/ecommerce_site && palm up

You make your changes, testing with ``palm test``. The same happens with the WordPress and your infra work.
 
**Here is where it gets interesting!** 

You get a panicked call from the finance team.

It appears the only Data Engineer is on vacation and they forgot a CCPA request due today! 
You quickly clone the data team’s ``ccpa_privacy`` repo, and do this:

.. code:: bash

   $ cd ~/Repos/ccpa_privacy && palm
   Commands:
   delete       deletes (or obfuscates) a user by email address. Enforces financial retention per our privacy policy.
   report       generates a right-of-portability report of the data we have on a user by email address. non-destructive. 

   $ palm report --help 
     Generates a json report of all the found data relating to a given email address. 

     Args: email-address: the email to look up
   
   $ palm report dave@requestedprivacy.com
   Generating report… 
   Report done. Saved to ~/Documents/privacy_report_123.json 

When an organization adopts palm, moving from one codebase to another becomes fluid, and without hard context switches. 
Developers can confidently pick up and start working with any code, anywhere in the organization - including code they have never seen before. 


Consulting
==========

Palm & The Modern Work Dynamic
==============================

Offshoring & Nearshoring
^^^^^^^^^^^^^^^^^^^^^^^^

Gig Work - For the Organization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Gig Work - For the Gig Worker
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^