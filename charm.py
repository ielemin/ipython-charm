import os
import time
import IPython
from abc import ABCMeta, abstractmethod, abstractproperty
from IPython.core.magics.execution import _format_time as format_time

__author__ = 'ielemin'


class AbstractCharm(metaclass=ABCMeta):
    """Abstract method for providing IPython.events handlers.

    See 'https://ipython.org/ipython-doc/3/api/generated/IPython.core.events.html'
    """

    def __init__(self):
        pass

    @abstractproperty
    def name(self):
        pass

    @abstractmethod
    def on_shell_initialized(self, isi):
        """Fires after initialisation of InteractiveShell.

        This is before extensions and startup scripts are loaded, so it can only be set by subclassing.
        :param isi: InteractiveShell instance
        """
        pass

    @abstractmethod
    def on_pre_run_cell(self):
        """Process when called at cell execution, before cell content runs.
        """
        pass

    @abstractmethod
    def on_post_run_cell(self):
        """Process when called at cell execution, after cell content has run.
        """
        pass

    @abstractmethod
    def on_pre_execute(self):
        """Fires before code is executed in response to user/frontend action.

        This includes comm and widget messages and silent execution, as well as user code cells.
        """
        pass

    @abstractmethod
    def on_post_execute(self):
        """Fires after code is executed in response to user/frontend action.

        This includes comm and widget messages and silent execution, as well as user code cells.
        """
        pass

    @abstractmethod
    def register_magic_functions(self):
        """Register magic functions modifying the behaviour of this class.
        """
        pass

    @abstractmethod
    def unregister_magic_functions(self):
        """Unregister magic functions modifying the behaviour of this class.
        """
        pass

    def print(self, msg, *args, **kwargs):
        """Redefinition of 'print' including the charm name.
        """
        print('<{0}> '.format(self.name()) + msg, *args, **kwargs)


class BasicTimer(AbstractCharm):
    """A class displaying some capabilities of the 'charm' framework.
    """

    def __init__(self):
        super().__init__()

        # Gives user's home directory
        user_home = os.path.expanduser('~')
        # Gives username by splitting path based on OS
        self.username = os.path.split(user_home)[-1]

        self.last_time_point = time.time()
        self.all_cell_time_span = 0
        print('<{0}> Run by {1}'.format(self.name(), self.username))

    def name(self):
        return 'Timer'

    # Invisible magic implementations

    def on_pre_run_cell(self):
        self.last_time_point = time.time()

    def on_post_run_cell(self):
        new_time_point = time.time()
        time_span = new_time_point - self.last_time_point

        self.last_time_point = new_time_point
        self.all_cell_time_span += time_span

        print('Time (this cell): {0}'.format(format_time(time_span)))
        print('Time (all cells): {0}'.format(format_time(self.all_cell_time_span)))

    def on_shell_initialized(self, isi):
        pass

    def on_pre_execute(self):
        pass

    def on_post_execute(self):
        pass

    # Explicit magic implementations

    def register_magic_functions(self):
        current_isi.register_magic_function(self.magic, magic_kind='line', magic_name='TIMER')

    def unregister_magic_functions(self):
        current_isi.unregister_magic_function(None, magic_kind='line', magic_name='TIMER')

    def magic(self, spell):
        """Modify class behaviour when called with the appropriate spell

        :param spell: a str encoding a spell
        """
        spell = str.upper(spell)
        if spell == 'RESET':
            self.all_cell_time_span = 0
            self.last_time_point = time.time()
            self.print('Reset')
        elif spell == 'WHOAMI':
            self.print('You are: {0}'.format(self.username))
        else:
            self.print('Spell not defined: "{0}"'.format(spell))


class Sorcerer:
    """Handle all charms and magically change their behaviour.
    """

    def __init__(self, isi):
        # Event handler categories
        """

        :param isi: an InteractiveShell instance
        """
        self.isi = isi

    def invoke(self, charm_class_name):
        """Invoke a charm by its name

        :param charm_class_name: a str representing the name of a charm class
        """
        charm = AbstractCharm()  # TODO implement this by reflection

        self._invoke(charm)

    def revoke(self, charm_class_name):
        """Revoke a charm by its name

        :param charm_class_name: a str representing the name of a charm class
        """
        charm = AbstractCharm()  # TODO implement this by reflection

        self._revoke(charm)

    def _invoke(self, charm):
        """Invoke a charm

        :param charm: an AbstractCharm instance
        """
        if not issubclass(type(charm), AbstractCharm):
            print('Requested charm type {0} is not a subclass of AbstractCharm and cannot be loaded'.format(
                type(charm)))
            return
        print('Charm <{0}> invoked'.format(charm.name()))
        self.isi.events.register('shell_initialized', charm.on_shell_initialized)
        self.isi.events.register('pre_run_cell', charm.on_pre_run_cell)
        self.isi.events.register('post_run_cell', charm.on_post_run_cell)
        self.isi.events.register('pre_execute', charm.on_pre_execute)
        self.isi.events.register('post_execute', charm.on_post_execute)
        charm.register_magic_functions()

    def _revoke(self, charm):
        """Revoke a charm

        :param charm: an AbstractCharm instance
        """
        if not issubclass(type(charm), AbstractCharm):
            return
        print('Charm <{0}> revoked'.format(charm.name()))
        self.isi.events.unregister('shell_initialized', charm.on_shell_initialized)
        self.isi.events.unregister('pre_run_cell', charm.on_pre_run_cell)
        self.isi.events.unregister('post_run_cell', charm.on_post_run_cell)
        self.isi.events.unregister('pre_execute', charm.on_pre_execute)
        self.isi.events.unregister('post_execute', charm.on_post_execute)
        charm.unregister_magic_functions()


# Declare your own charms here
# ...

# Current InteractiveShell instance
current_isi = IPython.get_ipython()

# The sorcerer
sorcerer = Sorcerer(current_isi)

# Magic functions invoking the sorcerer
current_isi.register_magic_function(sorcerer.invoke, magic_kind='line', magic_name='INVOKE')
current_isi.register_magic_function(sorcerer.revoke, magic_kind='line', magic_name='REVOKE')

# Invoke the sorcerer with the charms
timer = BasicTimer()
sorcerer._invoke(timer)  # We would like to call '%WITCH BasicTimer' instead
# Invoke your own charms here...
