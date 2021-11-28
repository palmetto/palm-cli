================================
Wait. Why Do My CLIs need a CLI?
================================

For a seasoned Engineer, the idea of wrapping public software interfaces in an abstraction layer will probably set off some warning bells. Admittedly, at first glace palm can appear to add unnecessary complexity and “magic” to an already polished API. For example, bringing up a docker-compose service stack:

.. code:: bash
    
    # via native docker-compose
    $ docker-compose up -d 
    Creating network my-project… done

    # via palm
    $ palm up
    Creating network my-project… done


In this case, it is hard to see the argument for palm’s usefulness. But modern software development rarely stays that simple for long. 
Let’s look at a real-world use case where we want to run tests on the Django webapp portion of our monorepo. 
In this case the stack is down and the needed port is allocated by an orphan container.

.. code:: bash 

   # via native bash + docker-compose
   $ docker-compose exec --rm --service-ports my_app /bin/bash -c “pytest webapp/tests/webapp”
   ERROR: No such service: my_app
   
   $ docker-compose up -d 
   ERROR: Bind for 0.0.0.0:8080 failed: port is already allocated
   
   $ docker ps
   CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
   I98ds8sd90gsd    django1    /bin/bash        2 days ago  running
   
   $ docker kill I98ds8sd90gsd
   I98ds8sd90gsd
   
   $ docker-compose up -d 
   Creating network my-project… done

   $ docker-compose exec --rm --service-ports my_app /bin/bash -c “pytest webapp/tests/webapp”
   Running 84 tests via pytest…

   # same thing, via palm

   $ palm test
   Starting compose…
   Unable to compose, stopping orphan container… Stopped.
   Starting compose… Started.
   Running 84 tests via pytest…

Suddenly, palm starts to make a lot of sense. The abstraction layer that palm provides allows you to architect simplicity and consistency into your development environments, across languages, frameworks, and infrastructure designs. You decide what each command does, designing the workflow interface for each repo. A simple, single-container Jekyll app, and complex, multi-cloud microservices ecosystem, implemented by different teams with completely different skills, can share a common interface. 

Palm Is Working Software
====================

    *Through this work we have come to value...
    Working software over comprehensive documentation*

        ~ `Agile Manifesto <https://agilemanifesto.org/#:~:text=processes%20and%20tools-,Working%20software,-over%20comprehensive%20documentation>`_

A core concept in quality programming is `Self-documenting code <https://en.wikipedia.org/wiki/Self-documenting_code>`_. 
Most seasoned Engineers would cringe if they came across a function like this:

.. code:: javascript
   
   /* Function for determining customer balance.
       This function takes the current known balance, 
       queries the bank api with the customer account,
       then if the api returns a new balance it applies it to… (etc etc)
   */ 
   function customerBalance(custId){
      // awful code goes here 
   }

And yet, the first instinct when engineering a development environments is 
often to generate reams of stagnant documentation! 
For example, let’s say a team of Developers randomly suffer from this error: 

.. code:: bash

   $ docker-compose up -d 
   ERROR: unable to read file app/conf: file does not exist or access denied

After hours of painful debugging, it is discovered that this is not a permission or mounting issue,
but that docker is actually out of memory. 
The fix is to clean up the docker environment. 
Convention is to add this find to the project Readme.md, like this: 

.. code::  

   #Readme.md
      
   ## Troubleshooting
   **“ERROR: unable to read file app/conf: file does not exist or access denied”** : 
   your docker environment may be out of memory. Start by running `docker rm -f $(docker ps -qa)` … 

But what if, instead of writing docs - docs the Developers will likely forget to check, 
with steps that will need to methodically replicated, 
what if the fix was automated? Enter palm. 

.. code:: python

   #.palm/cmd_up.py

   def cmd_up(ctx):
       “”” starts the compose stack”””
       echo(“starting docker stack…”)
       exit_code, out, err = ctx.docker_up()
       cryptic_message_indicating_no_memory = “ERROR: unable to read file app/conf: file does not exist or access denied”
       if cryptic_message_indicating_no_memory in err:
           red_echo(“docker may be out of memory, cleaning up first…”)
           ctx.docker_clean()
           ctx.docker_up(bubble_error=True)
           green_echo(“docker stack started.”)       
	
Now and forever, your developers will see this when they run out of memory:

.. code:: bash

   $ palm up 
   Starting docker stack…
   docker may be out of memory, cleaning up first...
   docker stack started.

Of course this solution is very basic. In a real implementation we might want to 
check that the file exists and has the correct permissions, prompt the developer before nuking the docker environment etc. 

**As Engineers, we preach the value of automation and scoff at repetitive, error-prone manual tasks.
Palm is a way for us to practice what we preach.** 

