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




Context Switching
=================

Consulting
==========

Palm & The Modern Work Dynamic
==============================

Offshoring & Nearshoring
========================

Gig Work - As An Organization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Gig Work - As a Gig Worker
^^^^^^^^^^^^^^^^^^^^^^^^^^