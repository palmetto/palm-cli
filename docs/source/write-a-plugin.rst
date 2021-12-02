==============
Write a plugin
==============

Hello there, friend! Thank you in advance for your interest in writing a plugin for 
Palm CLI! If you have questions or want to discuss your ideas, please feel free to
contact the Core team at <data-analytics-team@palmetto.com>


Getting started
===============

Palm includes a command to generate a plugin skeleton. You can use it to get started.

1. cd into an active project - this is necessary at the moment as palm commands 
   are not currently available outside of an initialized git repository.
2. Run ``palm plugin new --name <plugin-name>`` and follow the prompts.
3. Your new plugin skeleton is created and ready for you to add commands!

Installing your plugin during local development
===============================================

When developing a new plugin, you will want to install your plugin
so that you can test it out.  To do this, run the following command from
your plugin's root directory:

.. code:: bash
  
  python3 -m pip install .

**Note**: Due to the way plugins are used by palm, you will need to re-install 
the plugin every time you want to test changes to the plugin
