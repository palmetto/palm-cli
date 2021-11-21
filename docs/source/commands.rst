========
Commands
========

Commands are python scripts that are executed by Palm CLI. They allow you to run complex 
tasks in a repeatable way, with a simple interface, and ensure everyone on your
team is working with the same tools.

Palm commands import the `click <https://click.palletsprojects.com/en/8.0.x/>`_ 
CLI library, which is a core dependency of palm. Familiarity with the click library
is recommended for developing your own commands, many examples can be found in the
palm-cli repository.

Where do commands come from?
============================

- Palm ships with some commands out-of-the-box that are always available. These are called
  "core" commands. For example the ``palm build`` command is a core command.
- Palm plugins provide commands for working with specific tools. For example, the
  ``palm-dbt`` plugin provides commands for working with dbt projects.
- You can create your own commands within your projects, these are called "repo"
  commands, as they exist only within the project's repository.

Overriding commands
-------------------

With Palm, it is possible to override commands from other plugins. This is done
based on the order of the plugins in the ``.palm/config.yaml`` file, and the naming
of project plugins.

For example, if the ``palm-dbt`` plugin defined a command named ``build`` it would
override the core ``palm build`` command. This is because the commands from the 
``palm-dbt`` plugin are added after the core commands. If you installed a second 
(ficticious) plugin called ``palm-builder`` which also defined a ``build`` command, 
the order of overriding would be determined by the order of plugins in your project's
``.palm/config.yaml`` file. Finally, if you define a ``build`` command in your project,
as a repo command, it would override all other definitions of the ``build`` command.

Command Groups
==============

Command groups are a useful structure for grouping commands together. For example,
if you have multiple commands relating to a single tool, you can group them together
within a command group. This allows you to easily see all the commands for a tool
when you run ``palm <tool name> --help``.

Command groups are a construct provided by click - for more information, see the 
`click documentation on commands and groups <https://click.palletsprojects.com/en/8.0.x/commands/>`_ 

Writing your own commands
=========================

To simplify the process of writing your own commands and command groups,
Palm ships with some scaffolding commands. These commands will generate boilerplate
code for you, allowing you to focus on writing your command's functionality.

- To scaffold a single command you can run 
  ``palm scaffold command --name <command-name>``
- To scaffold a command group you can run 
  ``palm scaffold group --group <group-name> --command <command-name>``

Once you have scaffolded your command or command group. You can edit the generated
file in your .palm directory, add the functionality you need and then run the command
immediately with ``palm <command-name>``.

Conventions
-----------

- Command files are always named ``cmd_{name}.py``
- A command _must_ expose a ``cli`` function. This function is called when the
  command is executed.

Command Syntax
--------------

- The ``cli`` function should be decorated with either the ``@click.command``
  decorator or the ``@click.group`` decorator.
- The ``cli`` function can optionally be decorated with ``@click.pass_context`` and
  accept a ``ctx`` argument, which is a click context. The ctx.obj is a useful 
  Environment provided by palm that enables you to perform complex operations, like
  running in docker containers, generating code, etc.
- For commands within a command group, each command _must_ be decorated with the
  ``@cli.command`` decorator. Note that this is different from the ``@click.command``
  decorator, as the command belongs to the ``@click.group()`` which is always the
  ``cli`` function.

Common patterns and important notes
-----------------------------------

**Run in docker**:

The global ``run_in_docker`` function is used to execute a command in the docker 
container for the current project. This is used in many palm commands. This function
is provided via the palm context. If you want to use ``run_in_docker`` in your 
own command, ensure you use the ``@click.pass_context`` decorator for your command, 
then use ``ctx.obj.run_in_docker(command)``.

**Run on Host**:

Palm provides a simple interface for running shell commands directly on your machine via
the context (similarly to how ``run_in_docker`` is accessed, via ``ctx.obj``). We highly
recommend using ``run_on_host`` over rolling your own subprocess commands.

.. warning:: 

  **Why Not Use subprocess?**

  The prime directive of palm is to give all your developers an identical interface and 
  experience, regardless of environment. Different versions of python running on different
  operating systems can behave differently when calling ``subprocess``; palm normalizes this
  behavior in ```ctx.obj.run_on_host``. 

**Importing code**:

When writing "repo" commands in your project, you will not be able to use 
conventional relative imports in your commands, as the command is executed in 
the context of palm. If you need to share logic between commands, or import code
from your project, you must do this with the ``ctx.obj.import_module`` function. 
This function is provided via the palm context and uses importlib to ensure
your shared code is imported from the correct location at run time.

**Examples**:

Maybe you want a command that kicks off a slow-building container
as a background process, but you want to see it complete before moving it back. 
That could look something like this:

.. code:: python

  ## ./palm/cmd_slow_starter.py
  ...
  @click.command('slow_starter')
  @click.pass_context
  def cli(ctx):
      """Starts the container as daemon, watches the logs, then exits"""
      ctx.run_on_host("docker-compose run -d super_slow_starting_django_app",
                           bubble_error=True)
        
      ## this is where we watch, pseudo-blocking
      building_logs = str()
      while "Starting local webserver via runserver on port 8080..." \
        not in building_logs:
          logs, _, _ = ctx.run_on_host("docker-compose logs static_app")
            if logs != building_logs:
                building_logs = logs
                click.echo(logs)
      click.secho("Super-slow app is _finally_ ready!", fg="green")