===============
Code generation
===============

Palm includes a set of code generation commands that allow you to generate code
for your project, automating repetitive boiler plating tasks, and making your
codebase more consistent.

Code generation in palm is powered by `Jinja2 <https://jinja2docs.readthedocs.io/en/stable/>`_
and `PyYAML <https://pyyaml.org/>`_.

Basics
======

To use Palm code generation you will need:

1. A directory of templates. We recommended you make a subdirectory within your
   project's .palm directory.
2. A YAML configuration file called ``template-config.yaml`` - this is a
   configuration file that describes how to generate code.
3. A palm command which is decorated with the ``@click.pass_obj`` decorator and
   calls ``environment.generate(template_path, output_path, replacements)``.

For full documentation of the generator see ``palm/code_generator.py`` in the Palm
CLI source code

Template config
===============

The ``template-config.yaml`` file is a fundamental piece of code generation with palm.
It describes the directory structure we want to create, and where each of our templates
will generate code.

The config file works on 2 top-level objects:
1. ``directories`` - a list of directories to create.
2. ``templates`` - a dict of templates to use, and where to use them. The key is the
name of the template, and the value is the path at which we want to create a file from it.

Each line of the template-config is parsed by jinja, which enables you to use replacements
in your config file.

Example template config

.. code:: yaml

   directories:
     - "{{model_name}}"
   files:
     - base_model.sql: "{{model_name}}/{{model_name}}.sql"
     - base_model.yml: "{{model_name}}/{{model_name}}.yml"

The ``replacements`` dict allows this template-config to be used to create a directory
containing an appropriately named sql file and a yaml file.

Gotchas
=======

Generating code is awesome, but there are gotchas to be aware of.

1. Generating code that contains jinja is a pain, all jinja expressions must be
   provided as replacements in the template, to prevent jinja from trying to
   evaluate them during code generation.
